# Multi-Purpose Information MCP Server Setup Guide

## Overview
This MCP server provides comprehensive tools for financial analysis, news research, cryptocurrency tracking, weather information, and web search capabilities.

## Available Tools

### 1. **get_exchange_rate**
- **Description**: Get current currency exchange rates
- **Parameters**:
  - `currency_from` (str): Source currency code (default: "USD")
  - `currency_to` (str): Target currency code (default: "EUR")
  - `currency_date` (str): Date for rate or "latest" (default: "latest")
- **API**: Frankfurter (free, no key required)
- **Use Cases**: Currency conversion, forex analysis, travel planning

### 2. **tavily_search** ⭐
- **Description**: Web search using Tavily AI search engine
- **Parameters**:
  - `query` (str): Search query
  - `include_answer` (bool): Include direct answer (default: True)
  - `max_results` (int): Max results 1-20 (default: 5)
- **API**: Tavily AI
- **Required**: TAVILY_API_KEY environment variable
- **Use Cases**: Deep web research, fact-checking, market research

### 3. **news_search**
- **Description**: Search for news articles by keyword
- **Parameters**:
  - `query` (str): Search query for news
  - `sort_by` (str): 'relevancy', 'popularity', or 'publishedAt' (default: "relevancy")
  - `language` (str): Language code (default: "en")
  - `count` (int): Number of articles (max: 100, default: 10)
- **API**: NewsAPI
- **Required**: NEWS_API_KEY environment variable
- **Use Cases**: News research, trend analysis, current events

### 4. **news_by_category**
- **Description**: Get top headlines by category and country
- **Parameters**:
  - `category` (str): Category type - business, entertainment, general, health, science, sports, technology (default: "general")
  - `country` (str): Country code - us, gb, ca, au, de, fr, in, jp, br, etc. (default: "us")
  - `count` (int): Number of articles (max: 100, default: 10)
- **API**: NewsAPI
- **Required**: NEWS_API_KEY environment variable
- **Use Cases**: Following trends, market news, industry updates

### 5. **get_crypto_prices**
- **Description**: Get cryptocurrency prices and market data
- **Parameters**:
  - `symbols` (str): Crypto IDs comma-separated (default: "bitcoin,ethereum")
  - `vs_currency` (str): Target currency (default: "usd")
- **API**: CoinGecko (free, no key required)
- **Use Cases**: Crypto tracking, investment analysis, market monitoring

### 6. **weather_search**
- **Description**: Get current weather information for cities
- **Parameters**:
  - `city` (str): City name
  - `country_code` (str, optional): ISO 3166 country code
- **API**: wttr.in (free, no key required)
- **Use Cases**: Travel planning, event planning, weather alerts

## Available Prompts

### 1. **financial_analyst_prompt**
- Expert financial analysis and market research
- Guides analysis of exchange rates, crypto, and financial news
- Provides insights and recommendations

### 2. **news_journalist_prompt**
- Investigative journalism and news research
- Focuses on finding, comparing, and verifying news stories
- Emphasizes attribution and sourcing

### 3. **investment_advisor_prompt**
- Professional investment advice and analysis
- Covers crypto, currencies, and economic news
- Includes risk assessment guidelines

### 4. **travel_planner_prompt**
- Expert travel planning and advice
- Combines currency rates, weather, and travel news
- Provides practical travel recommendations

### 5. **market_researcher_prompt**
- Comprehensive market trend analysis
- Focuses on opportunities and competitive landscape
- Analyzes blockchain, forex, and emerging technologies

### 6. **weather_analyst_prompt**
- Weather forecasting and climate analysis
- Identification of weather patterns and impacts
- Safety and preparedness recommendations

## Environment Variables Setup

### Required for Web Search
```bash
export TAVILY_API_KEY="your_tavily_api_key_here"
```
Get key from: https://tavily.com

### Required for News Features
```bash
export NEWS_API_KEY="your_newsapi_key_here"
```
Get key from: https://newsapi.org

