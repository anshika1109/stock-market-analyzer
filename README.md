# 📈 Stock Market Real-Time Analyzer with News Sentiment Analysis

A comprehensive Python tool for fetching and analyzing real-time stock market data from multiple public APIs, with integrated news sentiment analysis to understand how news impacts stock prices. Features include a command-line interface, web dashboards, and an MCP (Model Context Protocol) server for AI assistant integration.

## ✨ Features

- **Multi-Source Data Fetching**: Get stock data from Yahoo Finance, Alpha Vantage, and Finnhub
- **News Sentiment Analysis**: Analyze news articles and their impact on stock prices
- **News-Price Correlation**: Understand if news sentiment aligns with price movements
- **Real-Time Analysis**: Compare prices and news across different sources
- **Multiple Interfaces**:
  - Command-line tool for stocks and news
  - Web dashboard (Flask)
  - Standalone HTML dashboard
  - Streamlit dashboard
  - MCP server for AI assistants (Claude, Kiro)
- **Comprehensive Data**: Price, change, volume, market cap, day high/low, news sentiment, and more
- **Easy Integration**: Works with Claude Desktop and other MCP-compatible clients

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stock-market-analyzer.git
cd stock-market-analyzer

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

**Stock Prices (Command Line):**
```bash
python main.py AAPL GOOGL MSFT
```

**News Analysis (Command Line):**
```bash
# Get recent news
python news_cli.py AAPL

# Analyze sentiment
python news_cli.py AAPL sentiment

# Correlate news with price movement
python news_cli.py AAPL correlate

# Get news summary
python news_cli.py AAPL summary
```

**Standalone Dashboard:**
```bash
open standalone_dashboard.html
```

**Web Dashboard:**
```bash
python web_dashboard.py
# Open http://127.0.0.1:8080
```

## 🔑 API Keys (Optional)

Yahoo Finance works without API keys. For additional sources:

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - [Alpha Vantage](https://www.alphavantage.co/support/#api-key) - Free tier: 25 requests/day
   - [Finnhub](https://finnhub.io/register) - Free tier available

```bash
cp .env.example .env
# Edit .env and add your keys
```

## 🤖 MCP Server Integration

Use this tool with AI assistants like Claude Desktop or Kiro.

### Setup for Claude Desktop

1. Run the setup script:
```bash
./setup_claude_desktop.sh
```

2. Restart Claude Desktop

3. Ask Claude: "Get the stock price for AAPL"
4. Ask Claude: "Analyze news sentiment for TSLA"
5. Ask Claude: "Why did AAPL stock go up today?"

See [CLAUDE_DESKTOP_SETUP.md](CLAUDE_DESKTOP_SETUP.md) for detailed instructions.

### Setup for Kiro

The MCP server is pre-configured in `.kiro/settings/mcp.json`. Just restart Kiro and ask:
- "Get the stock price for AAPL"
- "Compare TSLA across all sources"
- "What's the news sentiment for NVDA?"
- "Why did GOOGL stock drop today?"

## 📊 Available Tools

### Command Line - Stock Prices
```bash
# Single stock
python main.py AAPL

# Multiple stocks
python main.py AAPL GOOGL MSFT TSLA

# Interactive mode
python main.py
```

### Command Line - News Analysis
```bash
# Get recent news articles
python news_cli.py AAPL news

# Analyze overall sentiment
python news_cli.py AAPL sentiment

# Correlate news with price movement
python news_cli.py AAPL correlate

# Get formatted summary
python news_cli.py AAPL summary
```

### MCP Server Tools

When integrated with AI assistants, you get access to:

**Stock Data:**
1. **get_stock_quote** - Get quote from specific sources
2. **compare_stock_sources** - Compare data across all sources
3. **get_best_quote** - Get most reliable quote
4. **get_multiple_quotes** - Get quotes for multiple symbols

**News Analysis:**
5. **get_stock_news** - Get recent news articles
6. **analyze_news_sentiment** - Analyze overall sentiment
7. **correlate_news_with_price** - Correlate news with price movement
8. **get_news_summary** - Get formatted news summary

## 🏗️ Project Structure

```
.
├── analyzer.py              # Core stock analysis logic
├── news_analyzer.py         # News sentiment analysis
├── data_sources.py          # Stock API integrations
├── news_sources.py          # News API integrations
├── config.py                # Configuration management
├── main.py                  # CLI interface for stocks
├── news_cli.py              # CLI interface for news
├── mcp_server.py            # MCP server for AI integration
├── web_dashboard.py         # Flask web server
├── dashboard.py             # Streamlit dashboard
├── standalone_dashboard.html # Browser-only version
├── templates/
│   └── index.html           # Web dashboard UI
├── .kiro/settings/
│   └── mcp.json             # Kiro MCP configuration
└── requirements.txt         # Python dependencies
```

## 📖 Documentation

- [MCP Setup Guide](MCP_SETUP.md) - Detailed MCP server configuration
- [Claude Desktop Setup](CLAUDE_DESKTOP_SETUP.md) - Claude Desktop integration
- [Workflow Diagram](WORKFLOW_DIAGRAM.md) - Complete data flow explanation
- [Quick Start Guide](QUICK_START.md) - Getting started quickly

## 🔧 Requirements

- Python 3.9+
- Internet connection for API access
- Optional: API keys for Alpha Vantage and Finnhub

## 📦 Dependencies

- `requests` - HTTP requests
- `pandas` - Data manipulation
- `yfinance` - Yahoo Finance API
- `python-dotenv` - Environment variables
- `flask` - Web dashboard (optional)
- `streamlit` - Streamlit dashboard (optional)
- `mcp` - Model Context Protocol server

## 🎯 Use Cases

- **Real-time stock monitoring** - Track multiple stocks simultaneously
- **Price comparison** - Verify prices across different data sources
- **News sentiment analysis** - Understand market sentiment from news
- **News-price correlation** - See if news explains price movements
- **AI assistant integration** - Ask AI for stock data and news analysis in natural language
- **Data analysis** - Export data for further analysis
- **Portfolio tracking** - Monitor your investments with news context

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) - Primary data source
- [Alpha Vantage](https://www.alphavantage.co/) - Financial data API
- [Finnhub](https://finnhub.io/) - Stock market data
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI integration standard

## 📧 Contact

For questions or support, please open an issue on GitHub.

## ⚠️ Disclaimer

This tool is for informational purposes only. Stock market data may be delayed. Always verify information before making investment decisions. Not financial advice.

---

Made with ❤️ for stock market enthusiasts and AI developers
