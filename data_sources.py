import requests
import yfinance as yf
from config import Config
from typing import Dict, Optional

class StockDataSource:
    """Base class for stock data sources"""
    
    def get_quote(self, symbol: str) -> Dict:
        raise NotImplementedError

class YahooFinanceSource(StockDataSource):
    """Yahoo Finance data source (free, no API key needed)"""
    
    def get_quote(self, symbol: str) -> Dict:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'change': info.get('regularMarketChange'),
                'change_percent': info.get('regularMarketChangePercent'),
                'volume': info.get('volume'),
                'market_cap': info.get('marketCap'),
                'high': info.get('dayHigh') or info.get('regularMarketDayHigh'),
                'low': info.get('dayLow') or info.get('regularMarketDayLow'),
                'open': info.get('open') or info.get('regularMarketOpen'),
                'previous_close': info.get('previousClose') or info.get('regularMarketPreviousClose'),
                'source': 'Yahoo Finance'
            }
        except Exception as e:
            return {'error': str(e), 'source': 'Yahoo Finance'}

class AlphaVantageSource(StockDataSource):
    """Alpha Vantage data source"""
    
    def __init__(self):
        self.api_key = Config.ALPHA_VANTAGE_API_KEY
        self.base_url = Config.ALPHA_VANTAGE_BASE_URL
    
    def get_quote(self, symbol: str) -> Dict:
        if not self.api_key:
            return {'error': 'API key not configured', 'source': 'Alpha Vantage'}
        
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': symbol,
                    'price': float(quote.get('05. price', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent', '0%').rstrip('%'),
                    'volume': int(quote.get('06. volume', 0)),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0)),
                    'open': float(quote.get('02. open', 0)),
                    'previous_close': float(quote.get('08. previous close', 0)),
                    'source': 'Alpha Vantage'
                }
            return {'error': 'No data available', 'source': 'Alpha Vantage'}
        except Exception as e:
            return {'error': str(e), 'source': 'Alpha Vantage'}

class FinnhubSource(StockDataSource):
    """Finnhub data source"""
    
    def __init__(self):
        self.api_key = Config.FINNHUB_API_KEY
        self.base_url = Config.FINNHUB_BASE_URL
    
    def get_quote(self, symbol: str) -> Dict:
        if not self.api_key:
            return {'error': 'API key not configured', 'source': 'Finnhub'}
        
        try:
            response = requests.get(
                f'{self.base_url}/quote',
                params={'symbol': symbol, 'token': self.api_key},
                timeout=10
            )
            data = response.json()
            
            if 'c' in data:
                return {
                    'symbol': symbol,
                    'price': data['c'],
                    'change': data['d'],
                    'change_percent': data['dp'],
                    'high': data['h'],
                    'low': data['l'],
                    'open': data['o'],
                    'previous_close': data['pc'],
                    'source': 'Finnhub'
                }
            return {'error': 'No data available', 'source': 'Finnhub'}
        except Exception as e:
            return {'error': str(e), 'source': 'Finnhub'}
