#!/usr/bin/env python3
"""
MCP Server for Stock Market Analyzer
Provides real-time stock data from multiple sources via MCP protocol
"""

import asyncio
import json
from typing import Any
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from analyzer import StockAnalyzer

# Initialize the analyzer
analyzer = StockAnalyzer()

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
            
            result = analyzer.get_quote(symbol, sources=sources)
            
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
            
            df = analyzer.compare_sources(symbol)
            
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
            
            result = analyzer.get_best_quote(symbol)
            
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
                results[symbol] = analyzer.get_quote(symbol, sources=sources)
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
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
