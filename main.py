#!/usr/bin/env python3
from analyzer import StockAnalyzer
import sys

def main():
    analyzer = StockAnalyzer()
    
    # Get symbols from command line or prompt user
    if len(sys.argv) > 1:
        symbols = sys.argv[1:]
    else:
        user_input = input("Enter stock symbols (comma-separated, e.g., AAPL,TSLA,GOOGL): ").strip()
        if user_input:
            symbols = [s.strip().upper() for s in user_input.split(',')]
        else:
            symbols = ['AAPL', 'GOOGL', 'MSFT']  # Default fallback
    
    print("Stock Market Real-Time Data Analyzer")
    print("=" * 50)
    
    for symbol in symbols:
        print(f"\n{symbol}:")
        print("-" * 50)
        
        # Get best available quote
        quote = analyzer.get_best_quote(symbol)
        
        if 'error' in quote:
            print(f"Error: {quote['error']}")
        else:
            print(f"Source: {quote['source']}")
            print(f"Price: ${quote.get('price', 'N/A')}")
            print(f"Change: {quote.get('change', 'N/A')}")
            print(f"Change %: {quote.get('change_percent', 'N/A')}%")
            if 'volume' in quote:
                print(f"Volume: {quote.get('volume'):,}")
        
        # Compare all sources
        print("\nComparison across sources:")
        df = analyzer.compare_sources(symbol)
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("No data available from any source")

if __name__ == '__main__':
    main()
