# Stock Market Analyzer MCP - Complete Workflow

## Overview

This document explains how data flows from your question to Claude, through the MCP server, to the stock APIs, and back to you.

## The Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    "Get the stock price for AAPL"
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLAUDE (AI Assistant)                       │
│  • Understands your natural language question                   │
│  • Recognizes it needs stock market data                        │
│  • Sees available MCP tools: get_stock_quote, etc.              │
│  • Decides which tool to use                                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    MCP Protocol Request (JSON-RPC)
                    {
                      "method": "tools/call",
                      "params": {
                        "name": "get_best_quote",
                        "arguments": {"symbol": "AAPL"}
                      }
                    }
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP SERVER (mcp_server.py)                    │
│  • Receives the tool call request                               │
│  • Validates the parameters                                     │
│  • Routes to appropriate handler function                       │
│  • Calls analyzer.get_best_quote("AAPL")                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYZER (analyzer.py)                        │
│  • Coordinates data fetching from multiple sources              │
│  • Calls each data source in parallel                           │
│  • Prioritizes: Yahoo > Finnhub > Alpha Vantage                 │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
        ┌───────────────┐  ┌──────────┐  ┌──────────────┐
        │ Yahoo Finance │  │ Finnhub  │  │ Alpha Vantage│
        │ (yfinance lib)│  │   API    │  │     API      │
        └───────────────┘  └──────────┘  └──────────────┘
                    │            │            │
                    ▼            ▼            ▼
              HTTP Requests to Public APIs
                    │            │            │
                    ▼            ▼            ▼
        ┌───────────────┐  ┌──────────┐  ┌──────────────┐
        │  Yahoo API    │  │ Finnhub  │  │ Alpha Vantage│
        │   Servers     │  │  Servers │  │   Servers    │
        └───────────────┘  └──────────┘  └──────────────┘
                    │            │            │
                    └────────────┼────────────┘
                                 ▼
                    Raw Stock Data (JSON)
                    {
                      "price": 263.88,
                      "change": 8.10,
                      "volume": 58081661,
                      ...
                    }
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATA SOURCES (data_sources.py)                  │
│  • Parse API responses                                           │
│  • Normalize data format                                        │
│  • Handle errors gracefully                                     │
│  • Return standardized data structure                           │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYZER (analyzer.py)                        │
│  • Receives data from all sources                               │
│  • Compares and validates data                                  │
│  • Selects best/most reliable quote                             │
│  • Returns formatted result                                     │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MCP SERVER (mcp_server.py)                    │
│  • Formats response as JSON                                     │
│  • Wraps in MCP protocol response                               │
│  • Sends back to Claude                                         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    MCP Protocol Response (JSON)
                    {
                      "result": {
                        "symbol": "AAPL",
                        "price": 263.88,
                        "change": 8.10,
                        "source": "Yahoo Finance"
                      }
                    }
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLAUDE (AI Assistant)                       │
│  • Receives the structured data                                 │
│  • Interprets the results                                       │
│  • Formats into natural language                                │
│  • Adds context and insights                                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    Natural Language Response
                    "Apple (AAPL) is currently trading at 
                     $263.88, up $8.10 (+3.17%) today."
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER SEES RESULT                         │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Step-by-Step Breakdown

### 1. User Question
**You:** "Get the stock price for AAPL"

### 2. Claude Processing
- Claude's AI understands you want stock market data
- Checks available MCP tools
- Sees: `get_stock_quote`, `get_best_quote`, `compare_stock_sources`, `get_multiple_quotes`
- Decides `get_best_quote` is most appropriate
- Prepares MCP tool call

### 3. MCP Protocol Communication
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_best_quote",
    "arguments": {
      "symbol": "AAPL"
    }
  }
}
```

### 4. MCP Server Receives Request
**File:** `mcp_server.py`
```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "get_best_quote":
        symbol = arguments.get("symbol")
        result = analyzer.get_best_quote(symbol)
        return result
