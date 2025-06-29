import yfinance as yf
import pandas as pd
from typing import List, Tuple
from logger import setup_logger, log_exceptions

logger = setup_logger(__name__)

@log_exceptions(logger)
def fetch_stock_data(tickers: List[str], start: str, end: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetch historical stock prices and metadata for tickers.

    Returns:
        - prices_df: OHLCV data with 'ticker' column
        - metadata_df: stock info like name, sector, etc.
    """
    price_data = []
    metadata = []

    for ticker in tickers:
        try:
            logger.info(f"Fetching data for {ticker}")
            df = yf.download(ticker, start=start, end=end)
            df.reset_index(inplace=True)
            df["ticker"] = ticker
            df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in df.columns]
            df["date"] = pd.to_datetime(df["date"]).dt.date
            price_data.append(df)

            stock = yf.Ticker(ticker)
            info = stock.info
            metadata.append({
                "ticker": ticker,
                "long_name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "summary": info.get("longBusinessSummary")
            })
        except Exception as e:
            logger.error(f"Failed to fetch data for {ticker}: {e}")

    prices_df = pd.concat(price_data, ignore_index=True) if price_data else pd.DataFrame()
    metadata_df = pd.DataFrame(metadata)

    return prices_df, metadata_df
