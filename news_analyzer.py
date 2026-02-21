from typing import List, Dict
from news_sources import FinnhubNewsSource, AlphaVantageNewsSource, YahooFinanceNewsSource
import pandas as pd
from collections import Counter

class NewsAnalyzer:
    """Analyzer for stock-related news from multiple sources"""
    
    def __init__(self):
        self.sources = {
            'finnhub': FinnhubNewsSource(),
            'alphavantage': AlphaVantageNewsSource(),
            'yahoo': YahooFinanceNewsSource()
        }
    
    def get_news(self, symbol: str, sources: List[str] = None, limit: int = 10) -> Dict:
        """Get news from specified sources or all sources"""
        if sources is None:
            sources = list(self.sources.keys())
        
        results = {}
        for source_name in sources:
            if source_name in self.sources:
                results[source_name] = self.sources[source_name].get_news(symbol, limit)
        
        return results
    
    def get_aggregated_news(self, symbol: str, limit: int = 20) -> List[Dict]:
        """Get news from all sources and aggregate them"""
        all_news = []
        results = self.get_news(symbol, limit=limit)
        
        for source, news_list in results.items():
            if isinstance(news_list, list):
                for news_item in news_list:
                    if 'error' not in news_item:
                        all_news.append(news_item)
        
        # Sort by datetime (most recent first)
        all_news.sort(key=lambda x: x.get('datetime', ''), reverse=True)
        
        return all_news[:limit]
    
    def analyze_sentiment(self, symbol: str) -> Dict:
        """Analyze overall sentiment from news"""
        news = self.get_aggregated_news(symbol, limit=50)
        
        if not news:
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_articles': 0
            }
        
        sentiments = [item.get('sentiment', 'neutral') for item in news if 'error' not in item]
        sentiment_counts = Counter(sentiments)
        
        # Calculate weighted sentiment score
        sentiment_weights = {'positive': 1, 'neutral': 0, 'negative': -1}
        total_score = sum(sentiment_weights.get(s, 0) for s in sentiments)
        avg_score = total_score / len(sentiments) if sentiments else 0
        
        # Determine overall sentiment
        if avg_score > 0.2:
            overall = 'positive'
        elif avg_score < -0.2:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'overall_sentiment': overall,
            'sentiment_score': round(avg_score, 2),
            'positive_count': sentiment_counts.get('positive', 0),
            'negative_count': sentiment_counts.get('negative', 0),
            'neutral_count': sentiment_counts.get('neutral', 0),
            'total_articles': len(sentiments),
            'recent_headlines': [item.get('headline', '') for item in news[:5]]
        }
    
    def correlate_with_price(self, symbol: str, price_change: float) -> Dict:
        """Correlate news sentiment with price movement"""
        sentiment_analysis = self.analyze_sentiment(symbol)
        
        # Determine if sentiment matches price movement
        sentiment = sentiment_analysis['overall_sentiment']
        correlation = 'unknown'
        
        if price_change > 0 and sentiment == 'positive':
            correlation = 'aligned'
            explanation = 'Positive news aligns with price increase'
        elif price_change < 0 and sentiment == 'negative':
            correlation = 'aligned'
            explanation = 'Negative news aligns with price decrease'
        elif price_change > 0 and sentiment == 'negative':
            correlation = 'divergent'
            explanation = 'Price increased despite negative news (possible market optimism or other factors)'
        elif price_change < 0 and sentiment == 'positive':
            correlation = 'divergent'
            explanation = 'Price decreased despite positive news (possible profit-taking or market conditions)'
        else:
            correlation = 'neutral'
            explanation = 'Neutral news sentiment with price movement'
        
        return {
            'symbol': symbol,
            'price_change': price_change,
            'price_direction': 'up' if price_change > 0 else 'down' if price_change < 0 else 'flat',
            'sentiment': sentiment,
            'sentiment_score': sentiment_analysis['sentiment_score'],
            'correlation': correlation,
            'explanation': explanation,
            'article_count': sentiment_analysis['total_articles'],
            'sentiment_breakdown': {
                'positive': sentiment_analysis['positive_count'],
                'negative': sentiment_analysis['negative_count'],
                'neutral': sentiment_analysis['neutral_count']
            }
        }
    
    def get_news_summary(self, symbol: str) -> str:
        """Get a text summary of recent news"""
        news = self.get_aggregated_news(symbol, limit=5)
        sentiment = self.analyze_sentiment(symbol)
        
        if not news:
            return f"No recent news found for {symbol}"
        
        summary = f"📰 News Summary for {symbol}\n"
        summary += f"Overall Sentiment: {sentiment['overall_sentiment'].upper()} "
        summary += f"(Score: {sentiment['sentiment_score']})\n"
        summary += f"Articles Analyzed: {sentiment['total_articles']}\n\n"
        summary += "Recent Headlines:\n"
        
        for i, item in enumerate(news[:5], 1):
            if 'error' not in item:
                sentiment_emoji = {
                    'positive': '📈',
                    'negative': '📉',
                    'neutral': '➡️'
                }.get(item.get('sentiment', 'neutral'), '➡️')
                
                summary += f"{i}. {sentiment_emoji} {item.get('headline', 'No headline')}\n"
                summary += f"   Source: {item.get('source', 'Unknown')} | {item.get('datetime', 'Unknown date')}\n"
        
        return summary