```

### 5. Analyzer Coordinates Data Fetching
**File:** `analyzer.py`
```python
def get_best_quote(self, symbol: str):
    results = self.get_quote(symbol)
    # Priority: Yahoo > Finnhub > Alpha Vantage
    for source in ['yahoo', 'finnhub', 'alphavantage']:
        if source in results and 'error' not in results[source]:
            return results[source]
```

### 6. Data Sources Fetch from APIs
**File:** `data_sources.py`

**Yahoo Finance:**
```python
ticker = yf.Ticker("AAPL")
info = ticker.info
price = info.get('currentPrice')
```

**Finnhub:**
```python
response = requests.get(
    'https://finnhub.io/api/v1/quote',
    params={'symbol': 'AAPL', 'token': API_KEY}
)
```

**Alpha Vantage:**
```python
response = requests.get(
    'https://www.alphavantage.co/query',
    params={
        'function': 'GLOBAL_QUOTE',
        'symbol': 'AAPL',
        'apikey': API_KEY
    }
)
```

### 7. Data Normalization
Each source returns different formats, normalized to:
```python
{
    "symbol": "AAPL",
    "price": 263.88,
    "change": 8.10,
    "change_percent": 3.17,
    "volume": 58081661,
    "source": "Yahoo Finance"
}
```

### 8. Response Back to Claude
MCP server sends formatted JSON back through the protocol

### 9. Claude Formats Response
Claude converts the structured data into natural language:
- Adds context
- Formats numbers nicely
- Provides insights
- Makes it conversational

### 10. You See the Result
"Apple (AAPL) is currently trading at $263.88, up $8.10 (+3.17%) today with a volume of 58M shares."

## Key Components

### Configuration Files

**`.env`** - API Keys
```
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key
```

**`claude_desktop_config.json`** - MCP Server Registration
```json
{
  "mcpServers": {
    "stock-market-analyzer": {
      "command": "/opt/homebrew/bin/python3",
      "args": ["/path/to/mcp_server.py"],
      "env": { "API_KEYS": "..." }
    }
  }
}
```

### Python Files

1. **`mcp_server.py`** - MCP protocol handler
2. **`analyzer.py`** - Orchestrates data fetching
3. **`data_sources.py`** - API integrations
4. **`config.py`** - Configuration management

## Data Flow Summary

```
User Question
    ↓
Claude AI (understands intent)
    ↓
MCP Protocol (standardized communication)
    ↓
MCP Server (routes request)
    ↓
Analyzer (coordinates)
    ↓
Data Sources (fetch from APIs)
    ↓
Yahoo/Finnhub/Alpha Vantage APIs
    ↓
Raw Data (JSON responses)
    ↓
Data Sources (normalize)
    ↓
Analyzer (select best)
    ↓
MCP Server (format response)
    ↓
MCP Protocol (send back)
    ↓
Claude AI (interpret & format)
    ↓
Natural Language Response
    ↓
User Sees Result
```

## Error Handling

At each step, errors are caught and handled:

1. **API Errors** → Return error message with source
2. **Rate Limits** → Try next source
3. **Invalid Symbol** → Return "No data available"
4. **Network Issues** → Timeout and fallback
5. **MCP Errors** → Return structured error response

## Performance

- **Parallel Requests:** All sources queried simultaneously
- **Caching:** yfinance library caches recent data
- **Fallback:** If one source fails, others still work
- **Timeout:** 10 seconds per API call

## Security

- API keys stored in environment variables
- No data logged or stored
- Direct API calls (no intermediary servers)
- Local execution only

## Advantages of This Architecture

1. **Modular:** Easy to add new data sources
2. **Reliable:** Multiple sources provide redundancy
3. **Fast:** Parallel requests minimize latency
4. **Flexible:** Works with any MCP-compatible client
5. **Maintainable:** Clear separation of concerns
6. **Extensible:** Easy to add new tools/features
