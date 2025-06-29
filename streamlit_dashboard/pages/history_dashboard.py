import streamlit as st
import duckdb
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'stock_data.duckdb'))

# Set page configuration
st.set_page_config(page_title="Historical Dashboard", layout="wide")

# Title
st.title("📈 Historical Data")

st.markdown("""
    This table provides historical stock data for all selected tickers from the full dataset.
    It includes open, high, low, close prices and traded volume by day.
    Use the pagination controls below to explore the data.
    """)

@st.cache_data
def all_prices():
    with duckdb.connect(db_path) as conn:
        data = conn.sql("SELECT * FROM stock_data.stocks").df()
    return data

data = all_prices()
st.dataframe(data)