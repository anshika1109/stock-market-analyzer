#!/usr/bin/env python3
"""
Command-line interface for stock news analysis
"""

from news_analyzer import NewsAnalyzer
from analyzer import StockAnalyzer
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python news_cli.py <SYMBOL> [command]")
        print("\nCommands:")
        print("  news       - Get recent news (default)")
        print("  sentiment  - Analyze news sentiment")
        print("  correlate  - Correlate news with price movement")
        print("  summary    - Get news summary")
        print("\nExample:")
        print("  python news_cli.py AAPL")
        print("  python news_cli.py AAPL sentiment")
        print("  python news_cli.py AAPL correlate")
        sys.exit(1)
    
    symbol = sys.argv[1].upper()
    command = sys.argv[2] if len(sys.argv) > 2 else 'news'
    
    news_analyzer = NewsAnalyzer()
    stock_analyzer = StockAnalyzer()
    
    print(f"\n{'='*70}")
    print(f"Stock News Analysis: {symbol}")
    print(f"{'='*70}\n")
    
    if command == 'news':
        print("📰 Recent News Articles:\n")
        news = news_analyzer.get_aggregated_news(symbol, limit=10)
        
        if not news:
            print(f"No news found for {symbol}")
            return
        
        for i, article in enumerate(news, 1):
            if 'error' not in article:
                sentiment_emoji = {
                    'positive': '📈',
                    'negative': '📉',
                    'neutral': '➡️'
                }.get(article.get('sentiment', 'neutral'), '➡️')
                
                print(f"{i}. {sentiment_emoji} {article.get('headline', 'No headline')}")
                print(f"   Source: {article.get('source', 'Unknown')} ({article.get('provider', 'Unknown')})")
                print(f"   Date: {article.get('datetime', 'Unknown')}")
                print(f"   Sentiment: {article.get('sentiment', 'neutral').upper()}")
                if article.get('url'):
                    print(f"   URL: {article.get('url')}")
                print()
    
    elif command == 'sentiment':
        print("📊 Sentiment Analysis:\n")
        sentiment = news_analyzer.analyze_sentiment(symbol)
        
        print(f"Overall Sentiment: {sentiment['overall_sentiment'].upper()}")
        print(f"Sentiment Score: {sentiment['sentiment_score']}")
        print(f"\nArticle Breakdown:")
        print(f"  Positive: {sentiment['positive_count']}")
        print(f"  Negative: {sentiment['negative_count']}")
        print(f"  Neutral: {sentiment['neutral_count']}")
        print(f"  Total: {sentiment['total_articles']}")
        
        if sentiment['recent_headlines']:
            print(f"\nRecent Headlines:")
            for i, headline in enumerate(sentiment['recent_headlines'], 1):
                print(f"  {i}. {headline}")
    
    elif command == 'correlate':
        print("🔗 News-Price Correlation:\n")
        
        # Get current price data
        quote = stock_analyzer.get_best_quote(symbol)
        
        if 'error' in quote:
            print(f"Error getting price data: {quote['error']}")
            return
        
        price_change = quote.get('change', 0)
        
        correlation = news_analyzer.correlate_with_price(symbol, price_change)
        
        print(f"Stock: {correlation['symbol']}")
        print(f"Price Change: ${correlation['price_change']:.2f} ({correlation['price_direction']})")
        print(f"News Sentiment: {correlation['sentiment'].upper()}")
        print(f"Sentiment Score: {correlation['sentiment_score']}")
        print(f"\nCorrelation: {correlation['correlation'].upper()}")
        print(f"Explanation: {correlation['explanation']}")
        print(f"\nArticles Analyzed: {correlation['article_count']}")
        print(f"Sentiment Breakdown:")
        print(f"  Positive: {correlation['sentiment_breakdown']['positive']}")
        print(f"  Negative: {correlation['sentiment_breakdown']['negative']}")
        print(f"  Neutral: {correlation['sentiment_breakdown']['neutral']}")
    
    elif command == 'summary':
        print(news_analyzer.get_news_summary(symbol))
    
    else:
        print(f"Unknown command: {command}")
        print("Valid commands: news, sentiment, correlate, summary")
    
    print(f"\n{'='*70}\n")

if __name__ == '__main__':
    main()
