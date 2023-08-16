import dataclasses
import typing
from abc import ABC
from abc import abstractmethod
from typing import Optional

import attrs
import pandas as pd
import pyarrow
import sqlparse

from tecton_core import conf
from tecton_core.query.executor_params import QueryTreeStagingLocation
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.sql_compat import Dialect


if typing.TYPE_CHECKING:
    import snowflake.snowpark
    from duckdb import DuckDBPyConnection


@dataclasses.dataclass
class StagingConfig:
    destination: QueryTreeStagingLocation
    sql_string: str
    table_name: str
    s3_path: Optional[str]
    num_partitions: Optional[int]


class QueryTreeCompute(ABC):
    """
    Base class for compute (e.g. DWH compute or Python compute) which can be
    used for different stages of executing the query tree.
    """

    @abstractmethod
    def get_dialect(self) -> Dialect:
        pass

    @abstractmethod
    def run_sql(self, sql_string: str, return_dataframe: bool = False) -> Optional[pyarrow.Table]:
        pass

    @abstractmethod
    def run_odfv(self, qt_node: NodeRef, input_df: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def register_temp_table(self, table_name: str, pa_table: pyarrow.Table) -> None:
        pass

    # TODO(danny): remove this once we convert connectors to return arrow tables instead of pandas dataframes
    @abstractmethod
    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def stage(self, staging_config: StagingConfig) -> Optional[pyarrow.Table]:
        pass


@attrs.frozen
class SnowflakeCompute(QueryTreeCompute):
    session: "snowflake.snowpark.Session"

    def run_sql(self, sql_string: str, return_dataframe: bool = False) -> Optional[pyarrow.Table]:
        if conf.get_bool("DUCKDB_DEBUG"):
            sql_string = sqlparse.format(sql_string, reindent=True)
            print(f"SNOWFLAKE QT: run SQL {sql_string}")
        snowpark_df = self.session.sql(sql_string)
        if return_dataframe:
            # TODO(TEC-16169): check types are converted properly
            df = self._to_pandas(snowpark_df)
            return pyarrow.Table.from_pandas(df)
        snowpark_df.collect()
        return None

    @staticmethod
    def _to_pandas(snowpark_df: "snowflake.snowpark.DataFrame") -> pd.DataFrame:
        """Converts a Snowpark DataFrame to a Pandas DataFrame while preserving types."""
        import snowflake.snowpark

        snowpark_schema = snowpark_df.schema
        df = snowpark_df.toPandas()

        for field in snowpark_schema:
            # TODO(TEC-16169): Handle other types.
            if field.datatype == snowflake.snowpark.types.LongType():
                df[field.name] = df[field.name].astype("int64")

        return df

    def get_dialect(self) -> Dialect:
        return Dialect.SNOWFLAKE

    def run_odfv(self, qt_node: NodeRef, input_df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pd.DataFrame) -> None:
        self.session.write_pandas(
            pandas_df,
            table_name=table_name,
            auto_create_table=True,
            table_type="temporary",
            quote_identifiers=True,
            overwrite=True,
        )

    def register_temp_table(self, table_name: str, pa_table: pyarrow.Table) -> None:
        self.register_temp_table_from_pandas(table_name, pa_table.to_pandas())

    def stage(self, staging_config: StagingConfig) -> Optional[pyarrow.Table]:
        if staging_config.destination == QueryTreeStagingLocation.MEMORY:
            df = self.run_sql(staging_config.sql_string, return_dataframe=True)
            return df

        if staging_config.destination == QueryTreeStagingLocation.S3:
            # TODO(danny): consider using pypika for this
            # TODO(danny): add temp credentials
            assert staging_config.s3_path
            final_sql = f"""
                COPY INTO '{staging_config.s3_path}'
                FROM ({staging_config.sql_string})
                CREDENTIALS = (
                    AWS_KEY_ID='{conf.get_or_none('AWS_ACCESS_KEY_ID')}'
                    AWS_SECRET_KEY='{conf.get_or_none('AWS_SECRET_ACCESS_KEY')}'
                )
                FILE_FORMAT = (TYPE=parquet) MAX_FILE_SIZE = 32000000
                HEADER = TRUE
            """
            # Note: doesn't include a separate PARTITION BY since that slows down this query significantly
            self.run_sql(final_sql)
        elif staging_config.destination == QueryTreeStagingLocation.DWH:
            final_sql = f"""
                CREATE OR REPLACE TEMPORARY TABLE {staging_config.table_name} AS
                ({staging_config.sql_string});
            """

            self.run_sql(final_sql)
        else:
            msg = f"Unexpected staging destination type: {staging_config.destination}"
            raise Exception(msg)

        # Only returns df if it's in memory
        return None


@attrs.frozen
class DuckDBCompute(QueryTreeCompute):
    session: "DuckDBPyConnection"

    def run_sql(self, sql_string: str, return_dataframe: bool = False) -> Optional[pyarrow.Table]:
        if conf.get_bool("DUCKDB_DEBUG"):
            sql_string = sqlparse.format(sql_string, reindent=True)
            print(f"DUCKDB: run SQL {sql_string}")
        duckdb_relation = self.session.sql(sql_string)
        if return_dataframe:
            return duckdb_relation.arrow()
        return None

    def get_dialect(self) -> Dialect:
        return Dialect.DUCKDB

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pd.DataFrame) -> None:
        self.run_sql(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM pandas_df")

    def register_temp_table(self, table_name: str, pa_table: pyarrow.Table) -> None:
        # NOTE: alternatively, can page through table + insert with SELECT *
        # FROM pa_table LIMIT 100000 OFFSET 100000*<step>. This doesn't seem
        # to offer any memory benefits and only slows down the insert.
        self.run_sql(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM pa_table")

    def run_odfv(self, qt_node: NodeRef, input_df: pd.DataFrame) -> pd.DataFrame:
        # TODO: leverage duckdb udfs
        pass

    def stage(self, staging_config: StagingConfig) -> Optional[pyarrow.Table]:
        create_table_sql = f"""
            CREATE TEMP TABLE {staging_config.table_name} AS ({staging_config.sql_string})
        """
        self.run_sql(create_table_sql)
        if staging_config.destination == QueryTreeStagingLocation.MEMORY:
            return self.run_sql(f"SELECT * FROM {staging_config.table_name}", return_dataframe=True)
        elif staging_config.destination == QueryTreeStagingLocation.S3:
            # TODO(danny): consider using pypika for this
            assert staging_config.s3_path
            final_sql = f"""
                LOAD httpfs;
                SET s3_region='us-west-2';
                SET s3_access_key_id='{conf.get_or_none('AWS_ACCESS_KEY_ID')}';
                SET s3_secret_access_key='{conf.get_or_none('AWS_SECRET_ACCESS_KEY')}';
                SET s3_session_token='{conf.get_or_none('AWS_SESSION_TOKEN')}';
                COPY {staging_config.table_name} TO '{staging_config.s3_path}' (FORMAT PARQUET, PER_THREAD_OUTPUT TRUE);
            """
        elif staging_config.destination == QueryTreeStagingLocation.DWH:
            final_sql = f"""
                CREATE OR REPLACE TEMPORARY TABLE {staging_config.table_name} AS
                ({staging_config.sql_string});
            """
        else:
            msg = f"Unexpected staging config type {staging_config.destination}"
            raise Exception(msg)

        # Only returns df if it's in memory
        self.run_sql(final_sql)
        return None


@attrs.frozen
class PandasCompute(QueryTreeCompute):
    def run_sql(self, sql_string: str, return_dataframe: bool = False) -> Optional[pyarrow.Table]:
        raise NotImplementedError

    def get_dialect(self) -> Dialect:
        return Dialect.PANDAS

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pd.DataFrame) -> None:
        raise NotImplementedError

    def register_temp_table(self, table_name: str, pa_table: pyarrow.Table) -> None:
        raise NotImplementedError

    def run_odfv(self, qt_node: NodeRef, input_df: pd.DataFrame) -> pd.DataFrame:
        from tecton_core.query.pandas.translate import pandas_convert_odfv_only

        pandas_node = pandas_convert_odfv_only(qt_node, input_df)
        return pandas_node.to_dataframe()

    def stage(self, staging_config: StagingConfig) -> Optional[pyarrow.Table]:
        raise NotImplementedError
