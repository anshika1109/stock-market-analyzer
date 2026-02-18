#!/bin/bash

# Setup script for adding Stock Market Analyzer MCP to Claude Desktop

echo "🚀 Stock Market Analyzer MCP - Claude Desktop Setup"
echo "=================================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    CONFIG_PATH="$APPDATA/Claude/claude_desktop_config.json"
else
    echo "❌ Unsupported operating system"
    exit 1
fi

echo "📁 Config file location: $CONFIG_PATH"
echo ""

# Create directory if it doesn't exist
CONFIG_DIR=$(dirname "$CONFIG_PATH")
if [ ! -d "$CONFIG_DIR" ]; then
    echo "📂 Creating config directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Backup existing config
if [ -f "$CONFIG_PATH" ]; then
    echo "💾 Backing up existing config..."
    cp "$CONFIG_PATH" "${CONFIG_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup created"
else
    echo "ℹ️  No existing config found, creating new one"
fi

# Get current directory
CURRENT_DIR=$(pwd)
MCP_SERVER_PATH="$CURRENT_DIR/mcp_server.py"

# Find Python path
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "🐍 Using Python: $PYTHON_PATH"
echo "📄 MCP Server: $MCP_SERVER_PATH"
echo ""

# Read API keys from .env file
if [ -f ".env" ]; then
    source .env
    echo "✅ API keys loaded from .env"
else
    echo "⚠️  Warning: .env file not found"
    ALPHA_VANTAGE_API_KEY=""
    FINNHUB_API_KEY=""
fi

# Create or update config
cat > "$CONFIG_PATH" << EOF
{
  "mcpServers": {
    "stock-market-analyzer": {
      "command": "$PYTHON_PATH",
      "args": ["$MCP_SERVER_PATH"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "$ALPHA_VANTAGE_API_KEY",
        "FINNHUB_API_KEY": "$FINNHUB_API_KEY"
      }
    }
  }
}
EOF

echo ""
echo "✅ Configuration written successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Restart Claude Desktop completely"
echo "2. Look for the 🔨 (hammer) icon to see MCP tools"
echo "3. Ask Claude: 'What's the current price of AAPL?'"
echo ""
echo "🎉 Setup complete!"
