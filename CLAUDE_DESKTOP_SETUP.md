# Using Stock Market Analyzer MCP Server with Claude Desktop

## What is This?

Your stock market analyzer is now an MCP server that Claude Desktop can use to fetch real-time stock data during conversations.

## Setup for Claude Desktop

### Step 1: Locate Claude Desktop Config File

The configuration file location depends on your OS:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Edit the Configuration

Open the config file and add your MCP server:

```json
{
  "mcpServers": {
    "stock-market-analyzer": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["/Users/anshikagupta/Sementic_analysis/mcp_server.py"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "78XX5FJBIUZP6NVG",
        "FINNHUB_API_KEY": "d6adai9r01qqjvbq1mbgd6adai9r01qqjvbq1mc0"
      }
    }
  }
}
```

**Important:** 
- Use the FULL absolute path to `mcp_server.py`
- Use the correct Python path (run `which python3` to find yours)
- If you already have other MCP servers configured, just add this one to the existing `mcpServers` object

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop completely for the changes to take effect.

### Step 4: Verify It's Working

In Claude Desktop, you should see a small 🔨 (hammer) icon or MCP indicator. Click it to see available tools.

You should see:
- get_stock_quote
- compare_stock_sources
- get_best_quote
- get_multiple_quotes

## Using the MCP Server in Claude Desktop

Once configured, just ask Claude naturally:

**Examples:**
- "What's the current price of Apple stock?"
- "Get me the stock price for TSLA"
- "Compare AAPL data from all sources"
- "Get quotes for AAPL, GOOGL, MSFT, and NVDA"
- "What's Tesla trading at right now?"

Claude will automatically use your MCP server to fetch real-time data!

## Example Configuration with Multiple Servers

If you already have other MCP servers, your config might look like this:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "stock-market-analyzer": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["/Users/anshikagupta/Sementic_analysis/mcp_server.py"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "78XX5FJBIUZP6NVG",
        "FINNHUB_API_KEY": "d6adai9r01qqjvbq1mbgd6adai9r01qqjvbq1mc0"
      }
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key"
      }
    }
  }
}
```

## Quick Setup Script

Run this to quickly add the configuration:

```bash
# Backup existing config
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json.backup

# Create or update config (macOS)
cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "stock-market-analyzer": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["/Users/anshikagupta/Sementic_analysis/mcp_server.py"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "78XX5FJBIUZP6NVG",
        "FINNHUB_API_KEY": "d6adai9r01qqjvbq1mbgd6adai9r01qqjvbq1mc0"
      }
    }
  }
}
EOF

echo "✅ Configuration added! Restart Claude Desktop."
```

## Troubleshooting

### MCP Server Not Showing Up

1. **Check the config file path** - Make sure you edited the right file
2. **Verify JSON syntax** - Use a JSON validator to check for syntax errors
3. **Check Python path** - Run `which python3` and use that exact path
4. **Check file path** - Use absolute path to `mcp_server.py`
5. **Restart Claude Desktop** - Completely quit and reopen

### "Connection Failed" Error

1. **Test the server manually:**
   ```bash
   /opt/homebrew/bin/python3 /Users/anshikagupta/Sementic_analysis/mcp_server.py
   ```
   
2. **Check dependencies:**
   ```bash
   /opt/homebrew/bin/python3 -c "import mcp, yfinance, pandas; print('All OK')"
   ```

3. **Check permissions:**
   ```bash
   chmod +x /Users/anshikagupta/Sementic_analysis/mcp_server.py
   ```

### No Data Returned

1. **Check API keys** - Verify they're correct in the config
2. **Check internet connection**
3. **Alpha Vantage rate limit** - Free tier has 25 requests/day limit
4. **Test directly:**
   ```bash
   python3 main.py AAPL
   ```

## Features Available in Claude Desktop

Once configured, Claude can:

✅ Get real-time stock prices
✅ Compare data across Yahoo Finance, Alpha Vantage, and Finnhub
✅ Fetch multiple stocks at once
✅ Show price changes, volume, market cap
✅ Provide day high/low ranges

## Data Sources

- **Yahoo Finance** - Free, no API key needed, most reliable
- **Finnhub** - Free tier with API key, good for additional data
- **Alpha Vantage** - Free tier limited to 25 requests/day

## Privacy & Security

- Your API keys are stored locally in the config file
- Data is fetched directly from public APIs
- No data is sent to third parties
- The MCP server runs locally on your machine

## Next Steps

1. Configure Claude Desktop using the steps above
2. Restart Claude Desktop
3. Ask Claude about stock prices
4. Enjoy real-time market data in your conversations!

## Support

If you have issues:
1. Check Claude Desktop's developer console (if available)
2. Test the MCP server manually: `python3 mcp_server.py`
3. Verify all dependencies are installed
4. Check the MCP_SETUP.md file for more details
