# News Filtering Update - Price-Related News Only

## 🎯 What Changed

The news analysis system now filters and shows **only news articles that are directly related to stock price movements**.

## ✨ New Features

### 1. **Intelligent Price-Related Filtering**

News articles are now filtered to show only those containing keywords related to:
- **Price movements**: up, down, rise, fall, surge, drop, rally, decline, jump, plunge, soar, tumble
- **Trading activity**: stock, price, share, trading, market, gain, loss, percent
- **Financial metrics**: earnings, revenue, profit, sales, guidance, forecast
- **Analyst activity**: upgrade, downgrade, target, analyst, rating

### 2. **Clear Data Source Attribution**

Each news article now clearly shows:
- **📡 Data Source**: The API used (e.g., "Finnhub API", "Alpha Vantage News Sentiment API", "Yahoo Finance News API")
- **Publisher**: The original news publisher (e.g., "SeekingAlpha", "Benzinga", "Yahoo Finance")
- **Relevance Score**: For Alpha Vantage news (shows how relevant the news is to the stock)

### 3. **Enhanced Sentiment Analysis**

Expanded keyword lists for better sentiment detection:
- **Positive**: surge, gain, profit, growth, up, rise, bullish, beat, strong, success, boost, rally, soar, jump, climb, upgrade, outperform, buy
- **Negative**: fall, drop, loss, decline, down, bearish, miss, weak, crash, plunge, concern, tumble, sink, downgrade, sell, underperform

## 📊 Dashboard Updates

### Web Dashboard (`templates/index.html`)

**New Display Format:**
```
📊 Price-Related News (Filtered)
Showing only news articles that discuss price movements, earnings, ratings, or market performance.

📈 [Headline]
📡 Data Source: Alpha Vantage News Sentiment API | Publisher: Benzinga | 2026-02-18 12:00:00
Sentiment: BULLISH | Relevance: 95%
[Summary text...]
Read more →
```

**Key Improvements:**
- Clear "Price-Related News (Filtered)" header
- Explanation of filtering criteria
- Prominent data source display
- Relevance scores (when available)
- Color-coded sentiment badges

## 🔍 How It Works

### Filtering Process:

1. **Fetch More Articles**: System fetches 2x the requested limit from each source
2. **Apply Filter**: Each article is checked for price-related keywords
3. **Return Filtered**: Only articles matching criteria are returned
4. **Limit Results**: Returns up to the requested limit of filtered articles

### Example Keywords Detected:

**Price Movement Keywords:**
- "Stock surges 15% after earnings beat"  ✅
- "Shares drop on analyst downgrade"  ✅
- "Price target raised to $50"  ✅
- "Company announces new product"  ❌ (not price-related)

## 📝 Code Changes

### Files Modified:

1. **`news_sources.py`**
   - Added `_is_price_related()` method to all source classes
   - Enhanced `_analyze_sentiment()` with more keywords
   - Added `data_source` field to all news items
   - Implemented filtering in `get_news()` methods

2. **`templates/index.html`**
   - Updated news display to show data source prominently
   - Added filtering explanation text
   - Enhanced metadata display with relevance scores

## 🎯 Benefits

1. **Focused Information**: Users see only news that matters for price analysis
2. **Source Transparency**: Clear attribution of where data comes from
3. **Better Correlation**: Easier to understand news-price relationships
4. **Reduced Noise**: No irrelevant news cluttering the analysis

## 📈 Example Output

### Before (All News):
- Company announces new product launch
- CEO gives interview about company culture
- Stock drops 5% on earnings miss  ← Only this is relevant
- Company sponsors local event

### After (Filtered):
- Stock drops 5% on earnings miss
- Analyst upgrades rating to Buy
- Shares surge on strong revenue guidance
- Price target raised by JPMorgan

## 🚀 Usage

### Command Line:
```bash
python news_cli.py SOFI news
```

### Web Dashboard:
1. Enter stock symbol (e.g., SOFI)
2. Click "📰 Get News Analysis"
3. See only price-related news with clear source attribution

### MCP Server:
```python
# Through Kiro or Claude Desktop
"Get price-related news for SOFI"
"Show me news affecting AAPL stock price"
```

## 🔧 Customization

To adjust filtering, modify the `price_keywords` list in `_is_price_related()` method in `news_sources.py`:

```python
price_keywords = [
    'stock', 'price', 'share', 'trading', 'market',
    # Add your custom keywords here
]
```

## ⚠️ Note

- If no price-related news is found, you'll see: "No price-related news found"
- The system fetches 2x articles to ensure enough filtered results
- Relevance scores are only available from Alpha Vantage
- Filtering is done locally after fetching from APIs
