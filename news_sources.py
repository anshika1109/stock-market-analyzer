import requests
from config import Config
from typing import Dict, List
from datetime import datetime, timedelta

class NewsSource:
    """Base class for news sources"""
    
    def get_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        raise NotImplementedError

class FinnhubNewsSource(NewsSource):
    """Finnhub company news source"""
    
    def __init__(self):
        self.api_key = Config.FINNHUB_API_KEY
        self.base_url = Config.FINNHUB_BASE_URL
    
    def get_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        if not self.api_key:
            return [{'error': 'API key not configured', 'source': 'Finnhub'}]
        
        # Get news from last 7 days
        to_date = datetime.now()
        from_date = to_date - timedelta(days=7)
        
        try:
            response = requests.get(
                f'{self.base_url}/company-news',
                params={
                    'symbol': symbol,
                    'from': from_date.strftime('%Y-%m-%d'),
                    'to': to_date.strftime('%Y-%m-%d'),
                    'token': self.api_key
                },
                timeout=10
            )
            data = response.json()
            
            if isinstance(data, list):
                news_items = []
                for item in data[:limit * 2]:  # Get more to filter
                    headline = item.get('headline', 'No headline')
                    summary = item.get('summary', 'No summary')
                    
                    # Check if news is price-related
                    if self._is_price_related(headline + ' ' + summary):
                        news_items.append({
                            'headline': headline,
                            'summary': summary,
                            'source': item.get('source', 'Unknown'),
                            'url': item.get('url', ''),
                            'datetime': datetime.fromtimestamp(item.get('datetime', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                            'sentiment': self._analyze_sentiment(headline),
                            'provider': 'Finnhub',
                            'data_source': 'Finnhub API'
                        })
                        
                        if len(news_items) >= limit:
                            break
                
                return news_items if news_items else [{'error': 'No price-related news found', 'source': 'Finnhub'}]
            return [{'error': 'No news available', 'source': 'Finnhub'}]
        except Exception as e:
            return [{'error': str(e), 'source': 'Finnhub'}]
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis based on keywords"""
        text_lower = text.lower()
        
        positive_words = ['surge', 'gain', 'profit', 'growth', 'up', 'rise', 'bullish', 
                         'beat', 'strong', 'success', 'positive', 'boost', 'rally', 'soar',
                         'jump', 'climb', 'upgrade', 'outperform', 'buy']
        negative_words = ['fall', 'drop', 'loss', 'decline', 'down', 'bearish', 
                         'miss', 'weak', 'negative', 'crash', 'plunge', 'concern',
                         'tumble', 'sink', 'downgrade', 'sell', 'underperform']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _is_price_related(self, text: str) -> bool:
        """Check if news is related to price movement"""
        text_lower = text.lower()
        
        price_keywords = [
            'stock', 'price', 'share', 'trading', 'market', 'gain', 'loss',
            'up', 'down', 'rise', 'fall', 'surge', 'drop', 'rally', 'decline',
            'jump', 'plunge', 'soar', 'tumble', 'climb', 'sink', 'percent', '%',
            'earnings', 'revenue', 'profit', 'sales', 'guidance', 'forecast',
            'upgrade', 'downgrade', 'target', 'analyst', 'rating'
        ]
        
        return any(keyword in text_lower for keyword in price_keywords)

class AlphaVantageNewsSource(NewsSource):
    """Alpha Vantage news sentiment source"""
    
    def __init__(self):
        self.api_key = Config.ALPHA_VANTAGE_API_KEY
        self.base_url = Config.ALPHA_VANTAGE_BASE_URL
    
    def get_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        if not self.api_key:
            return [{'error': 'API key not configured', 'source': 'Alpha Vantage'}]
        
        try:
            response = requests.get(
                self.base_url,
                params={
                    'function': 'NEWS_SENTIMENT',
                    'tickers': symbol,
                    'apikey': self.api_key,
                    'limit': limit * 2  # Get more to filter
                },
                timeout=10
            )
            data = response.json()
            
            if 'feed' in data:
                news_items = []
                for item in data['feed']:
                    # Get ticker-specific sentiment
                    ticker_sentiment = None
                    if 'ticker_sentiment' in item:
                        for ts in item['ticker_sentiment']:
                            if ts.get('ticker') == symbol:
                                ticker_sentiment = ts
                                break
                    
                    headline = item.get('title', 'No headline')
                    summary = item.get('summary', 'No summary')[:200] + '...'
                    
                    # Check if news is price-related
                    if self._is_price_related(headline + ' ' + summary):
                        sentiment_score = float(ticker_sentiment.get('ticker_sentiment_score', 0)) if ticker_sentiment else 0
                        sentiment_label = ticker_sentiment.get('ticker_sentiment_label', 'Neutral') if ticker_sentiment else 'Neutral'
                        
                        news_items.append({
                            'headline': headline,
                            'summary': summary,
                            'source': item.get('source', 'Unknown'),
                            'url': item.get('url', ''),
                            'datetime': item.get('time_published', ''),
                            'sentiment': sentiment_label.lower(),
                            'sentiment_score': sentiment_score,
                            'relevance_score': float(ticker_sentiment.get('relevance_score', 0)) if ticker_sentiment else 0,
                            'provider': 'Alpha Vantage',
                            'data_source': 'Alpha Vantage News Sentiment API'
                        })
                        
                        if len(news_items) >= limit:
                            break
                
                return news_items if news_items else [{'error': 'No price-related news found', 'source': 'Alpha Vantage'}]
            return [{'error': 'No news available', 'source': 'Alpha Vantage'}]
        except Exception as e:
            return [{'error': str(e), 'source': 'Alpha Vantage'}]
    
    def _is_price_related(self, text: str) -> bool:
        """Check if news is related to price movement"""
        text_lower = text.lower()
        
        price_keywords = [
            'stock', 'price', 'share', 'trading', 'market', 'gain', 'loss',
            'up', 'down', 'rise', 'fall', 'surge', 'drop', 'rally', 'decline',
            'jump', 'plunge', 'soar', 'tumble', 'climb', 'sink', 'percent', '%',
            'earnings', 'revenue', 'profit', 'sales', 'guidance', 'forecast',
            'upgrade', 'downgrade', 'target', 'analyst', 'rating'
        ]
        
        return any(keyword in text_lower for keyword in price_keywords)

class YahooFinanceNewsSource(NewsSource):
    """Yahoo Finance news (via yfinance)"""
    
    def get_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if news:
                news_items = []
                for item in news[:limit * 2]:  # Get more to filter
                    headline = item.get('title', 'No headline')
                    summary = item.get('summary', 'No summary')
                    
                    # Check if news is price-related
                    if self._is_price_related(headline + ' ' + summary):
                        news_items.append({
                            'headline': headline,
                            'summary': summary,
                            'source': item.get('publisher', 'Yahoo Finance'),
                            'url': item.get('link', ''),
                            'datetime': datetime.fromtimestamp(item.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                            'sentiment': self._analyze_sentiment(headline),
                            'provider': 'Yahoo Finance',
                            'data_source': 'Yahoo Finance News API'
                        })
                        
                        if len(news_items) >= limit:
                            break
                
                return news_items if news_items else [{'error': 'No price-related news found', 'source': 'Yahoo Finance'}]
            return [{'error': 'No news available', 'source': 'Yahoo Finance'}]
        except Exception as e:
            return [{'error': str(e), 'source': 'Yahoo Finance'}]
    
    def _is_price_related(self, text: str) -> bool:
        """Check if news is related to price movement"""
        text_lower = text.lower()
        
        price_keywords = [
            'stock', 'price', 'share', 'trading', 'market', 'gain', 'loss',
            'up', 'down', 'rise', 'fall', 'surge', 'drop', 'rally', 'decline',
            'jump', 'plunge', 'soar', 'tumble', 'climb', 'sink', 'percent', '%',
            'earnings', 'revenue', 'profit', 'sales', 'guidance', 'forecast',
            'upgrade', 'downgrade', 'target', 'analyst', 'rating'
        ]
        
        return any(keyword in text_lower for keyword in price_keywords)
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis based on keywords"""
        text_lower = text.lower()
        
        positive_words = ['surge', 'gain', 'profit', 'growth', 'up', 'rise', 'bullish', 
                         'beat', 'strong', 'success', 'positive', 'boost', 'rally', 'soar',
                         'jump', 'climb', 'upgrade', 'outperform', 'buy']
        negative_words = ['fall', 'drop', 'loss', 'decline', 'down', 'bearish', 
                         'miss', 'weak', 'negative', 'crash', 'plunge', 'concern',
                         'tumble', 'sink', 'downgrade', 'sell', 'underperform']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
