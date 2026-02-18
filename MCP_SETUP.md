# MCP Server Setup Guide

## What is MCP?

MCP (Model Context Protocol) allows AI assistants to use your stock market analyzer as a tool. Once configured, you can ask AI assistants to fetch stock data directly.

## Installation

1. Install MCP dependency:
```bash
pip install mcp
```

2. Make the MCP server executable:
```bash
chmod +x mcp_server.py
```

## Configuration

### Option 1: Workspace Configuration (Recommended)

The MCP configuration is already set up in `.kiro/settings/mcp.json` for this workspace.

### Option 2: Global Configuration

To use this MCP server across all workspaces, add to `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "stock-market-analyzer": {
      "command": "python3",
      "args": ["/Users/anshikagupta/Sementic_analysis/mcp_server.py"],
      "env": {},
      "disabled": false,
      "autoApprove": ["get_stock_quote", "get_best_quote", "compare_stock_sources", "get_multiple_quotes"]
    }
  }
}
```

## Testing the MCP Server

Test if the server works:

```bash
python3 mcp_server.py
```

The server should start and wait for input. Press Ctrl+C to stop.

## Using in Kiro

Once configured, restart Kiro or reload the MCP servers. Then you can use natural language:

- "Get the current stock price for AAPL"
- "Compare TSLA across all data sources"
- "Get quotes for AAPL, GOOGL, and MSFT"
- "What's the best available quote for NVDA?"

## Available Tools

### 1. get_stock_quote
Get real-time stock quote from specified sources.

**Parameters:**
- `symbol` (required): Stock symbol (e.g., "AAPL")
- `sources` (optional): Array of sources ["yahoo", "alphavantage", "finnhub"]

**Example:**
```json
{
  "symbol": "AAPL",
  "sources": ["yahoo", "finnhub"]
}
```

### 2. compare_stock_sources
Compare stock data across all available sources.

**Parameters:**
- `symbol` (required): Stock symbol (e.g., "AAPL")

**Example:**
```json
{
  "symbol": "TSLA"
}
```

### 3. get_best_quote
Get the most reliable quote (prioritizes Yahoo > Finnhub > Alpha Vantage).

**Parameters:**
- `symbol` (required): Stock symbol (e.g., "AAPL")

**Example:**
```json
{
  "symbol": "GOOGL"
}
```

### 4. get_multiple_quotes
Get quotes for multiple symbols at once.

**Parameters:**
- `symbols` (required): Array of stock symbols
- `sources` (optional): Array of sources to query

**Example:**
```json
{
  "symbols": ["AAPL", "GOOGL", "MSFT"],
  "sources": ["yahoo"]
}
```

## API Keys

If you want to use Alpha Vantage or Finnhub, add your API keys to the `.env` file:

```
ALPHA_VANTAGE_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here
```

Yahoo Finance works without any API key.

## Troubleshooting

### Server not connecting
- Check that Python 3.9+ is installed: `python3 --version`
- Verify MCP is installed: `pip show mcp`
- Check the path in mcp.json is correct

### No data returned
- Verify your `.env` file has API keys (if using Alpha Vantage or Finnhub)
- Test the analyzer directly: `python main.py AAPL`
- Check internet connection

### Permission denied
- Make sure the script is executable: `chmod +x mcp_server.py`
- Use full absolute paths in mcp.json

## Viewing MCP Servers in Kiro

1. Open Command Palette (Cmd+Shift+P)
2. Search for "MCP"
3. Select "View MCP Servers" to see status
4. Use "Reconnect MCP Server" if needed
