from flask import Flask, render_template, request, jsonify
from analyzer import StockAnalyzer
from news_analyzer import NewsAnalyzer
from datetime import datetime

app = Flask(__name__)
stock_analyzer = StockAnalyzer()
news_analyzer = NewsAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/quote', methods=['POST'])
def get_quote():
    data = request.json
    symbols = data.get('symbols', [])
    sources = data.get('sources', ['yahoo', 'alphavantage', 'finnhub'])
    
    results = {}
    for symbol in symbols:
        results[symbol] = stock_analyzer.get_quote(symbol.upper(), sources=sources)
    
    return jsonify({
        'results': results,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/news', methods=['POST'])
def get_news():
    data = request.json
    symbol = data.get('symbol', '').upper()
    limit = data.get('limit', 10)
    
    if not symbol:
        return jsonify({'error': 'Symbol is required'}), 400
    
    # Get aggregated news
    news = news_analyzer.get_aggregated_news(symbol, limit=limit)
    
    # Get sentiment analysis
    sentiment = news_analyzer.analyze_sentiment(symbol)
    
    # Get price data for correlation
    quote = stock_analyzer.get_best_quote(symbol)
    price_change = quote.get('change', 0) if 'error' not in quote else 0
    
    # Get correlation
    correlation = news_analyzer.correlate_with_price(symbol, price_change)
    
    return jsonify({
        'symbol': symbol,
        'news': news,
        'sentiment': sentiment,
        'correlation': correlation,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Stock Market Dashboard Starting...")
    print("="*50)
    print("\n📊 Open your browser and go to:")
    print("   http://127.0.0.1:8080")
    print("   or http://localhost:8080")
    print("\n💡 Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='127.0.0.1', port=8080)
