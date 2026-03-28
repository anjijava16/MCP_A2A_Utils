# Multi-Purpose Information MCP Server with MySQL Integration 🌐

A comprehensive Model Context Protocol (MCP) server providing tools for financial data, web search, cryptocurrency tracking, weather information, and **complete MySQL database management** with DDL, DML, and SELECT operations.

## Features

### 🌍 Financial & Information Tools
- **Exchange Rates**: Real-time currency conversion using Frankfurter API
- **Web Search**: Tavily AI-powered web search with answers
- **Cryptocurrency**: CoinGecko price tracking and market data
- **Weather**: Real-time weather information for any location

### 🗄️ MySQL Database Management Tools

#### DDL Operations (Data Definition Language)
- **Create/Drop Databases**: Full database lifecycle management
- **Create/Drop Tables**: Table schema creation and deletion
- **Alter Tables**: Modify table structures dynamically
- **Describe Tables**: View table schemas and column information
- **List Databases/Tables**: Inventory all databases and tables

#### DML Operations (Data Manipulation Language)
- **Insert Records**: Single and bulk insert operations
- **Update Records**: Modify existing data with conditions
- **Delete Records**: Remove data with optional WHERE clauses

#### SELECT Operations (Data Retrieval)
- **Select All**: Retrieve all records from a table
- **Select with Conditions**: Query specific data using WHERE clauses
- **Count Records**: Get record counts with optional conditions
- **Distinct Values**: Find unique values in columns
- **Aggregate Functions**: SUM, AVG, MIN, MAX operations
- **Ordered Selection**: Sort results in ascending/descending order
- **Grouped Selection**: GROUP BY queries with aggregates
- **Custom Queries**: Execute any SQL query

### 👥 Role-Based Prompts

1. **financial_analyst_prompt**: Market analysis and financial insights
2. **investment_advisor_prompt**: Investment recommendations
3. **travel_planner_prompt**: Travel planning assistance
4. **market_researcher_prompt**: Comprehensive market research
5. **weather_analyst_prompt**: Weather-based planning
6. **database_administrator_prompt**: Database management and optimization
7. **data_analyst_prompt**: Data analysis and reporting
8. **data_engineer_prompt**: ETL and data pipeline design
9. **developer_database_prompt**: Application development with databases
10. **business_analyst_prompt**: Business intelligence and insights
11. **database_designer_prompt**: Schema design and optimization

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server (8.0+)
- pip (Python package manager)

### Setup

1. **Clone/Download the repository**
```bash
cd mcp_server
```

2. **Create Python virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

### MySQL Configuration
The server uses these default credentials:
- **Host**: localhost
- **User**: root
- **Password**: Maxis@123
- **Port**: 3306

Update these in your `.env` file or pass as environment variables.

## Running the Server

```bash
python currency_mcp_server.py
```

The server will start on `0.0.0.0:7080` by default.

## Tool Usage Examples

### 1. Database Management

#### Create a database
```python
mysql_create_database(database_name="myapp_db")
```

#### Create a table
```python
mysql_create_table(
    database_name="myapp_db",
    table_name="users",
    columns="""
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE,
        age INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
)
```

#### List all databases
```python
mysql_list_databases()
# Returns: {'success': True, 'databases': ['mysql', 'myapp_db', ...]}
```

### 2. Data Insertion

#### Insert single record
```python
mysql_insert_record(
    database_name="myapp_db",
    table_name="users",
    column_values="(name, email, age) VALUES ('John Doe', 'john@example.com', 30)"
)
# Returns: {'success': True, 'message': 'Record inserted successfully', 'id': 1}
```

#### Insert multiple records
```python
mysql_insert_multiple_records(
    database_name="myapp_db",
    table_name="users",
    records="""(name, email, age) VALUES 
        ('Jane Doe', 'jane@example.com', 28),
        ('Bob Smith', 'bob@example.com', 35),
        ('Alice Johnson', 'alice@example.com', 32)"""
)
# Returns: {'success': True, 'message': '3 records inserted successfully', 'rows_affected': 3}
```

### 3. Data Queries

#### Select all records
```python
mysql_select_all(
    database_name="myapp_db",
    table_name="users",
    limit=100
)
# Returns: {'success': True, 'records': [...], 'count': 4}
```

#### Select with conditions
```python
mysql_select_where(
    database_name="myapp_db",
    table_name="users",
    where_clause="age > 30",
    columns="name, email, age"
)
# Returns matching records with specified columns
```

