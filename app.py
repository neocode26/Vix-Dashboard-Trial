import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="VIX Real-Time Tracker", layout="wide")

st.title("📉 VIX 'Fear Index' Dashboard")
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Fetch VIX data from Yahoo Finance
@st.cache_data(ttl=300)  # Refreshes every 5 minutes
def load_data():
    vix = yf.Ticker("^VIX")
    df = vix.history(period="1mo", interval="1d")
    return df, vix.info

try:
    data, info = load_data()
    current_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    change = current_price - prev_price

    # Top Metric Tiles
    col1, col2, col3 = st.columns(3)
    col1.metric("VIX Index", f"{current_price:.2f}", f"{change:.2f}")
    col2.metric("Day High", f"{data['High'].iloc[-1]:.2f}")
    col3.metric("52-Week Range", f"{info.get('fiftyTwoWeekLow', 0):.2f} - {info.get('fiftyTwoWeekHigh', 0):.2f}")

    # Charting
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'])])
    
    fig.update_layout(title="VIX Price Action (Last 30 Days)", template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error("Market data is currently unavailable. Please try again later.")
