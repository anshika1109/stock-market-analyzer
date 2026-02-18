from typing import List, Dict
from data_sources import YahooFinanceSource, AlphaVantageSource, FinnhubSource
import pandas as pd

class StockAnalyzer:
    """Main analyzer that aggregates data from multiple sources"""
    
    def __init__(self):
        self.sources = {
            'yahoo': YahooFinanceSource(),
            'alphavantage': AlphaVantageSource(),
            'finnhub': FinnhubSource()
        }
    
    def get_quote(self, symbol: str, sources: List[str] = None) -> Dict:
        """Get quote from specified sources or all sources"""
        if sources is None:
            sources = list(self.sources.keys())
        
        results = {}
        for source_name in sources:
            if source_name in self.sources:
                results[source_name] = self.sources[source_name].get_quote(symbol)
        
        return results
    
    def compare_sources(self, symbol: str) -> pd.DataFrame:
        """Compare data from all sources in a DataFrame"""
        results = self.get_quote(symbol)
        
        data = []
        for source, quote in results.items():
            if 'error' not in quote:
                data.append({
                    'Source': source,
                    'Price': quote.get('price'),
                    'Change': quote.get('change'),
                    'Change %': quote.get('change_percent'),
                    'Volume': quote.get('volume')
                })
        
        return pd.DataFrame(data)
    
    def get_best_quote(self, symbol: str) -> Dict:
        """Get the most recent/reliable quote from available sources"""
        results = self.get_quote(symbol)
        
        # Priority: Yahoo (free, reliable) > Finnhub > Alpha Vantage
        for source in ['yahoo', 'finnhub', 'alphavantage']:
            if source in results and 'error' not in results[source]:
                return results[source]
        
        return {'error': 'No data available from any source'}