#### Select with sorting
```python
mysql_select_ordered(
    database_name="myapp_db",
    table_name="users",
    order_by="age",
    ascending=False,
    limit=10
)
# Returns records ordered by age (descending)
```

#### Get count
```python
mysql_select_count(
    database_name="myapp_db",
    table_name="users",
    where_clause="age > 25"
)
# Returns: {'success': True, 'count': 3}
```

### 4. Data Aggregation

#### Calculate aggregate values
```python
mysql_select_aggregate(
    database_name="myapp_db",
    table_name="users",
    aggregate_function="AVG",
    column="age"
)
# Returns average age of all users

mysql_select_aggregate(
    database_name="myapp_db",
    table_name="users",
    aggregate_function="SUM",
    column="age",
    where_clause="created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)"
)
# Returns sum of ages for users created in last 30 days
```

#### Group and aggregate
```python
mysql_select_grouped(
    database_name="myapp_db",
    table_name="users",
    group_by_column="age",
    aggregate_function="COUNT"
)
# Returns count of users by age group
```

### 5. Data Updates

#### Update records
```python
mysql_update_records(
    database_name="myapp_db",
    table_name="users",
    set_clause="age=31, updated_at=NOW()",
    where_clause="name='John Doe'"
)
# Returns: {'success': True, 'rows_affected': 1}
```

### 6. Data Deletion

#### Delete records
```python
mysql_delete_records(
    database_name="myapp_db",
    table_name="users",
    where_clause="age < 18"
)
# Returns count of deleted records
```

### 7. Custom Queries

#### Execute custom SQL
```python
mysql_custom_query(
    database_name="myapp_db",
    query="SELECT u.name, COUNT(o.id) as order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id"
)
# Executes any SQL query and returns results
```

## Use Case Examples

### Data Analyst Role
```
Prompt: "I need to analyze user demographics in our database"
- Use mysql_select_grouped() to group users by age
- Use mysql_select_aggregate() to calculate statistics
- Use mysql_select_where() to filter specific cohorts
```

### Database Administrator Role
```
Prompt: "Set up a new customer database with proper schema"
- Use mysql_create_database() for database creation
- Use mysql_create_table() with proper constraints
- Use mysql_describe_table() to verify structure
```

### Developer Role
```
Prompt: "Create a users table and add test data"
- Use mysql_create_table() with appropriate columns
- Use mysql_insert_multiple_records() for test data
- Use mysql_select_all() to verify insertion
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Never commit `.env` files** with real credentials
2. **Use environment variables** for sensitive data
3. **Implement rate limiting** in production
4. **Use parameterized queries** when building dynamic SQL
5. **Validate input data** before database operations
6. **Use proper authentication** for database access
7. **Enable SSL/TLS** for remote MySQL connections
8. **Implement proper access control** at database level
9. **Monitor query logs** for suspicious activity
10. **Regular backups** of critical data

## Environment Variables

```env
# MySQL Connection
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Maxis@123
MYSQL_PORT=3306

# API Keys
TAVILY_API_KEY=your_api_key

# Server Configuration
PORT=7080
```

## Response Format

All tools return consistent JSON responses:

```json
{
  "success": true/false,
  "message": "Operation description",
  "data": {...},
  "error": "Error message if failed"
}
```

## Troubleshooting

### MySQL Connection Issues
```
Error: "MySQL connection error"
- Check MySQL server is running
- Verify credentials in .env
- Ensure MySQL is accessible on specified host:port
```

### Table Not Found
```
Error: "no such table"
- Verify correct database name
- Verify correct table name
- Use mysql_list_tables() to see available tables
```

### Query Syntax Errors
```
Error: "Syntax error in SQL statement"
- Check column names are properly backtick-quoted
- Verify WHERE clause syntax
- Test query in MySQL client first
```

## Performance Tips

1. **Use LIMIT** to restrict large result sets
2. **Create indexes** on frequently queried columns
3. **Use WHERE clauses** to filter early
4. **Use aggregate functions** instead of client-side processing
5. **Monitor slow queries** with MySQL slow query log
6. **Connection pooling** for high-traffic applications

## Available Prompts

Each prompt is designed for specific use cases:

- **database_administrator_prompt**: Full database management
- **data_analyst_prompt**: Analyzing and reporting on data
- **data_engineer_prompt**: Building ETL pipelines
- **developer_database_prompt**: Application development
- **business_analyst_prompt**: Business intelligence
- **database_designer_prompt**: Schema and architecture design

## License

MIT License

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review MySQL documentation
3. Verify database connectivity
4. Check application logs

---

**Last Updated**: March 2026
**Version**: 2.0
**MySQL Compatibility**: 5.7+
