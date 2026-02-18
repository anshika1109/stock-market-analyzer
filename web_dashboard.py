from flask import Flask, render_template, request, jsonify
from analyzer import StockAnalyzer
from datetime import datetime

app = Flask(__name__)
analyzer = StockAnalyzer()

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
        results[symbol] = analyzer.get_quote(symbol.upper(), sources=sources)
    
    return jsonify({
        'results': results,
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
