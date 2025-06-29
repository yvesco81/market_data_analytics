import duckdb
import shutil
from pathlib import Path
from logger import setup_logger

logger = setup_logger("stock_data.sync")

def sync_duckdb_to_evidence(
    source_path: Path = Path("data/stock_data.duckdb"),
    dest_path: Path = Path("evidence_dashboard/sources/stock_data/stock_data.duckdb")
) -> None:
    """Copy the DuckDB file into the Evidence sources directory and ensure metadata is present."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source DB file not found: {source_path}")

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, dest_path)
    logger.info(f"Copied DuckDB to Evidence: {dest_path}")

    # Optional: Ensure metadata table exists (if necessary)
    with duckdb.connect(str(dest_path)) as conn:
        conn.execute("PRAGMA show_tables")
        tables = [row[0] for row in conn.fetchall()]
        if "companies" not in tables:
            logger.warning("companies table not found in Evidence DB.")