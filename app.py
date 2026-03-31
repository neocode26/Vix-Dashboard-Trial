import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# --- CONFIGURATION ---
API_KEY = 'YOUR_KEY_HERE'  # <--- PUT YOUR KEY HERE
SYMBOL = 'VIX'

st.set_page_config(page_title="Reliable VIX Tracker", layout="wide")

st.title("📊 VIX 'Fear Index' (Official API)")

def get_vix_data():
    # function=QUOTE gets the most recent real-time price
    # function=TIME_SERIES_DAILY gets the history
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        return None
        
    df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype(float).sort_index()
    return df

data = get_vix_data()

if data is not None:
    current_price = data['4. close'].iloc[-1]
    prev_price = data['4. close'].iloc[-2]
    delta = current_price - prev_price

    # Dashboard Layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("Current VIX", f"{current_price:.2f}", f"{delta:.2f}")
        st.write("---")
        st.write("**VIX Levels Guide:**")
        st.info("🟢 < 15: Low Stress\n\n🟡 20-30: Elevated\n\n🔴 > 40: Panic")

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['4. close'], fill='tozeroy', name='VIX'))
        fig.update_layout(title="Volatility Trend (Official Data)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.error("API Limit Reached or Invalid Key. The free tier allows 25 requests per day. Please check back in a bit!")
