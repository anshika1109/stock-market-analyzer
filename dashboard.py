import streamlit as st
import plotly.graph_objects as go
from analyzer import StockAnalyzer
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Stock Market Analyzer",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize analyzer
@st.cache_resource
def get_analyzer():
    return StockAnalyzer()

analyzer = get_analyzer()

# Header
st.title("📈 Stock Market Real-Time Analyzer")
st.markdown("Compare real-time stock data from multiple sources")

# Sidebar
st.sidebar.header("Settings")
symbols_input = st.sidebar.text_input(
    "Enter Stock Symbols (comma-separated)",
    value="AAPL,GOOGL,MSFT",
    help="Example: AAPL,TSLA,NVDA"
)

symbols = [s.strip().upper() for s in symbols_input.split(',') if s.strip()]

# Source selection
st.sidebar.subheader("Data Sources")
use_yahoo = st.sidebar.checkbox("Yahoo Finance", value=True)
use_alphavantage = st.sidebar.checkbox("Alpha Vantage", value=True)
use_finnhub = st.sidebar.checkbox("Finnhub", value=True)

sources = []
if use_yahoo:
    sources.append('yahoo')
if use_alphavantage:
    sources.append('alphavantage')
if use_finnhub:
    sources.append('finnhub')

# Refresh button
if st.sidebar.button("🔄 Refresh Data", type="primary"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main content
if not symbols:
    st.warning("Please enter at least one stock symbol")
else:
    for symbol in symbols:
        st.markdown(f"## {symbol}")
        
        # Get data from all sources
        results = analyzer.get_quote(symbol, sources=sources)
        
        # Create columns for metrics
        cols = st.columns(len(sources))
        
        for idx, (source_name, quote) in enumerate(results.items()):
            with cols[idx]:
                if 'error' in quote:
                    st.error(f"**{source_name.upper()}**\n\n❌ {quote['error']}")
                else:
                    price = quote.get('price', 'N/A')
                    change = quote.get('change', 0)
                    change_pct = quote.get('change_percent', 0)
                    
                    # Determine color based on change
                    if isinstance(change, (int, float)) and change > 0:
                        delta_color = "normal"
                        arrow = "📈"
                    elif isinstance(change, (int, float)) and change < 0:
                        delta_color = "inverse"
                        arrow = "📉"
                    else:
                        delta_color = "off"
                        arrow = "➡️"
                    
                    st.metric(
                        label=f"{arrow} {source_name.upper()}",
                        value=f"${price:.2f}" if isinstance(price, (int, float)) else price,
                        delta=f"{change:.2f} ({change_pct:.2f}%)" if isinstance(change, (int, float)) else None,
                        delta_color=delta_color
                    )
                    
                    if 'volume' in quote and quote['volume']:
                        st.caption(f"Volume: {quote['volume']:,}")
        
        # Comparison table
        st.subheader("📊 Source Comparison")
        df = analyzer.compare_sources(symbol)
        
        if not df.empty:
            # Style the dataframe
            st.dataframe(
                df.style.format({
                    'Price': '${:.2f}',
                    'Change': '{:.2f}',
                    'Change %': '{:.2f}%',
                    'Volume': '{:,.0f}'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Price comparison chart
            if len(df) > 1:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df['Source'],
                    y=df['Price'],
                    text=df['Price'].apply(lambda x: f'${x:.2f}'),
                    textposition='auto',
                    marker_color='lightblue'
                ))
                fig.update_layout(
                    title=f"{symbol} - Price Comparison Across Sources",
                    xaxis_title="Source",
                    yaxis_title="Price ($)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available from any source")
        
        st.markdown("---")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**API Keys Required:**
- Alpha Vantage: [Get Key](https://www.alphavantage.co/support/#api-key)
- Finnhub: [Get Key](https://finnhub.io/register)
- Yahoo Finance: No key needed ✅
""")
