try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

try:
    __version__ = version("market_data_analytics")
except Exception as e:
    print(f"[stock_data] Could not determine version: {e}")
    __version__ = "0.0.0"