### Optional
```bash
export PORT=7080  # Custom port (default: 7080)
export RAPIDAPI_KEY="your_rapidapi_key"  # For future enhancements
```

## Installation

1. **Install Dependencies**:
```bash
pip install fastmcp httpx
```

2. **Set Environment Variables**:
```bash
# Add to your shell profile or use .env file
export TAVILY_API_KEY="your_key"
export NEWS_API_KEY="your_key"
export PORT=7080
```

3. **Run the Server**:
```bash
python currency_mcp_server.py
```

Or with a specific port:
```bash
PORT=8000 python currency_mcp_server.py
```

## API Keys & Free Options

| Tool | API | Free Tier | Notes |
|------|-----|-----------|-------|
| Exchange Rates | Frankfurter | ✅ Unlimited | No key required |
| Web Search | Tavily | 🟡 Limited | Sign up for free tier |
| News | NewsAPI | 🟡 Limited | Free tier available |
| Crypto Prices | CoinGecko | ✅ Unlimited | No key required |
| Weather | wttr.in | ✅ Unlimited | No key required |

## Usage Examples

### Currency Conversion
```python
# Get USD to EUR rate
get_exchange_rate(currency_from="USD", currency_to="EUR")
```

### Web Search with Tavily
```python
# Search for AI trends
tavily_search("artificial intelligence trends 2024", max_results=10)
```

### News Research
```python
# Search for specific news
news_search("cryptocurrency regulation")

# Get tech news from US
news_by_category(category="technology", country="us", count=20)
```

### Crypto Tracking
```python
# Get prices for multiple cryptos
get_crypto_prices(symbols="bitcoin,ethereum,cardano,solana", vs_currency="usd")
```

### Weather Check
```python
# Check weather in London, UK
weather_search(city="London", country_code="GB")
```

## Combining Tools & Prompts

Use prompts to guide agent behavior with specific tools:

1. **Financial Analysis**: Use `financial_analyst_prompt` with exchange rates, crypto prices, and financial news
2. **News Research**: Use `news_journalist_prompt` with news_search, news_by_category, and tavily_search
3. **Investment Planning**: Use `investment_advisor_prompt` with crypto prices, currency rates, and economic news
4. **Travel Planning**: Use `travel_planner_prompt` with weather, exchange rates, and travel news
5. **Market Research**: Use `market_researcher_prompt` with all search and news tools

## Troubleshooting

### Missing API Keys
- Error: "API_KEY not configured"
- Solution: Export the required environment variable (see Environment Variables Setup)

### Rate Limiting
- Some APIs have rate limits on free tiers
- Solutions:
  - Use free-tier APIs first (currencies, crypto, weather)
  - Implement request queuing for paid APIs
  - Consider paid tier for production use

### Network Issues
- Error: "API request failed"
- Solutions:
  - Check internet connection
  - Verify API endpoint is accessible
  - Check firewall/proxy settings

## Performance Optimization

1. **Cache Results**: Store exchange rates and weather data
2. **Batch Requests**: Combine multiple crypto symbols in one call
3. **Rate Limiting**: Implement exponential backoff for retries
4. **Timeout**: Requests timeout after 10 seconds by default

## Future Enhancements

- [ ] Add stock market data (Alpha Vantage)
- [ ] Add social media sentiment analysis
- [ ] Add predictive analytics
- [ ] Add multi-language support
- [ ] Add database caching layer
- [ ] Add authentication/authorization
- [ ] Add API usage analytics
- [ ] Add webhook support

## Logging

The server provides detailed logging:
- 🛠️ Tool invocations
- ✅ Successful API responses
- ❌ Errors and failures
- 📊 Performance metrics

View logs in console output when running the server.

## Support & Resources

- FastMCP Documentation: https://github.com/jlopp/fastmcp
- Tavily API Docs: https://tavily.com/api
- NewsAPI Docs: https://newsapi.org
- CoinGecko API: https://www.coingecko.com/api
- wttr.in: https://wttr.in

---

**Last Updated**: 2026-03-26
**Version**: 1.0
