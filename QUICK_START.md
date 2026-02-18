# Stock Market Analyzer - Quick Start Guide

## ✅ What You Have

Your stock market analyzer tool is complete with:

1. **Core Analyzer** (`analyzer.py`, `data_sources.py`)
   - Fetches real-time stock data from Yahoo Finance, Alpha Vantage, and Finnhub
   - Compares data across sources
   - Returns best available quote

2. **Command Line Interface** (`main.py`)
   - Run: `python main.py AAPL TSLA GOOGL`
   - Interactive mode with prompts

3. **Web Dashboard** (`web_dashboard.py` + `templates/index.html`)
   - Beautiful UI with real-time updates
   - Run: `python web_dashboard.py`
   - Access: http://127.0.0.1:8080

4. **Standalone HTML** (`standalone_dashboard.html`)
   - No server needed, works in browser
   - Just open the file in your browser

5. **MCP Server** (`mcp_server.py`)
   - Allows AI assistants to use your tool
   - Configuration in `.kiro/settings/mcp.json`

## 🚀 Quick Start

### Option 1: Command Line (Simplest)
```bash
python main.py AAPL
```

### Option 2: Standalone Dashboard (No Server)
```bash
open standalone_dashboard.html
```

### Option 3: Web Dashboard (Full Features)
```bash
python web_dashboard.py
# Then open: http://127.0.0.1:8080
```

### Option 4: MCP Server (For AI Integration)
The MCP server is configured and ready. Just restart Kiro and ask:
- "Get the stock price for AAPL"
- "Compare TSLA across all sources"

## 📋 Available MCP Tools

Once Kiro loads the MCP server, you'll have access to:

1. **get_stock_quote** - Get quote from specific sources
2. **compare_stock_sources** - Compare all sources
3. **get_best_quote** - Get most reliable quote  
4. **get_multiple_quotes** - Get multiple stocks at once

## 🔑 API Keys (Optional)

Yahoo Finance works without API keys. For additional sources:

1. Copy `.env.example` to `.env`
2. Add your API keys:
   - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   - Finnhub: https://finnhub.io/register

## 🧪 Testing

Test the analyzer:
```bash
python main.py AAPL
```

Test the web dashboard:
```bash
python web_dashboard.py
```

Test MCP server (in Kiro):
Just ask: "Get the current price of AAPL"

## 📁 Project Structure

```
.
├── analyzer.py              # Core analysis logic
├── data_sources.py          # API integrations
├── config.py                # Configuration
├── main.py                  # CLI interface
├── web_dashboard.py         # Flask web server
├── standalone_dashboard.html # Browser-only version
├── mcp_server.py            # MCP server for AI
├── templates/
│   └── index.html           # Web dashboard UI
├── .kiro/settings/
│   └── mcp.json             # MCP configuration
├── .env                     # API keys (create from .env.example)
└── requirements.txt         # Dependencies
```

## 🐛 Troubleshooting

### Dependency Issues
Your conda environment has conflicts. Use a virtual environment:
```bash
python -m venv stock_env
source stock_env/bin/activate
pip install -r requirements.txt
```

### Web Dashboard 403 Error
Try the standalone HTML version instead:
```bash
open standalone_dashboard.html
```

### MCP Server Not Working
1. Check Kiro's MCP Server view (Command Palette → "View MCP Servers")
2. Try reconnecting the server
3. Check that paths in `.kiro/settings/mcp.json` are correct

## 💡 Next Steps

1. Add your API keys to `.env` for multi-source data
2. Customize data sources in `data_sources.py`
3. Extend the analyzer with new features
4. Create custom visualizations in the dashboard

## 🎯 Example Usage in Kiro

Once the MCP server is loaded, you can ask:

- "What's the current price of Apple stock?"
- "Compare Tesla stock data from all sources"
- "Get quotes for AAPL, GOOGL, MSFT, and NVDA"
- "Show me the best available quote for Amazon"

The AI will automatically use your MCP server to fetch real-time data!
