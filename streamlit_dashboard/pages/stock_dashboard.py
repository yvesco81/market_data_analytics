import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
import duckdb
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'stock_data.duckdb'))

# Set page configuration
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# Title
st.title("📈 Stock Dashboard")

st.markdown("""
    This dashboard provides detailed insights into selected stock tickers. It includes:
    - Company metadata
    - Price trends
    - Volume patterns
    - Daily variation
    - Moving averages
    - High-low spread analysis

    Use the filters on the left to customize the view.
    """)


# Load tickers and date range from DuckDB
conn = duckdb.connect(db_path)

@st.cache_data
def get_tickers_and_date_range():
    tickers = conn.sql("SELECT DISTINCT CAST(ticker AS VARCHAR) AS ticker FROM stock_data.stocks ORDER BY ticker").df()["ticker"].tolist()
    dates = conn.sql("SELECT MIN(date) as min_date, MAX(date) as max_date FROM stock_data.stocks").fetchone()
    return tickers, dates[0], dates[1]

tickers, min_date, max_date = get_tickers_and_date_range()

# Sidebar filters
st.sidebar.title('Filters')
selected_ticker = st.sidebar.selectbox("Ticker", tickers, index=None, placeholder="Select a ticker")
# Date range selection
selected_range = st.sidebar.date_input(
    label="Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="date_range"
)
# Ensure the selected range is valid
if len(selected_range) != 2:
    st.warning("Please select a full start and end date range to view data.")
    st.stop()

start_date, end_date = selected_range

# Show Company Metadata
@st.cache_data
def get_company_info(ticker):
    query = f"""
    SELECT long_name as name, sector, industry, summary
    FROM companies
    WHERE ticker = '{ticker}'
    """
    return conn.sql(query).df()

company_info = get_company_info(selected_ticker)
if not company_info.empty:
    st.subheader("Company Information")
    st.markdown(f"**Name:** {company_info.iloc[0]['name']}")
    st.markdown(f"**Sector:** {company_info.iloc[0]['sector']}")
    st.markdown(f"**Industry:** {company_info.iloc[0]['industry']}")
    with st.expander("Description"):
        st.write(company_info.iloc[0]['summary'])


# Load stock price data for selection
@st.cache_data
def get_stock_data(ticker, start, end):
    query = f"""
    SELECT * FROM stock_data.stocks
    WHERE ticker = '{ticker}'
      AND date BETWEEN '{start}' AND '{end}'
    ORDER BY date
    """
    return conn.sql(query).df()

df = get_stock_data(selected_ticker, start_date, end_date)

# 30-Day Moving Average
@st.cache_data
def get_moving_avg_30(ticker, start, end):
    query = f"""
    SELECT
        date,
        close,
        AVG(close) OVER (ORDER BY date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS ma_30
    FROM stock_data.stocks
    WHERE ticker = '{ticker}'
      AND date BETWEEN '{start}' AND '{end}'
    ORDER BY date
    """
    return conn.sql(query).df()

# Daily High-Low Spread
@st.cache_data
def get_spread_data(ticker, start, end):
    query = f"""
    SELECT
        date,
        high - low AS spread
    FROM stock_data.stocks
    WHERE ticker = '{ticker}'
      AND date BETWEEN '{start}' AND '{end}'
    ORDER BY date
    """
    return conn.sql(query).df()

# Show basic info
# Calculate and show % Change
if len(df) >= 2:
    latest_close = df.iloc[-1]["close"]
    previous_close = df.iloc[-2]["close"]
    delta = (latest_close - previous_close) / previous_close * 100
    st.metric(label="Latest Close", value=f"${latest_close:.2f}", delta=f"{delta:.2f}%")

# Plotting section
# Display company metadata
col1, col2 = st.columns(2)

#ticker price
with col1:
    ticker_prices = df[['date', 'close']]
    ticker_prices['date'] = pd.to_datetime(ticker_prices['date'])
    fig_line = px.line(ticker_prices, x='date', y='close', title=f"{selected_ticker} Closing Prices")
    fig_line.update_layout(xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig_line, use_container_width=True)

# price_distribution
price_distribution = df[['close']].copy()
with col2:
    fig_hist = px.histogram(
        price_distribution,
        x='close',
        nbins=50,
        title=f"{selected_ticker} – Distribution of Closing Prices"
    )
    fig_hist.update_layout(
        xaxis_title='Closing Price (USD)',
        yaxis_title='Frequency',
        bargap=0.1
    )

    st.plotly_chart(fig_hist, use_container_width=True)

col3, col4 = st.columns(2)
# rolling_avg
with col3:
    rolling_avg = df[['date', 'close']].copy()
    rolling_avg['date'] = pd.to_datetime(rolling_avg['date'])
    rolling_avg['rolling_avg'] = rolling_avg['close'].rolling(window=7).mean()
    fig_roll = px.line(rolling_avg, x='date', y='rolling_avg', title=f"{selected_ticker} 7-Day Rolling Average")
    fig_roll.update_layout(xaxis_title='Date', yaxis_title='Avg Price (USD)')
    st.plotly_chart(fig_roll, use_container_width=True)

# 30-Day Moving Average
with col4:
    ma_30 = get_moving_avg_30(selected_ticker, start_date, end_date)
    ma_30['date'] = pd.to_datetime(ma_30['date'])
    fig_ma30 = px.line(ma_30, x='date', y='ma_30', title="30-Day Moving Average")
    fig_ma30.update_layout(xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig_ma30, use_container_width=True)


col5, col6 = st.columns(2)
# Volume vs Close (Price vs Volume)
with col5:
    volume_df = df[['date', 'close', 'volume']].copy()
    volume_df['volume_million'] = volume_df['volume'] / 1_000_000
    fig_vol = px.bar(volume_df, x='date', y='volume_million', title=f"{selected_ticker} Volume (in Millions)")
    fig_vol.add_scatter(x=volume_df['date'], y=volume_df['close'], mode='lines', name='Close Price', yaxis='y2')

    fig_vol.update_layout(
        yaxis=dict(title="Volume (M)"),
        yaxis2=dict(title="Close Price", overlaying="y", side="right"),
        xaxis_title="Date"
    )
    st.plotly_chart(fig_vol, use_container_width=True)

# Daily High-Low Spread
with col6:
    spread_data = get_spread_data(selected_ticker, start_date, end_date)
    spread_data['date'] = pd.to_datetime(spread_data['date'])
    fig_spread = px.line(spread_data, x='date', y='spread', title="Daily High-Low Spread")
    fig_spread.update_layout(xaxis_title='Date', yaxis_title='Spread (USD)')
    st.plotly_chart(fig_spread, use_container_width=True)



