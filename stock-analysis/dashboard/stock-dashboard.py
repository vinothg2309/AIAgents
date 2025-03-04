import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(layout="wide", page_title="Stock Dashboard")

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: white;
    }
    .stApp {
        background-color: #121212;
    }
    .stSelectbox, .stSelectbox > div > div {
        background-color: #1E1E1E;
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: white;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .highlight-block {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: white;
    }
    .red-text {
        color: #FF5252;
    }
    .green-text {
        color: #69F0AE;
    }
    h1, h2, h3, p {
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4F4F4F;
    }
    div[data-testid="stDecoration"] {
        background-image: linear-gradient(to bottom, #1E1E1E, #121212);
    }
    .current-price {
        font-size: 36px;
        font-weight: bold;
        margin: 0;
        padding: 0;
        color: white;
    }
    .stHeading{
        color: white;
    }
    .price-change {
        font-size: 16px;
        margin: 0;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)


# Function to get company name
def get_company_name(ticker):
    ticker_to_name = {
        "MSFT": "Microsoft Corporation",
        "AAPL": "Apple Inc.",
        "GOOGL": "Alphabet Inc.",
        "AMZN": "Amazon.com, Inc.",
        "META": "Meta Platforms, Inc."
    }
    return ticker_to_name.get(ticker, ticker)


# Function to load stock data
@st.cache_data(ttl=300)
def load_stock_data(ticker, period="1mo", interval="1d"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        info = stock.info
        return hist, info
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Provide empty DataFrame with expected columns as fallback
        return pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume']), {}


# Sidebar
with st.sidebar:
    st.markdown('<div style="color: white;">Home</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding: 1px; background-color: #333333;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="color: white;">Earnings</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding: 1px; background-color: #333333;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="color: white; margin-top: 30px; font-weight: bold;">Choose your filter:</div>',
                unsafe_allow_html=True)

    # Ticker selection
    st.markdown('<div style="color: white; margin-top: 10px;">Choose Ticker</div>', unsafe_allow_html=True)

    # Create a container with custom styling for the dropdown
    ticker_container = st.container()
    with ticker_container:
        ticker_options = ["MSFT", "AAPL", "GOOGL", "AMZN", "META"]
        selected_ticker = st.selectbox("", ticker_options, index=0, label_visibility="collapsed")

    # Period selection
    st.markdown('<div style="color: white; margin-top: 10px;">Select Period</div>', unsafe_allow_html=True)

    period_container = st.container()
    with period_container:
        period_options = ["1mo", "3mo", "6mo", "1y", "ytd", "max"]
        selected_period = st.selectbox("", period_options, index=0, label_visibility="collapsed")

# Main panel
st.title(f"{get_company_name(selected_ticker)} ({selected_ticker})")
st.markdown('<div style="padding: 1px; background-color: #333333; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

# Get stock data and info
stock_data, stock_info = load_stock_data(selected_ticker, period=selected_period)

# Handle empty data
if stock_data.empty:
    st.error("No data available for the selected ticker and period.")
    st.stop()

# Current price and change
current_price = stock_data['Close'].iloc[-1]
previous_close = stock_data['Close'].iloc[-2] if len(stock_data) > 1 else current_price
price_change = current_price - previous_close
price_change_percent = (price_change / previous_close) * 100 if previous_close > 0 else 0

# Display current price
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown('<div style="color: white; font-size: 18px; margin-bottom: 5px;">Current</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="current-price">{current_price:.2f}</div>', unsafe_allow_html=True)

    if price_change < 0:
        st.markdown(
            f'<div class="price-change red-text">▼ {abs(price_change):.2f} ({abs(price_change_percent):.2f}%)</div>',
            unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="price-change green-text">▲ {price_change:.2f} ({price_change_percent:.2f}%)</div>',
                    unsafe_allow_html=True)

# Create layout with columns for stock information
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Previous Close</span><br><b>{previous_close:.2f}</b></div>',
        unsafe_allow_html=True)

with col2:
    open_price = stock_data['Open'].iloc[-1]
    st.markdown(f'<div class="highlight-block"><span style="color: #888;">Open</span><br><b>{open_price:.2f}</b></div>',
                unsafe_allow_html=True)

with col3:
    day_low = stock_data['Low'].iloc[-1]
    day_high = stock_data['High'].iloc[-1]
    day_range = f"{day_low:.2f} - {day_high:.2f}"
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Day\'s Range</span><br><b>{day_range}</b></div>',
        unsafe_allow_html=True)

with col4:
    # Get 52-week range from available data or approximate
    week_52_low = stock_data['Low'].min()
    week_52_high = stock_data['High'].max()
    week_range = f"{week_52_low:.2f} - {week_52_high:.2f}"
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">52-Week Range</span><br><b>{week_range}</b></div>',
        unsafe_allow_html=True)

# Additional metrics (get from info when available, otherwise use reasonable defaults)
col1, col2, col3, col4 = st.columns(4)

with col1:
    eps = stock_info.get('trailingEPS', 9.69)
    st.markdown(f'<div class="highlight-block"><span style="color: #888;">EPS (TTM)</span><br><b>{eps}</b></div>',
                unsafe_allow_html=True)

with col2:
    div_yield = stock_info.get('dividendYield', 0.0082) * 100
    div_rate = stock_info.get('dividendRate', 2.72)
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Fwd Div & Yield</span><br><b>{div_rate:.2f} ({div_yield:.2f}%)</b></div>',
        unsafe_allow_html=True)

