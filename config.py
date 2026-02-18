import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')
    
    # API endpoints
    ALPHA_VANTAGE_BASE_URL = 'https://www.alphavantage.co/query'
    FINNHUB_BASE_URL = 'https://finnhub.io/api/v1'
