from collections import deque
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pandas as pd
import pyarrow
from pyarrow import fs

from tecton_core import conf
from tecton_core.query.executor_params import QueryTreeStagingLocation
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.node_interface import recurse_query_tree
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_compute import StagingConfig
from tecton_core.query.rewrite import QueryTreeRewriter


NUM_STAGING_PARTITIONS = 10


@dataclass
class QueryTreeOutput:
    # A map from table name to pyarrow table
    staged_data: Dict[str, pyarrow.Table]
    odfv_input_df: Optional[pd.DataFrame] = None
    result_df: Optional[pd.DataFrame] = None


@attrs.define
class QueryTreeExecutor:
    staging_compute: QueryTreeCompute
    agg_compute: QueryTreeCompute
    # TODO(danny): Consider separating aggregation from AsOfJoin, so we can process sub nodes and delete old
    #  tables in duckdb when doing `from_source=True`
    odfv_compute: QueryTreeCompute
    query_tree_rewriter: QueryTreeRewriter
    executor: ThreadPoolExecutor = attrs.field(init=False)
    s3fs: Optional[fs.S3FileSystem] = attrs.field(init=False)
    _temp_table_registered: Optional[Dict[str, set]] = None

    def __attrs_post_init__(self):
        # TODO(danny): Expose as configs
        self.executor = ThreadPoolExecutor(max_workers=10)
        awsAccessKey = conf.get_or_none("AWS_ACCESS_KEY_ID")
        awsSecretKey = conf.get_or_none("AWS_SECRET_ACCESS_KEY")
        awsSessionToken = conf.get_or_none("AWS_SESSION_TOKEN")
        if awsSecretKey and awsAccessKey:
            self.s3fs = fs.S3FileSystem(
                region="us-west-2",
                access_key=awsAccessKey,
                secret_key=awsSecretKey,
                session_token=awsSessionToken,
            )
        else:
            self.s3fs = None

    def cleanup(self):
        self.executor.shutdown()
        # TODO(danny): drop temp tables

    def exec_qt(self, qt_root: NodeRef) -> pd.DataFrame:
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"QT: {qt_root.pretty_str(columns=True)}")
        # TODO(danny): make ticket to avoid needing setting a global SQL_DIALECT conf
        orig_dialect = conf.get_or_raise("SQL_DIALECT")
        try:
            # Stages the results of spines and pre-partial aggs in S3
            output = self._exec_qt_node(qt_root, QueryTreeStep.PIPELINE)
            # Does partial aggregations and spine joins
            output = self._exec_qt_node(qt_root, QueryTreeStep.AGGREGATION, output)
            # Runs ODFVs
            output = self._exec_qt_node(qt_root, QueryTreeStep.ODFV, output)
            return output.result_df
        finally:
            # TODO(danny): remove staged data
            conf.set("SQL_DIALECT", orig_dialect)

    def _exec_qt_node(
        self, qt_node: NodeRef, query_tree_step: QueryTreeStep, prev_stage_output: Optional[QueryTreeOutput] = None
    ) -> QueryTreeOutput:
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"------------- Executing stage: {query_tree_step} -------------")
            print(f"QT: {qt_node.pretty_str(description=False)}")

        start_time = datetime.now()
        if query_tree_step == QueryTreeStep.PIPELINE:
            stage_output = self._execute_staging_stage(qt_node)
            self.query_tree_rewriter.rewrite(qt_node, query_tree_step)
        elif query_tree_step == QueryTreeStep.AGGREGATION:
            stage_output = self._execute_agg_stage(prev_stage_output, qt_node)
            self.query_tree_rewriter.rewrite(qt_node, query_tree_step)
        elif query_tree_step == QueryTreeStep.ODFV:
            assert prev_stage_output
            assert prev_stage_output.odfv_input_df is not None
            has_odfvs = self._tree_has_odfvs(qt_node)
            if has_odfvs:
                result_df = self.odfv_compute.run_odfv(qt_node, prev_stage_output.odfv_input_df)
            else:
                result_df = prev_stage_output.odfv_input_df
            stage_output = QueryTreeOutput(
                staged_data=prev_stage_output.staged_data,
                odfv_input_df=prev_stage_output.odfv_input_df,
                result_df=result_df,
            )
        else:
            msg = f"Unexpected compute type {query_tree_step}"
            raise Exception(msg)

        if conf.get_bool("DUCKDB_BENCHMARK"):
            stage_done_time = datetime.now()
            print(f"{query_tree_step.name}_TIME_SEC: {(stage_done_time - start_time).total_seconds()}")
        return stage_output

    def _tree_has_odfvs(self, qt_node):
        has_odfvs = False

        def check_for_odfv(node):
            if isinstance(node, MultiOdfvPipelineNode):
                nonlocal has_odfvs
                has_odfvs = True

        recurse_query_tree(
            qt_node,
            lambda node: check_for_odfv(node) if not has_odfvs else None,
        )
        return has_odfvs

    def _execute_staging_stage(self, qt_node: NodeRef) -> QueryTreeOutput:
        conf.set("SQL_DIALECT", self.staging_compute.get_dialect())
        # TODO(danny): handle case where the spine is a sql query string, so no need to pull down as dataframe
        self._maybe_register_temp_tables(qt_root=qt_node, compute=self.staging_compute)

        # For STAGING: concurrently stage nodes matching the QueryTreeStep.PIPELINE filter
        nodes_to_process = self._get_nodes_to_process(qt_node, QueryTreeStep.PIPELINE)
        staging_futures = self._stage_tables_and_load_pa(
            nodes_to_process=nodes_to_process,
            compute=self.staging_compute,
        )
        staged_data = {}
        for future in staging_futures:
            table_name, pa_table = future.result()
            staged_data[table_name] = pa_table

        return QueryTreeOutput(staged_data=staged_data)

    def _execute_agg_stage(self, output: Optional[QueryTreeOutput], qt_node: NodeRef) -> QueryTreeOutput:
        # Need to explicitly set this dialect since it's used for creating the SQL command in QT `to_sql` commands
        conf.set("SQL_DIALECT", self.agg_compute.get_dialect())
        assert output
        # The AsOfJoins need access to a spine, which are registered here.
        self._maybe_register_temp_tables(qt_root=qt_node, compute=self.agg_compute)

        visited_tables = set()
        # Register staged pyarrow tables in agg compute
        for table_name, pa_table in output.staged_data.items():
            self.agg_compute.register_temp_table(table_name, pa_table)
            visited_tables.add(table_name)

        try:
            nodes_to_process = self._get_nodes_to_process(qt_node, QueryTreeStep.AGGREGATION)
            if len(nodes_to_process) > 0:
                futures = self._stage_tables_and_load_pa(
                    nodes_to_process=nodes_to_process,
                    compute=self.agg_compute,
                )
                assert len(futures) == 1
                _, odfv_input_pa = futures[0].result()
                odfv_input_df = odfv_input_pa.to_pandas()
            else:
                # If there are no ODFVs, can run the entire query tree
                output_df_pa = self.agg_compute.run_sql(qt_node.to_sql(), return_dataframe=True)
                odfv_input_df = output_df_pa.to_pandas()
            return QueryTreeOutput(staged_data=output.staged_data, odfv_input_df=odfv_input_df)
        finally:
            for table in visited_tables:
                self.agg_compute.run_sql(f"DROP TABLE IF EXISTS {table}")

    def _get_nodes_to_process(
        self,
        qt_node_ref: NodeRef,
        query_tree_step: QueryTreeStep,
    ) -> List[QueryNode]:
        staging_nodes = []
        queue: Deque = deque()
        queue.append(qt_node_ref)
        while len(queue) > 0:
            curr_node = queue.pop().node
            if isinstance(curr_node, StagingNode) and curr_node.query_tree_step == query_tree_step:
                staging_nodes.append(curr_node)
                continue
            for child_node_ref in curr_node.inputs:
                queue.append(child_node_ref)
        return staging_nodes

    def _stage_tables_and_load_pa(
        self,
        nodes_to_process: List[QueryNode],
        compute: QueryTreeCompute,
    ) -> List[Future]:
        staging_futures = []
        for node in nodes_to_process:
            # TODO(danny): also process UserSpecifiedDataNode
            if isinstance(node, StagingNode):
                future = self.executor.submit(self._process_staging_node, node, compute)
                staging_futures.append(future)
        return staging_futures

    def _process_staging_node(self, qt_node: StagingNode, compute: QueryTreeCompute) -> Tuple[str, pyarrow.Table]:
        start_time = datetime.now()
        staging_table_name = qt_node.staging_table_name_unique()
        s3_path = (
            f"{qt_node.staging_s3_prefix}{staging_table_name}"
            if qt_node.staging_location == QueryTreeStagingLocation.S3
            else None
        )
        maybe_memory_table = compute.stage(
            staging_config=StagingConfig(
                destination=qt_node.staging_location,
                sql_string=qt_node._to_staging_query_sql(),
                table_name=staging_table_name,
                s3_path=f"s3://{s3_path}" if s3_path else None,
                num_partitions=NUM_STAGING_PARTITIONS,
            )
        )
        staging_done_time = datetime.now()
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"Stage {staging_table_name} elapsed: " f"{(staging_done_time - start_time).total_seconds()} seconds")

        if qt_node.staging_location == QueryTreeStagingLocation.MEMORY:
            assert maybe_memory_table is not None
            return staging_table_name, maybe_memory_table
        elif qt_node.staging_location == QueryTreeStagingLocation.S3:
            import pyarrow.parquet as pq

            pa_table = pq.read_table(s3_path, filesystem=self.s3fs)
            read_s3_time = datetime.now()
            if conf.get_bool("DUCKDB_DEBUG"):
                print(
                    f"Load from S3 {staging_table_name} elapsed: "
                    f"{(read_s3_time - staging_done_time).total_seconds()} seconds"
                )
            if conf.get_bool("DUCKDB_BENCHMARK"):
                print(f"S3_DATA_NBYTES_{staging_table_name}: {pa_table.nbytes}")
            return staging_table_name, pa_table
        else:
            msg = f"Unsupported staging mode: {qt_node.staging_location}"
            raise Exception(msg)

    def _maybe_register_temp_tables(self, qt_root: NodeRef, compute: QueryTreeCompute) -> None:
        self._temp_table_registered = self._temp_table_registered or {}

        dialect = compute.get_dialect()
        if dialect not in self._temp_table_registered:
            self._temp_table_registered[dialect] = set()

        def maybe_register_temp_table(node):
            if isinstance(node, UserSpecifiedDataNode):
                tmp_table_name = node.data._temp_table_name
                if tmp_table_name in self._temp_table_registered[dialect]:
                    return
                df = node.data.to_pandas()
                compute.register_temp_table_from_pandas(tmp_table_name, df)
                self._temp_table_registered[dialect].add(tmp_table_name)

        recurse_query_tree(
            qt_root,
            maybe_register_temp_table,
        )
