import argparse
import os
from flows.daily_etl import daily_etl_flow

def parse_args():
    parser = argparse.ArgumentParser(description="Run stock ETL flow with Prefect")
    parser.add_argument("--tickers", type=str, required=True)
    parser.add_argument("--start", type=str, required=True)
    parser.add_argument("--end", type=str, required=True)
    parser.add_argument("--db-path", type=str, default="data/stock_data.duckdb")
    parser.add_argument("--table", type=str, default="stocks")
    parser.add_argument("--mode", type=str, choices=["overwrite", "append"], default="overwrite")
    return parser.parse_args()

if __name__ == "__main__":
    # ✅ Disable Prefect client via env var before Prefect tries to connect
    os.environ["PREFECT_API_ENABLE_CLIENT"] = "false"

    args = parse_args()
    tickers = [t.strip() for t in args.tickers.split(",")]

    daily_etl_flow(
        tickers=tickers,
        start=args.start,
        end=args.end,
        db_path=args.db_path,
        table_name=args.table,
        mode=args.mode
    )
