import streamlit as st

st.set_page_config(
    page_title="index",
    page_icon="👋",
)

st.write("# Welcome to Stock Market App! 👋")
st.markdown(
    """
    This is a simple stock market app that allows you to explore stock data and visualize it.

    ## Features
    - View historical stock data
    - Visualize stock prices
    - Compare multiple stocks

    ## Get Started
    Use the sidebar to navigate through the app.

    ## About
    This app is built with Streamlit and uses DuckDB for data storage.
    """
)
