# Multi-Purpose MCP Server - Quick Reference

## 🎯 6 Tools Available

| Tool | Purpose | API Key Required |
|------|---------|-----------------|
| `get_exchange_rate()` | Currency conversion | ❌ No |
| `tavily_search()` | Web search | ✅ Yes (Tavily) |
| `news_search()` | Search news articles | ✅ Yes (NewsAPI) |
| `news_by_category()` | Get headlines by category | ✅ Yes (NewsAPI) |
| `get_crypto_prices()` | Crypto market data | ❌ No |
| `weather_search()` | Weather information | ❌ No |

## 🎭 6 Prompts Available

1. **financial_analyst_prompt** - Financial markets & analysis
2. **news_journalist_prompt** - News research & reporting
3. **investment_advisor_prompt** - Investment advice
4. **travel_planner_prompt** - Travel & trip planning
5. **market_researcher_prompt** - Market trends & opportunities
6. **weather_analyst_prompt** - Weather forecasting

## 🔑 API Keys Needed

```bash
# Get from https://tavily.com
export TAVILY_API_KEY="..."

# Get from https://newsapi.org
export NEWS_API_KEY="..."
```

## 📦 Installation

```bash
pip install fastmcp httpx
export TAVILY_API_KEY="your_key"
export NEWS_API_KEY="your_key"
python currency_mcp_server.py
```

## 💡 Common Use Cases

**Financial Analysis**
```python
# Get exchange rate
get_exchange_rate("USD", "EUR")

# Search financial news
news_search("stock market", count=10)

# Track crypto
get_crypto_prices("bitcoin,ethereum")
```

**Travel Planning**
```python
# Check weather
weather_search("Paris", "FR")

# Get exchange rates
get_exchange_rate("USD", "EUR")

# Find travel news
news_search("Paris travel", count=5)
```

**News Research**
```python
# Search for specific news
news_search("AI regulations")

# Get tech headlines  
news_by_category("technology", "us")

# Deep web search
tavily_search("quantum computing", max_results=10)
```

**Market Research**
```python
# Track crypto trends
get_crypto_prices("bitcoin,ethereum,solana")

# Research market news
news_by_category("business", "us")

# Web search for opportunities
tavily_search("emerging tech 2024")
```

## 🚀 Server Output

When started, the server logs:
- ✅ Available tools
- 📋 Available prompts
- 🔐 Required environment variables
- 📊 API response status

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "API_KEY not configured" | Export environment variable |
| "API request failed" | Check internet connection |
| Rate limit exceeded | Use paid API tier or wait |
| Timeout errors | Check API endpoint status |

## 📊 Performance Tips

- Cache exchange rates (they change slowly)
- Batch crypto price requests
- Use specific dates for historical rates
- Set max_results to limit data

## 🔗 Resources

- Frankfurter API: https://www.frankfurter.app
- Tavily AI: https://tavily.com
- NewsAPI: https://newsapi.org
- CoinGecko: https://www.coingecko.com/api/documentation
- wttr.in: https://wttr.in

---

**Ready to use!** Start with free-tier APIs (exchange rates, crypto, weather), then add API keys as needed.
