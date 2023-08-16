import logging
import typing

from tecton_core import conf


if typing.TYPE_CHECKING:
    from duckdb import DuckDBPyConnection
logger = logging.getLogger(__name__)


class DuckDBContext:
    """
    Singleton holder of DuckDB connection.
    """

    _current_context_instance = None
    _connection = None

    def __init__(self, connection: "DuckDBPyConnection") -> None:
        self._connection = connection
        # Needed to export to S3
        connection.sql("INSTALL httpfs;")
        duckdb_memory_limit = conf.get_or_none("DUCKDB_MEMORY_LIMIT")
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"Setting duckdb memory limit to {duckdb_memory_limit}")
        connection.sql(f"SET memory_limit='{duckdb_memory_limit}'")
        num_duckdb_threads = conf.get_or_none("DUCKDB_NTHREADS")
        if num_duckdb_threads:
            connection.sql(f"SET threads TO {num_duckdb_threads};")
            if conf.get_bool("DUCKDB_DEBUG"):
                print(f"Setting duckdb threads to {num_duckdb_threads}")

    def get_connection(self):
        return self._connection

    @classmethod
    def get_instance(cls) -> "DuckDBContext":
        """
        Get the singleton instance of DuckDBContext.
        """
        if cls._current_context_instance is None:
            import duckdb

            if conf.get_bool("DUCKDB_PERSIST_DB"):
                conn = duckdb.connect("duckdb.db")
            else:
                conn = duckdb.connect()

            cls._current_context_instance = cls(conn)

        return cls._current_context_instance

    @classmethod
    def cleanup_instance(cls):
        if cls._current_context_instance:
            cls._current_context_instance.get_connection().close()

        cls._current_context_instance = None
