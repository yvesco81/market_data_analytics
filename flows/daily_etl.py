from prefect import flow, task
from stock_data.extractor import fetch_stock_data
from stock_data.loader import load_prices_to_duckdb, load_metadata_to_duckdb
from stock_data.utils import sync_duckdb_to_evidence
from logger import setup_logger
from typing import List
import pandas as pd

logger = setup_logger("flows.daily_etl")

@task
def extract(tickers: List[str], start: str, end: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    logger.info("Starting data extraction...")
    return fetch_stock_data(tickers, start, end)

@task
def load_prices(df: pd.DataFrame, db_path: str, table_name: str, mode: str):
    logger.info("Loading price data...")
    load_prices_to_duckdb(df, db_path, table_name, mode)

@task
def load_metadata(df: pd.DataFrame, db_path: str, table_name: str, mode: str):
    logger.info("Loading metadata...")
    load_metadata_to_duckdb(df, db_path, table_name, mode)

@task
def sync_to_evidence():
    logger.info("Syncing to Evidence dashboard...")
    sync_duckdb_to_evidence()

@flow(name="daily_stock_etl")
def daily_etl_flow(tickers: List[str], start: str, end: str, db_path: str, table_name: str = "stocks", mode: str = "overwrite"):
    logger.info("ETL flow started")

    prices_df, metadata_df = extract(tickers, start, end)

    if not prices_df.empty:
        load_prices(prices_df, db_path, table_name, mode)

    if not metadata_df.empty:
        load_metadata(metadata_df, db_path, "companies", mode)

    sync_to_evidence()

    logger.info("ETL flow completed")