with col3:
    pe_ratio = stock_info.get('trailingPE', 34.35)
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">PE Ratio (TTM)</span><br><b>{pe_ratio:.2f}</b></div>',
        unsafe_allow_html=True)

with col4:
    volume = stock_data['Volume'].iloc[-1]
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Volume</span><br><b>{int(volume):,}</b></div>',
        unsafe_allow_html=True)

# Bid, Ask, Volume, Average
col1, col2, col3, col4 = st.columns(4)

with col1:
    bid = stock_info.get('bid', 0.0)
    bid_size = stock_info.get('bidSize', 1200)
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Bid</span><br><b>{bid:.2f} x {bid_size}</b></div>',
        unsafe_allow_html=True)

with col2:
    ask = stock_info.get('ask', 0.0)
    ask_size = stock_info.get('askSize', 2200)
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Ask</span><br><b>{ask:.2f} x {ask_size}</b></div>',
        unsafe_allow_html=True)

with col3:
    avg_volume = stock_info.get('averageVolume', int(stock_data['Volume'].mean()))
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Average Volume</span><br><b>{int(avg_volume):,}</b></div>',
        unsafe_allow_html=True)

with col4:
    # Calculate 50-day moving average
    fifty_day_avg = stock_info.get('fiftyDayAverage',
                                   stock_data['Close'].rolling(window=min(50, len(stock_data))).mean().iloc[-1])
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">50-Day Average</span><br><b>{fifty_day_avg:.2f}</b></div>',
        unsafe_allow_html=True)

# Beta, Market Cap, 200-Day Average
col1, col2, col3, col4 = st.columns(4)

with col1:
    beta = stock_info.get('beta', 0.90)
    st.markdown(f'<div class="highlight-block"><span style="color: #888;">Beta</span><br><b>{beta:.2f}</b></div>',
                unsafe_allow_html=True)

with col2:
    market_cap = stock_info.get('marketCap', 2470000000000) / 1000000000000  # Convert to trillions
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">Market Cap</span><br><b>{market_cap:.2f}T</b></div>',
        unsafe_allow_html=True)

with col3:
    two_hundred_day_avg = stock_info.get('twoHundredDayAverage',
                                         stock_data['Close'].rolling(window=min(200, len(stock_data))).mean().iloc[-1])
    st.markdown(
        f'<div class="highlight-block"><span style="color: #888;">200-Day Average</span><br><b>{two_hundred_day_avg:.2f}</b></div>',
        unsafe_allow_html=True)

# Chart
st.markdown(
    '<div style="color: white; font-size: 18px; margin-top: 20px; margin-bottom: 10px;">Price, MA and Volume</div>',
    unsafe_allow_html=True)

# Calculate moving averages for the chart
stock_data['SMA50'] = stock_data['Close'].rolling(window=min(50, len(stock_data))).mean()
stock_data['SMA200'] = stock_data['Close'].rolling(window=min(200, len(stock_data))).mean()

# Fill NaN values that occur at the beginning of the moving averages
stock_data.fillna(method='bfill', inplace=True)

# Create subplot with shared x-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05,
                    row_heights=[0.7, 0.3])

# Add price line
fig.add_trace(go.Scatter(
    x=stock_data.index,
    y=stock_data['Close'],
    name="Price",
    line=dict(color="#00BFFF", width=2)
), row=1, col=1)

# Add SMA-50
fig.add_trace(go.Scatter(
    x=stock_data.index,
    y=stock_data['SMA50'],
    name="SMA-50",
    line=dict(color="#FF007F", width=1.5)
), row=1, col=1)

# Add SMA-200
fig.add_trace(go.Scatter(
    x=stock_data.index,
    y=stock_data['SMA200'],
    name="SMA-200",
    line=dict(color="#FFA500", width=1.5)
), row=1, col=1)

# Create alternating colors for volume bars
volume_colors = []
for i in range(len(stock_data)):
    if i > 0 and stock_data['Close'].iloc[i] > stock_data['Close'].iloc[i - 1]:
        volume_colors.append('#4CAF50')  # Green
    else:
        volume_colors.append('#F44336')  # Red

# Add volume bars
fig.add_trace(go.Bar(
    x=stock_data.index,
    y=stock_data['Volume'],
    name="Volume",
    marker_color=volume_colors
), row=2, col=1)

# Update layout
fig.update_layout(
    height=500,
    template="plotly_dark",
    plot_bgcolor="#121212",
    paper_bgcolor="#121212",
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_rangeslider_visible=False,
)

# Y-axis titles
fig.update_yaxes(title_text="Price ($)", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

# Update layout
fig.update_layout(
    font=dict(color='blue', size=15)
)

st.plotly_chart(fig, use_container_width=True)