#!/usr/bin/env python3
"""
MCP Server for Stock Market Analyzer
Provides real-time stock data and news analysis via MCP protocol
"""

import asyncio
import json
from typing import Any
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from analyzer import StockAnalyzer
from news_analyzer import NewsAnalyzer

# Initialize the analyzers
stock_analyzer = StockAnalyzer()
news_analyzer = NewsAnalyzer()

# Create MCP server instance
server = Server("stock-market-analyzer")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for stock market analysis"""
    return [
        types.Tool(
            name="get_stock_quote",
            description="Get real-time stock quote from multiple data sources (Yahoo Finance, Alpha Vantage, Finnhub)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    },
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["yahoo", "alphavantage", "finnhub"]
                        },
                        "description": "Data sources to query (default: all sources)",
                        "default": ["yahoo", "alphavantage", "finnhub"]
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="compare_stock_sources",
            description="Compare stock data across all available sources and return a formatted comparison",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_best_quote",
            description="Get the most reliable/recent quote from available sources (prioritizes Yahoo > Finnhub > Alpha Vantage)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_multiple_quotes",
            description="Get quotes for multiple stock symbols at once",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock symbols (e.g., ['AAPL', 'GOOGL', 'MSFT'])"
                    },
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["yahoo", "alphavantage", "finnhub"]
                        },
                        "description": "Data sources to query (default: all sources)",
                        "default": ["yahoo", "alphavantage", "finnhub"]
                    }
                },
                "required": ["symbols"]
            }
        ),
        types.Tool(
            name="get_stock_news",
            description="Get recent news articles for a stock symbol from multiple sources",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    },
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["finnhub", "alphavantage", "yahoo"]
                        },
                        "description": "News sources to query (default: all sources)",
                        "default": ["finnhub", "alphavantage", "yahoo"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of articles per source (default: 10)",
                        "default": 10
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="analyze_news_sentiment",
            description="Analyze overall sentiment from recent news articles for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="correlate_news_with_price",
            description="Correlate news sentiment with stock price movement to understand if news explains price changes",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    },
                    "price_change": {
                        "type": "number",
                        "description": "Price change amount (e.g., 5.25 for $5.25 increase, -3.50 for $3.50 decrease)"
                    }
                },
                "required": ["symbol", "price_change"]
            }
        ),
        types.Tool(
            name="get_news_summary",
            description="Get a formatted text summary of recent news and sentiment for a stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL, GOOGL, MSFT)"
                    }
                },
                "required": ["symbol"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests"""
    
    if not arguments:
        raise ValueError("Missing arguments")
    
    try:
        if name == "get_stock_quote":
            symbol = arguments.get("symbol", "").upper()
            sources = arguments.get("sources", ["yahoo", "alphavantage", "finnhub"])
            
            if not symbol:
                raise ValueError("Symbol is required")
            
            result = stock_analyzer.get_quote(symbol, sources=sources)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        
        elif name == "compare_stock_sources":
            symbol = arguments.get("symbol", "").upper()
            
            if not symbol:
                raise ValueError("Symbol is required")
            
            df = stock_analyzer.compare_sources(symbol)
            
            if df.empty:
                result = {"error": "No data available from any source", "symbol": symbol}
            else:
                result = {
                    "symbol": symbol,
                    "comparison": df.to_dict(orient="records")
                }
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        
        elif name == "get_best_quote":
            symbol = arguments.get("symbol", "").upper()
            
            if not symbol:
                raise ValueError("Symbol is required")
            
            result = stock_analyzer.get_best_quote(symbol)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        
        elif name == "get_multiple_quotes":
            symbols = arguments.get("symbols", [])
            sources = arguments.get("sources", ["yahoo", "alphavantage", "finnhub"])
            
            if not symbols:
                raise ValueError("Symbols list is required")
            
            results = {}
            for symbol in symbols:
                symbol = symbol.upper()
                results[symbol] = stock_analyzer.get_quote(symbol, sources=sources)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )
            ]
        
        elif name == "get_stock_news":
            symbol = arguments.get("symbol", "").upper()
            sources = arguments.get("sources", ["finnhub", "alphavantage", "yahoo"])
            limit = arguments.get("limit", 10)
            
            if not symbol:
                raise ValueError("Symbol is required")
            
            result = news_analyzer.get_news(symbol, sources=sources, limit=limit)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        
        elif name == "analyze_news_sentiment":
            symbol = arguments.get("symbol", "").upper()
            
            if not symbol:
                raise ValueError("Symbol is required")
            
            result = news_analyzer.analyze_sentiment(symbol)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        
        elif name == "correlate_news_with_price":
            symbol = arguments.get("symbol", "").upper()
            price_change = arguments.get("price_change")
            
            if not symbol:
                raise ValueError("Symbol is required")
            if price_change is None:
                raise ValueError("Price change is required")
            
            result = news_analyzer.correlate_with_price(symbol, float(price_change))
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )
            ]
        
        elif name == "get_news_summary":
            symbol = arguments.get("symbol", "").upper()
            
            if not symbol:
                raise ValueError("Symbol is required")
            
            result = news_analyzer.get_news_summary(symbol)
            
            return [
                types.TextContent(
                    type="text",
                    text=result
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )
        ]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="stock-market-analyzer",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
