# MySQL MCP Server 🗄️ 

## Overview
A comprehensive FastMCP-based server providing both MySQL database operations and currency conversion features. This multi-purpose server combines database management with financial data integration, supporting currency exchange rates and cryptocurrency prices.

## Features
- **MySQL Integration**: Full database query execution and management
- **Currency Exchange**: Real-time currency conversion
- **Cryptocurrency Prices**: Real-time crypto market data
- **Web Search Integration**: Tavily API integration for information search
- **Connection Pooling**: Efficient database connection management
- **Async Operations**: Full async/await support

## Tools Available

### Database Operations
- Execute SQL queries
- List databases
- List tables
- Insert, update, delete operations
- Complex query support with aggregations

### Financial Tools
- `get_exchange_rate(from_currency, to_currency)` - Get current exchange rates
- `get_crypto_prices(symbols, vs_currency)` - Get cryptocurrency prices
- `tavily_search(query, max_results)` - Web search integration

### Leave Management (Example)
- `get_leave_balance(employee_id)` - Check leave days
- Employee leave tracking

## Setup & Usage

### Installation
```bash
pip install fastmcp mysql-connector-python httpx python-dotenv
```

### Configuration
Create `.env` file with:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_PORT=3306

TAVILY_API_KEY=your_tavily_key
```

### Configuration File
Database config in `currency_mcp_server.py`:
```python
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "port": 3306,
    "autocommit": True,
}
```

### Running the Server

#### Stdio Transport (Claude Desktop)
```bash
python currency_mcp_server.py
```

#### SSE Transport (HTTP)
```bash
# Typically serves on http://localhost:7080/sse
```

## Files
- `currency_mcp_server.py` - Main server implementation with all tools
- `mcp_client.py` - Test client for server testing
- `requirements.txt` - Python dependencies
- `requirements_mcp.txt` - MCP-specific dependencies
- `.env.example` - Example environment configuration
- `SETUP_GUIDE.md` - Detailed setup instructions
- `QUICK_REFERENCE.md` - Quick API reference
- Various documentation files

## Database Operations

### Connection Management
```python
# Automatic connection pooling
# Handles connection lifecycle
# Supports transaction management
```

### Query Execution
```python
# Execute any SQL query
# Supports:
# - SELECT with complex joins
# - INSERT/UPDATE/DELETE operations
# - Stored procedures
# - Aggregations and grouping
```

## Currency & Crypto Integration

### Exchange Rates
- Real-time currency conversion
- Support for 150+ currencies
- Direct conversion without intermediaries
- USD, EUR, GBP, JPY, CAD, and more

### Cryptocurrency Data
- Real-time crypto prices
- Support for major coins: Bitcoin, Ethereum, Cardano, etc.
- Multiple currency quotes (USD, EUR, GBP, etc.)
- Market data and trends

## Use Cases
- **Financial Reporting**: Currency conversion for international reports
- **E-commerce**: Real-time pricing in multiple currencies
- **Investments**: Track crypto and forex prices
- **HR Systems**: Leave management integration
- **Data Analysis**: Query databases for insights
- **Multi-currency Apps**: Seamless currency handling

## API Examples

### Currency Conversion
```python
result = get_exchange_rate("USD", "GBP")
# Returns: {"rate": 0.7479, "from": "USD", "to": "GBP"}
```

### Crypto Prices
```python
prices = get_crypto_prices("bitcoin,ethereum", "usd")
# Returns: {
#   "bitcoin": 65000,
#   "ethereum": 2800
# }
```

### Web Search
```python
results = tavily_search("EUR USD exchange rate", 5)
# Returns: [list of relevant search results]
```

## Security Features
- **Parameterized Queries**: SQL injection prevention
- **Error Handling**: No sensitive info in errors
- **Connection Security**: SSL/TLS support
- **Credential Management**: Environment-based credentials
- **Input Validation**: Type checking and sanitization

## Error Handling
- Connection error recovery
- Query timeout management
- API availability checks
- Graceful fallbacks
- Detailed error logging

## Performance
- Connection pooling
- Async query execution
- Caching for frequently used rates
- Optimized external API calls
- Load balancing support

## Documentation
Comprehensive documentation included:
- `SETUP_GUIDE.md` - Step-by-step setup
- `QUICK_REFERENCE.md` - API quick reference
- `PRACTICAL_GUIDE.md` - Real-world examples
- `IMPLEMENTATION_SUMMARY.md` - Technical details

## Dependencies
- fastmcp (FastMCP framework)
- mysql-connector-python (MySQL driver)
- httpx (Async HTTP client)
- python-dotenv (Environment management)
- mcp (MCP protocol)

## Testing
Use provided `mcp_client.py` for testing:
```bash
python mcp_client.py
```

## Troubleshooting
- Check MySQL connection settings
- Verify API keys in .env
- Review logs for detailed errors
- Consult documentation files

## Future Enhancements
- Support for additional databases (PostgreSQL, MongoDB)
- More cryptocurrency data sources
- Advanced financial calculations
- Batch operations
- Caching layer for better performance
