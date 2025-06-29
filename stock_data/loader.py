import duckdb
import pandas as pd
from pathlib import Path
from logger import setup_logger, log_exceptions


logger = setup_logger(__name__)


@log_exceptions(logger)
def load_prices_to_duckdb(df: pd.DataFrame, db_path: str, table_name: str = "stocks", mode: str = "overwrite") -> None:
    """Load OHLCV stock data into DuckDB."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(db_path)

    if mode == "overwrite":
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    elif mode == "append":
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        raise ValueError("Mode must be 'overwrite' or 'append'.")

    conn.close()
    logger.info(f"[{table_name}] Prices loaded to '{db_path}' in {mode} mode.")


@log_exceptions(logger)
def load_metadata_to_duckdb(metadata_df: pd.DataFrame, db_path: str, table_name: str = "companies", mode: str = "overwrite") -> None:
    """Load company metadata into DuckDB."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(db_path)

    if mode == "overwrite":
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM metadata_df")
    elif mode == "append":
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM metadata_df")
    else:
        raise ValueError("Mode must be 'overwrite' or 'append'.")

    conn.close()
    logger.info(f"[{table_name}] Metadata loaded to '{db_path}' in {mode} mode.")
