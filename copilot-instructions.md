# Copilot Instructions

You have access to the following MCP tools through the `fastmcp-local` server at `http://localhost:7080/mcp`:

## Available Tools

### 1. **tavily_search** - Web Search
Search the web using Tavily AI search engine to find information, news, and answers.

**Parameters:**
- `query` (string, required): The search query
- `include_answer` (boolean, optional): Include a direct answer to the query
- `max_results` (integer, optional): Maximum number of results (1-20)

**When to use:** User asks for information about current events, news, product reviews, research, or anything requiring web search.

### 2. **get_crypto_prices** - Cryptocurrency Prices
Get real-time cryptocurrency prices using CoinGecko API (no authentication required).

**Parameters:**
- `symbols` (string, required): Comma-separated cryptocurrency IDs (e.g., 'bitcoin,ethereum,cardano')
- `vs_currency` (string, required): Target currency (e.g., 'usd', 'eur', 'gbp')

**When to use:** User asks for current crypto prices, market data, or cryptocurrency valuations.

### 3. **get_exchange_rate** - Foreign Exchange Rates
Get current or historical exchange rates between currencies.

**Parameters:**
- `currency_from` (string, required): Source currency code (e.g., 'USD')
- `currency_to` (string, required): Target currency code (e.g., 'EUR')
- `currency_date` (string, optional): Date for the rate or 'latest' (default: 'latest')

**When to use:** User asks for currency conversion, exchange rates, or currency information.

### 4. **weather_search** - Weather Information
Get current weather information for any location.

**Parameters:**
- `city` (string, required): City name (e.g., 'London', 'New York')
- `country_code` (string, optional): ISO 3166 country code (e.g., 'GB', 'US')

**When to use:** User asks about current weather, temperature, or weather conditions.

## MCP Server Status

The MCP server is configured in `.vscode/mcp.json` and runs at `http://localhost:7080/mcp`.

Make sure the server is running before using any of these tools. If you encounter session errors, the server may need to be restarted.
