import asyncio
import logging
import os
import json
from typing import Optional, List, Dict, Any

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    Error = Exception

import httpx
from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Multi-Purpose Information MCP Server 🌐")

# API Keys from environment
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ============================================================================
# MYSQL DATABASE CONFIGURATION
# ============================================================================
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "Maxis@123"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "autocommit": True,
}


def get_mysql_connection(database: Optional[str] = None):
    """Create and return a MySQL database connection."""
    if not MYSQL_AVAILABLE:
        raise ImportError(
            "mysql-connector-python is not installed. "
            "Install with: pip install mysql-connector-python"
        )
    try:
        config = MYSQL_CONFIG.copy()
        if database:
            config["database"] = database
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            logger.info("✅ MySQL connection established")
        return connection
    except Error as e:
        logger.error(f"❌ MySQL connection error: {e}")
        raise


# ============================================================================
# FINANCIAL & INFORMATION TOOLS
# ============================================================================

@mcp.tool()
def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Use this to get current exchange rate.

    Args:
        currency_from: The currency to convert from (e.g., "USD").
        currency_to: The currency to convert to (e.g., "EUR").
        currency_date: The date for the exchange rate or "latest". Defaults to "latest".

    Returns:
        A dictionary containing the exchange rate data, or an error message if the request fails.
    """
    logger.info(
        f"--- 🛠️ Tool: get_exchange_rate called for converting {currency_from} to {currency_to} ---"
    )
    try:
        response = httpx.get(
            f"https://api.frankfurter.app/{currency_date}",
            params={"from": currency_from, "to": currency_to},
        )
        response.raise_for_status()

        data = response.json()
        if "rates" not in data:
            logger.error(f"❌ rates not found in response: {data}")
            return {"error": "Invalid API response format."}
        logger.info(f"✅ API response: {data}")
        return data
    except httpx.HTTPError as e:
        logger.error(f"❌ API request failed: {e}")
        return {"error": f"API request failed: {e}"}
    except ValueError:
        logger.error("❌ Invalid JSON response from API")
        return {"error": "Invalid JSON response from API."}


@mcp.tool()
def tavily_search(query: str, include_answer: bool = True, max_results: int = 5):
    """Search the web using Tavily AI search engine.

    Args:
        query: The search query string.
        include_answer: Whether to include a direct answer to the query.
        max_results: Maximum number of results to return (1-20).

    Returns:
        A dictionary containing search results and optionally an answer.
    """
    logger.info(f"--- 🔍 Tool: tavily_search called with query: {query} ---")

    if not TAVILY_API_KEY:
        logger.error("❌ TAVILY_API_KEY not configured")
        return {"error": "TAVILY_API_KEY not configured. Set it as an environment variable."}

    try:
        response = httpx.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "include_answer": include_answer,
                "max_results": max_results,
            },
            timeout=10.0,
        )
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Tavily search results: {len(data.get('results', []))} found")
        return data
    except httpx.HTTPError as e:
        logger.error(f"❌ Tavily API request failed: {e}")
        return {"error": f"Tavily search failed: {e}"}
    except Exception as e:
        logger.error(f"❌ Unexpected error in tavily_search: {e}")
        return {"error": f"Unexpected error: {e}"}


@mcp.tool()
def get_crypto_prices(
    symbols: str = "bitcoin,ethereum",
    vs_currency: str = "usd",
):
    """Get cryptocurrency prices using CoinGecko API (no key required).

    Args:
        symbols: Comma-separated cryptocurrency IDs (e.g., 'bitcoin,ethereum,cardano').
        vs_currency: Currency to get prices in (e.g., 'usd', 'eur', 'gbp').

    Returns:
        A dictionary containing cryptocurrency prices and market data.
    """
    logger.info(f"--- 💰 Tool: get_crypto_prices called for {symbols} ---")

    try:
        response = httpx.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": symbols,
                "vs_currencies": vs_currency,
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true",
            },
            timeout=10.0,
        )
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Crypto prices retrieved: {list(data.keys())}")
        return data
    except httpx.HTTPError as e:
        logger.error(f"❌ CoinGecko API request failed: {e}")
        return {"error": f"Failed to fetch crypto prices: {e}"}
    except Exception as e:
        logger.error(f"❌ Error in get_crypto_prices: {e}")
        return {"error": f"Unexpected error: {e}"}


@mcp.tool()
def weather_search(
    city: str,
    country_code: Optional[str] = None,
):
    """Get current weather information for a city.

    Args:
        city: City name (e.g., 'London', 'New York').
        country_code: Optional ISO 3166 country code (e.g., 'GB', 'US').

    Returns:
        A dictionary containing current weather data.
    """
    logger.info(f"--- 🌤️ Tool: weather_search called for {city} ---")

    try:
        location = f"{city},{country_code}" if country_code else city
        response = httpx.get(
            "https://wttr.in",
            params={"q": location, "format": "j1"},
            timeout=10.0,
        )
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ Weather data retrieved for {city}")
        return data
    except httpx.HTTPError as e:
        logger.error(f"❌ Weather API request failed: {e}")
        return {"error": f"Failed to fetch weather: {e}"}
    except Exception as e:
        logger.error(f"❌ Error in weather_search: {e}")
        return {"error": f"Unexpected error: {e}"}


# ============================================================================
# MYSQL DDL TOOLS (8 tools)
# ============================================================================

@mcp.tool()
def mysql_create_database(database_name: str, charset: str = "utf8mb4", collation: str = "utf8mb4_unicode_ci"):
    """Create a new MySQL database.

    Args:
        database_name: Name of the database to create.
        charset: Character set for the database (default: utf8mb4).
        collation: Collation for the database (default: utf8mb4_unicode_ci).

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🗄️ Tool: mysql_create_database called for '{database_name}' ---")
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET {charset} COLLATE {collation}"
        cursor.execute(sql)
        cursor.close()
        conn.close()
        logger.info(f"✅ Database '{database_name}' created successfully")
        return {"success": True, "message": f"Database '{database_name}' created successfully", "database": database_name}
    except Exception as e:
        logger.error(f"❌ Error creating database: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_drop_database(database_name: str, confirm: bool = False):
    """Drop (delete) an existing MySQL database.

    Args:
        database_name: Name of the database to drop.
        confirm: Must be True to confirm deletion. Safety check to prevent accidental drops.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🗑️ Tool: mysql_drop_database called for '{database_name}' ---")
    if not confirm:
        return {"success": False, "error": "Set confirm=True to confirm database deletion. This action is irreversible."}
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{database_name}`")
        cursor.close()
        conn.close()
        logger.info(f"✅ Database '{database_name}' dropped successfully")
        return {"success": True, "message": f"Database '{database_name}' dropped successfully"}
    except Exception as e:
        logger.error(f"❌ Error dropping database: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_list_databases():
    """List all available MySQL databases.

    Returns:
        A dictionary containing a list of all databases.
    """
    logger.info("--- 📋 Tool: mysql_list_databases called ---")
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(databases)} databases")
        return {"success": True, "databases": databases, "count": len(databases)}
    except Exception as e:
        logger.error(f"❌ Error listing databases: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_create_table(database_name: str, table_name: str, columns: str, extra_options: str = ""):
    """Create a new table in a MySQL database.

    Args:
        database_name: Name of the database where the table will be created.
        table_name: Name of the table to create.
        columns: Column definitions as SQL string.
                 Example: "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(255) UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        extra_options: Optional table options such as ENGINE, CHARSET.
                       Example: "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🏗️ Tool: mysql_create_table called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})"
        if extra_options:
            sql += f" {extra_options}"
        cursor.execute(sql)
        cursor.close()
        conn.close()
        logger.info(f"✅ Table '{table_name}' created successfully in '{database_name}'")
        return {"success": True, "message": f"Table '{table_name}' created successfully", "database": database_name, "table": table_name}
    except Exception as e:
        logger.error(f"❌ Error creating table: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_drop_table(database_name: str, table_name: str, confirm: bool = False):
    """Drop (delete) an existing table from a MySQL database.

    Args:
        database_name: Name of the database containing the table.
        table_name: Name of the table to drop.
        confirm: Must be True to confirm deletion. Safety check.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🗑️ Tool: mysql_drop_table called for '{database_name}.{table_name}' ---")
    if not confirm:
        return {"success": False, "error": "Set confirm=True to confirm table deletion. This action is irreversible."}
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        cursor.close()
        conn.close()
        logger.info(f"✅ Table '{table_name}' dropped successfully")
        return {"success": True, "message": f"Table '{table_name}' dropped successfully"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_alter_table(database_name: str, table_name: str, alter_statement: str):
    """Modify an existing table structure using ALTER TABLE.

    Args:
        database_name: Name of the database containing the table.
        table_name: Name of the table to alter.
        alter_statement: The ALTER TABLE clause(s) to execute.
                         Examples:
                           "ADD COLUMN age INT DEFAULT 0"
                           "DROP COLUMN old_column"
                           "MODIFY COLUMN name VARCHAR(200) NOT NULL"
                           "ADD INDEX idx_email (email)"
                           "ADD COLUMN phone VARCHAR(20), ADD COLUMN address TEXT"

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🔧 Tool: mysql_alter_table called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        sql = f"ALTER TABLE `{table_name}` {alter_statement}"
        cursor.execute(sql)
        cursor.close()
        conn.close()
        logger.info(f"✅ Table '{table_name}' altered successfully")
        return {"success": True, "message": f"Table '{table_name}' altered successfully", "applied": alter_statement}
    except Exception as e:
        logger.error(f"❌ Error altering table: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_list_tables(database_name: str):
    """List all tables in a MySQL database.

    Args:
        database_name: Name of the database to list tables from.

    Returns:
        A dictionary containing a list of table names.
    """
    logger.info(f"--- 📋 Tool: mysql_list_tables called for database '{database_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(tables)} tables in '{database_name}'")
        return {"success": True, "database": database_name, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_describe_table(database_name: str, table_name: str):
    """Describe the structure of a MySQL table (columns, types, constraints).

    Args:
        database_name: Name of the database containing the table.
        table_name: Name of the table to describe.

    Returns:
        A dictionary containing column details: Field, Type, Null, Key, Default, Extra.
    """
    logger.info(f"--- 🔍 Tool: mysql_describe_table called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"✅ Table '{table_name}' described: {len(columns)} columns")
        return {"success": True, "database": database_name, "table": table_name, "columns": columns, "column_count": len(columns)}
    except Exception as e:
        logger.error(f"❌ Error describing table: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# MYSQL DML TOOLS (4 tools)
# ============================================================================

@mcp.tool()
def mysql_insert_record(database_name: str, table_name: str, data: Dict[str, Any]):
    """Insert a single record into a MySQL table.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to insert into.
        data: Dictionary of column-value pairs to insert.
              Example: {"name": "John Doe", "email": "john@example.com", "age": 30}

    Returns:
        A dictionary with the inserted row's ID and success status.
    """
    logger.info(f"--- ➕ Tool: mysql_insert_record called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        columns = ", ".join(f"`{col}`" for col in data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        inserted_id = cursor.lastrowid
        cursor.close()
        conn.close()
        logger.info(f"✅ Record inserted into '{table_name}' with ID {inserted_id}")
        return {"success": True, "message": "Record inserted successfully", "inserted_id": inserted_id, "table": table_name}
    except Exception as e:
        logger.error(f"❌ Error inserting record: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_insert_multiple_records(database_name: str, table_name: str, records: List[Dict[str, Any]]):
    """Bulk insert multiple records into a MySQL table.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to insert into.
        records: List of dictionaries, each representing a row.
                 Example: [
                   {"name": "Alice", "email": "alice@example.com"},
                   {"name": "Bob", "email": "bob@example.com"}
                 ]
                 All dictionaries must have the same keys.

    Returns:
        A dictionary with the number of records inserted and success status.
    """
    logger.info(f"--- ➕ Tool: mysql_insert_multiple_records called for '{database_name}.{table_name}' ---")
    if not records:
        return {"success": False, "error": "No records provided for insertion."}
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        columns = ", ".join(f"`{col}`" for col in records[0].keys())
        placeholders = ", ".join(["%s"] * len(records[0]))
        sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        values = [list(record.values()) for record in records]
        cursor.executemany(sql, values)
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        logger.info(f"✅ {rows_affected} records inserted into '{table_name}'")
        return {"success": True, "message": f"{rows_affected} records inserted successfully", "rows_inserted": rows_affected, "table": table_name}
    except Exception as e:
        logger.error(f"❌ Error bulk inserting records: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_update_records(database_name: str, table_name: str, updates: Dict[str, Any], condition: str):
    """Update existing records in a MySQL table based on a condition.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to update.
        updates: Dictionary of column-value pairs to update.
                 Example: {"email": "newemail@example.com", "age": 31}
        condition: SQL WHERE clause (without the WHERE keyword) to filter rows.
                   Example: "id = 5"
                   Example: "status = 'inactive' AND created_at < '2023-01-01'"
                   Use "1=1" to update all records (use with caution).

    Returns:
        A dictionary with the number of rows affected and success status.
    """
    logger.info(f"--- ✏️ Tool: mysql_update_records called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        set_clause = ", ".join(f"`{col}` = %s" for col in updates.keys())
        sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {condition}"
        cursor.execute(sql, list(updates.values()))
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        logger.info(f"✅ {rows_affected} records updated in '{table_name}'")
        return {"success": True, "message": f"{rows_affected} records updated successfully", "rows_affected": rows_affected, "table": table_name}
    except Exception as e:
        logger.error(f"❌ Error updating records: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_delete_records(database_name: str, table_name: str, condition: str, confirm: bool = False):
    """Delete records from a MySQL table based on a condition.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to delete from.
        condition: SQL WHERE clause (without the WHERE keyword) to identify rows to delete.
                   Example: "id = 10"
                   Example: "status = 'deleted' AND last_login < '2022-01-01'"
        confirm: Must be True to confirm deletion. Safety check.

    Returns:
        A dictionary with the number of rows deleted and success status.
    """
    logger.info(f"--- 🗑️ Tool: mysql_delete_records called for '{database_name}.{table_name}' ---")
    if not confirm:
        return {"success": False, "error": "Set confirm=True to confirm deletion. This action is irreversible."}
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        sql = f"DELETE FROM `{table_name}` WHERE {condition}"
        cursor.execute(sql)
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        logger.info(f"✅ {rows_affected} records deleted from '{table_name}'")
        return {"success": True, "message": f"{rows_affected} records deleted successfully", "rows_deleted": rows_affected, "table": table_name}
    except Exception as e:
        logger.error(f"❌ Error deleting records: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# MYSQL SELECT TOOLS (8 tools)
# ============================================================================

@mcp.tool()
def mysql_select_all(database_name: str, table_name: str, limit: int = 100, offset: int = 0):
    """Select all records from a MySQL table with optional pagination.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to query.
        limit: Maximum number of records to return (default: 100).
        offset: Number of records to skip for pagination (default: 0).

    Returns:
        A dictionary containing the records and row count.
    """
    logger.info(f"--- 🔎 Tool: mysql_select_all called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s", (limit, offset))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} records from '{table_name}'")
        return {"success": True, "table": table_name, "records": records, "count": len(records), "limit": limit, "offset": offset}
    except Exception as e:
        logger.error(f"❌ Error selecting records: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_select_where(database_name: str, table_name: str, condition: str, columns: str = "*", limit: int = 100):
    """Query records from a MySQL table with a WHERE condition.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to query.
        condition: SQL WHERE clause (without the WHERE keyword).
                   Example: "age > 25 AND status = 'active'"
        columns: Comma-separated column names to select (default: "*" for all).
                 Example: "id, name, email"
        limit: Maximum number of records to return (default: 100).

    Returns:
        A dictionary containing matching records and count.
    """
    logger.info(f"--- 🔎 Tool: mysql_select_where called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor(dictionary=True)
        sql = f"SELECT {columns} FROM `{table_name}` WHERE {condition} LIMIT %s"
        cursor.execute(sql, (limit,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} records from '{table_name}' with condition")
        return {"success": True, "table": table_name, "records": records, "count": len(records), "condition": condition}
    except Exception as e:
        logger.error(f"❌ Error in select_where: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_select_count(database_name: str, table_name: str, condition: Optional[str] = None):
    """Count records in a MySQL table, optionally filtered by a condition.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to count records in.
        condition: Optional SQL WHERE clause (without the WHERE keyword).
                   Example: "status = 'active'"
                   Leave empty to count all records.

    Returns:
        A dictionary containing the total record count.
    """
    logger.info(f"--- 🔢 Tool: mysql_select_count called for '{database_name}.{table_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        sql = f"SELECT COUNT(*) FROM `{table_name}`"
        if condition:
            sql += f" WHERE {condition}"
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        logger.info(f"✅ Count for '{table_name}': {count}")
        return {"success": True, "table": table_name, "count": count, "condition": condition}
    except Exception as e:
        logger.error(f"❌ Error counting records: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_select_distinct(database_name: str, table_name: str, column: str, condition: Optional[str] = None, limit: int = 100):
    """Get distinct (unique) values of a column in a MySQL table.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to query.
        column: Column name to get distinct values for.
                Example: "city" or "status" or "category"
        condition: Optional SQL WHERE clause to filter records first.
                   Example: "active = 1"
        limit: Maximum number of distinct values to return (default: 100).

    Returns:
        A dictionary containing unique values and their count.
    """
    logger.info(f"--- 🔎 Tool: mysql_select_distinct called for '{database_name}.{table_name}.{column}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        sql = f"SELECT DISTINCT `{column}` FROM `{table_name}`"
        if condition:
            sql += f" WHERE {condition}"
        sql += f" LIMIT {limit}"
        cursor.execute(sql)
        values = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(values)} distinct values in '{column}'")
        return {"success": True, "table": table_name, "column": column, "distinct_values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ Error getting distinct values: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_select_aggregate(
    database_name: str,
    table_name: str,
    function: str,
    column: str,
    condition: Optional[str] = None,
):
    """Perform an aggregate function (SUM, AVG, MIN, MAX, COUNT) on a MySQL table column.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to query.
        function: Aggregate function to apply. One of: SUM, AVG, MIN, MAX, COUNT.
        column: Column name to apply the aggregate function on.
                Example: "price", "age", "salary"
        condition: Optional SQL WHERE clause to filter records before aggregation.
                   Example: "category = 'Electronics'"

    Returns:
        A dictionary containing the aggregate result.
    """
    logger.info(f"--- 📊 Tool: mysql_select_aggregate called: {function}({column}) on '{database_name}.{table_name}' ---")
    allowed_functions = {"SUM", "AVG", "MIN", "MAX", "COUNT"}
    func_upper = function.upper()
    if func_upper not in allowed_functions:
        return {"success": False, "error": f"Invalid function '{function}'. Allowed: {', '.join(allowed_functions)}"}
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor()
        sql = f"SELECT {func_upper}(`{column}`) FROM `{table_name}`"
        if condition:
            sql += f" WHERE {condition}"
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        logger.info(f"✅ {func_upper}({column}) = {result}")
        return {
            "success": True,
            "table": table_name,
            "function": func_upper,
            "column": column,
            "result": result,
            "condition": condition,
        }
    except Exception as e:
        logger.error(f"❌ Error in aggregate query: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_select_ordered(
    database_name: str,
    table_name: str,
    order_by: str,
    direction: str = "ASC",
    columns: str = "*",
    limit: int = 100,
    condition: Optional[str] = None,
):
    """Select records from a MySQL table sorted by a column.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to query.
        order_by: Column name to sort by. Example: "created_at" or "price".
        direction: Sort direction. Either "ASC" (ascending) or "DESC" (descending). Default: "ASC".
        columns: Comma-separated column names to select (default: "*").
        limit: Maximum number of records to return (default: 100).
        condition: Optional SQL WHERE clause to filter results.

    Returns:
        A dictionary containing sorted records.
    """
    logger.info(f"--- 🔃 Tool: mysql_select_ordered called for '{database_name}.{table_name}' ORDER BY {order_by} {direction} ---")
    direction = direction.upper()
    if direction not in ("ASC", "DESC"):
        return {"success": False, "error": "direction must be 'ASC' or 'DESC'"}
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor(dictionary=True)
        sql = f"SELECT {columns} FROM `{table_name}`"
        if condition:
            sql += f" WHERE {condition}"
        sql += f" ORDER BY `{order_by}` {direction} LIMIT {limit}"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} ordered records from '{table_name}'")
        return {"success": True, "table": table_name, "records": records, "count": len(records), "order_by": order_by, "direction": direction}
    except Exception as e:
        logger.error(f"❌ Error in ordered select: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_select_grouped(
    database_name: str,
    table_name: str,
    group_by: str,
    aggregate_column: str,
    aggregate_function: str = "COUNT",
    condition: Optional[str] = None,
    having: Optional[str] = None,
    limit: int = 100,
):
    """Group records in a MySQL table and apply an aggregate function per group.

    Args:
        database_name: Name of the database.
        table_name: Name of the table to query.
        group_by: Column to group results by. Example: "category" or "status".
        aggregate_column: Column to apply aggregate on. Use "*" with COUNT.
        aggregate_function: Aggregate to apply per group: COUNT, SUM, AVG, MIN, MAX. Default: COUNT.
        condition: Optional SQL WHERE clause to pre-filter rows before grouping.
        having: Optional HAVING clause to filter groups after aggregation.
                Example: "COUNT(*) > 5" or "SUM(price) > 1000"
        limit: Maximum number of groups to return (default: 100).

    Returns:
        A dictionary containing group results with aggregated values.
    """
    logger.info(f"--- 📊 Tool: mysql_select_grouped called for '{database_name}.{table_name}' GROUP BY {group_by} ---")
    allowed_functions = {"SUM", "AVG", "MIN", "MAX", "COUNT"}
    func_upper = aggregate_function.upper()
    if func_upper not in allowed_functions:
        return {"success": False, "error": f"Invalid aggregate function. Allowed: {', '.join(allowed_functions)}"}
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor(dictionary=True)
        agg_expr = f"{func_upper}({'*' if aggregate_column == '*' else '`' + aggregate_column + '`'})"
        sql = f"SELECT `{group_by}`, {agg_expr} AS aggregate_value FROM `{table_name}`"
        if condition:
            sql += f" WHERE {condition}"
        sql += f" GROUP BY `{group_by}`"
        if having:
            sql += f" HAVING {having}"
        sql += f" LIMIT {limit}"
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} groups from '{table_name}'")
        return {
            "success": True,
            "table": table_name,
            "group_by": group_by,
            "aggregate": f"{func_upper}({aggregate_column})",
            "records": records,
            "count": len(records),
        }
    except Exception as e:
        logger.error(f"❌ Error in grouped select: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def mysql_custom_query(database_name: str, query: str, params: Optional[List[Any]] = None):
    """Execute a custom SQL query on a MySQL database.

    Use this for complex queries involving JOINs, subqueries, or any SQL not covered
    by the other tools. Supports both SELECT and DML statements.

    Args:
        database_name: Name of the database to run the query against.
        query: Full SQL query string to execute.
               Examples:
                 "SELECT u.name, COUNT(o.id) AS order_count FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id"
                 "UPDATE products SET stock = stock - 1 WHERE id = 42"
                 "SELECT * FROM orders WHERE total > 500 ORDER BY created_at DESC LIMIT 10"
        params: Optional list of parameter values for parameterized queries (prevents SQL injection).
                Example: ["active", 30] for "WHERE status = %s AND age > %s"

    Returns:
        A dictionary with records (for SELECT) or rows_affected (for DML), plus success status.
    """
    logger.info(f"--- ⚡ Tool: mysql_custom_query called on database '{database_name}' ---")
    try:
        conn = get_mysql_connection(database=database_name)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or [])

        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT") or query_upper.startswith("SHOW") or query_upper.startswith("DESCRIBE"):
            records = cursor.fetchall()
            cursor.close()
            conn.close()
            logger.info(f"✅ Custom SELECT returned {len(records)} records")
            return {"success": True, "records": records, "count": len(records), "query": query}
        else:
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            logger.info(f"✅ Custom DML affected {rows_affected} rows")
            return {"success": True, "rows_affected": rows_affected, "query": query}
    except Exception as e:
        logger.error(f"❌ Error in custom query: {e}")
        return {"success": False, "error": str(e), "query": query}


# ============================================================================
# PROMPTS
# ============================================================================

@mcp.prompt()
def financial_analyst_prompt() -> str:
    """Prompt for financial analysis and market research."""
    return """You are an expert financial analyst. Your role is to:
1. Analyze currency exchange rates and provide insights
2. Search for financial news and market updates
3. Track cryptocurrency prices and trends
4. Provide recommendations based on current market data

Use the available tools to:
- Get exchange rates for currency conversion
- Search for financial news
- Check cryptocurrency prices
- Search for relevant market information

Always cite sources and provide context for your analysis."""


@mcp.prompt()
def investment_advisor_prompt() -> str:
    """Prompt for investment advice and market analysis."""
    return """You are a professional investment advisor. Your expertise covers:
1. Cryptocurrency market analysis and trends
2. Currency market movements and implications
3. Economic news that affects investments
4. Risk assessment and portfolio recommendations

When assisting clients:
- Check real-time cryptocurrency and currency prices
- Search for relevant economic and financial news
- Analyze market trends
- Provide balanced, research-backed recommendations
- Always disclose that past performance doesn't guarantee future results

Use all available tools to build a comprehensive market view."""


@mcp.prompt()
def travel_planner_prompt() -> str:
    """Prompt for travel planning and advice."""
    return """You are an expert travel advisor helping clients plan their trips. Your duties include:
1. Finding currency exchange rates for different countries
2. Researching weather conditions at various destinations
3. Identifying travel news and travel advisories
4. Providing currency exchange tips

When planning trips:
- Get exchange rates for the traveler's destination
- Check weather forecasts for the travel dates
- Search for travel news and advisories
- Recommend the best times to exchange currency
- Consider local events and news that might affect travel

Create detailed, practical travel plans with all necessary information."""


@mcp.prompt()
def market_researcher_prompt() -> str:
    """Prompt for comprehensive market and trend research."""
    return """You are a market researcher analyzing trends, opportunities, and competitive landscape. Your focus areas:
1. Cryptocurrency and blockchain market trends
2. Global currency movements and forex opportunities
3. Industry-specific news and developments
4. Emerging technologies and innovations

Your research methodology:
- Conduct web searches using Tavily for comprehensive coverage
- Find news articles on specific market segments
- Track category-specific news (technology, business, etc.)
- Analyze exchange rates and currency trends
- Identify market gaps and opportunities

Present findings with clear data, sources, and actionable insights."""


@mcp.prompt()
def weather_analyst_prompt() -> str:
    """Prompt for weather and climate analysis."""
    return """You are a weather analyst for planning and forecasting. Your responsibilities:
1. Providing accurate weather information for locations
2. Identifying weather patterns affecting travel and events
3. Finding weather-related news and alerts
4. Planning around climatic conditions

When analyzing weather:
- Get current and forecast weather data
- Search for weather-related news and alerts
- Consider implications for planned activities
- Provide recommendations based on conditions
- Check for severe weather warnings

Always encourage safety and preparedness."""


@mcp.prompt()
def database_administrator_prompt() -> str:
    """Prompt for database management and optimization."""
    return """You are an expert Database Administrator (DBA). Your responsibilities include:
1. Creating and managing MySQL databases and tables
2. Optimizing queries and database performance
3. Ensuring data integrity and security
4. Managing user permissions and access control
5. Performing backups and recovery procedures

When working with databases:
- Use DDL tools to create/modify/drop databases and tables
- Validate schemas before applying changes
- Always confirm destructive operations (DROP, DELETE) before executing
- Monitor table sizes and query performance
- Apply proper indexing strategies for performance

Best practices to follow:
- Use transactions for critical multi-step operations
- Always backup data before schema changes
- Prefer ALTER TABLE over DROP/CREATE to preserve data
- Use parameterized queries to prevent SQL injection"""


@mcp.prompt()
def data_analyst_prompt() -> str:
    """Prompt for data analysis and reporting."""
    return """You are a skilled Data Analyst. Your role is to:
1. Extract insights from MySQL databases using SELECT queries
2. Perform aggregations, groupings, and statistical analysis
3. Build reports and summaries from raw data
4. Identify data quality issues and anomalies

Analytical approach:
- Use mysql_select_aggregate for SUM, AVG, MIN, MAX calculations
- Use mysql_select_grouped for GROUP BY analysis and segmentation
- Use mysql_select_ordered to rank and sort data
- Use mysql_custom_query for complex JOIN queries and subqueries
- Use mysql_select_count to measure dataset sizes and filter results

When presenting findings:
- Provide context and interpretation for all numbers
- Highlight trends, outliers, and patterns
- Suggest follow-up analyses when relevant
- Format results clearly for business stakeholders"""


@mcp.prompt()
def data_engineer_prompt() -> str:
    """Prompt for ETL pipelines and data engineering tasks."""
    return """You are a Data Engineer specializing in ETL pipelines and data infrastructure. Your focus:
1. Designing efficient MySQL schemas for data pipelines
2. Building ETL processes using INSERT, UPDATE, and DELETE operations
3. Managing bulk data operations efficiently
4. Ensuring data consistency and pipeline reliability

Engineering tasks:
- Use mysql_create_table to design optimized schemas with proper indexes
- Use mysql_insert_multiple_records for efficient bulk loading
- Use mysql_update_records for incremental data updates
- Use mysql_custom_query for complex transformation logic
- Use mysql_alter_table for schema evolution and migrations

Pipeline best practices:
- Design idempotent operations that can be safely retried
- Use batch inserts instead of row-by-row for performance
- Add timestamps (created_at, updated_at) to all tables
- Include audit columns for data lineage tracking
- Validate data counts before and after transformations"""


@mcp.prompt()
def developer_database_prompt() -> str:
    """Prompt for application development and database integration."""
    return """You are a Software Developer focused on MySQL database integration. Your expertise:
1. Designing application database schemas
2. Writing efficient CRUD operations for applications
3. Implementing data access patterns and best practices
4. Debugging data-related application issues

Development workflow:
- Use mysql_create_database and mysql_create_table to scaffold the database
- Use mysql_describe_table to understand existing schemas
- Use mysql_insert_record for single-record application writes
- Use mysql_select_where for filtered application reads
- Use mysql_update_records for application update operations
- Use mysql_custom_query for complex application queries with JOINs

Coding best practices:
- Always use parameterized queries (never string-concatenate SQL)
- Handle errors gracefully and return meaningful messages
- Index foreign keys and frequently queried columns
- Use appropriate data types to minimize storage
- Implement soft deletes (is_deleted flag) over hard deletes where possible"""


@mcp.prompt()
def business_analyst_prompt() -> str:
    """Prompt for business intelligence and KPI reporting."""
    return """You are a Business Analyst using data to drive business decisions. Your role:
1. Querying MySQL databases to answer business questions
2. Building KPI dashboards and executive summaries
3. Identifying trends, opportunities, and risks in data
4. Translating business requirements into SQL queries

BI workflow:
- Use mysql_select_count to measure volumes and growth rates
- Use mysql_select_aggregate to calculate revenue, costs, and margins
- Use mysql_select_grouped to segment customers, products, and regions
- Use mysql_select_ordered to rank top/bottom performers
- Use mysql_custom_query for multi-table reports with JOINs

Reporting approach:
- Start with high-level KPIs, then drill down into details
- Compare current period vs. prior period for trend analysis
- Segment data by relevant dimensions (region, category, channel)
- Highlight actionable insights and clear recommendations
- Always validate data quality before presenting findings"""


@mcp.prompt()
def database_designer_prompt() -> str:
    """Prompt for database schema design and architecture."""
    return """You are a Database Designer and Architect. Your expertise:
1. Designing normalized MySQL schemas for scalability
2. Choosing the right data types, constraints, and indexes
3. Modeling relationships (one-to-one, one-to-many, many-to-many)
4. Planning schema migrations and versioning strategies

Design principles:
- Apply normalization (3NF) to eliminate data redundancy
- Define primary keys on every table (prefer AUTO_INCREMENT INT or UUID)
- Use foreign keys to enforce referential integrity
- Create indexes on columns used in WHERE, JOIN, and ORDER BY clauses
- Choose VARCHAR sizes that match real-world data (don't over-allocate)

Schema design workflow:
- Use mysql_create_database to set up the database with proper charset
- Use mysql_create_table to implement the schema with all constraints
- Use mysql_describe_table to review and validate existing structures
- Use mysql_alter_table to add/modify columns and indexes over time
- Use mysql_list_tables to get an overview of the full schema

Always document your schema design decisions and consider future scalability."""


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7080))
    logger.info(f"🚀 Multi-Purpose MCP server starting on port {port}")

    logger.info("📋 Available Tools:")
    logger.info("\n--- FINANCIAL & INFORMATION TOOLS (4) ---")
    logger.info("  1. get_exchange_rate     - Get currency exchange rates")
    logger.info("  2. tavily_search         - Search the web using Tavily AI")
    logger.info("  3. get_crypto_prices     - Get cryptocurrency prices")
    logger.info("  4. weather_search        - Get weather information for cities")

    if MYSQL_AVAILABLE:
        logger.info("\n--- MYSQL DDL TOOLS (8) ---")
        logger.info("  5.  mysql_create_database  - Create a new database")
        logger.info("  6.  mysql_drop_database    - Drop an existing database")
        logger.info("  7.  mysql_list_databases   - List all databases")
        logger.info("  8.  mysql_create_table     - Create a new table")
        logger.info("  9.  mysql_drop_table       - Drop an existing table")
        logger.info("  10. mysql_alter_table      - Modify table structure")
        logger.info("  11. mysql_list_tables      - List tables in a database")
        logger.info("  12. mysql_describe_table   - Describe table columns/schema")

        logger.info("\n--- MYSQL DML TOOLS (4) ---")
        logger.info("  13. mysql_insert_record          - Insert a single record")
        logger.info("  14. mysql_insert_multiple_records - Bulk insert records")
        logger.info("  15. mysql_update_records         - Update records by condition")
        logger.info("  16. mysql_delete_records         - Delete records by condition")

        logger.info("\n--- MYSQL SELECT TOOLS (8) ---")
        logger.info("  17. mysql_select_all        - Select all records (paginated)")
        logger.info("  18. mysql_select_where      - Select with WHERE condition")
        logger.info("  19. mysql_select_count      - Count records")
        logger.info("  20. mysql_select_distinct   - Get distinct/unique values")
        logger.info("  21. mysql_select_aggregate  - SUM, AVG, MIN, MAX, COUNT")
        logger.info("  22. mysql_select_ordered    - Select with ORDER BY")
        logger.info("  23. mysql_select_grouped    - Select with GROUP BY")
        logger.info("  24. mysql_custom_query      - Execute any custom SQL query")
        logger.info("\n  ✅ Total MySQL Tools: 20  |  Grand Total: 24 tools")
    else:
        logger.warning("\n--- MYSQL DATABASE TOOLS ---")
        logger.warning("  ❌ MySQL tools NOT available (mysql-connector-python not installed)")
        logger.warning("  Install with: pip install mysql-connector-python>=8.2.0")

    logger.info("\n🎯 Available Prompts (11):")
    logger.info("  1.  financial_analyst_prompt      - Financial analysis")
    logger.info("  2.  investment_advisor_prompt     - Investment advice")
    logger.info("  3.  travel_planner_prompt         - Travel planning")
    logger.info("  4.  market_researcher_prompt      - Market research")
    logger.info("  5.  weather_analyst_prompt        - Weather analysis")
    logger.info("  6.  database_administrator_prompt - Database management & optimization")
    logger.info("  7.  data_analyst_prompt           - Data analysis & reporting")
    logger.info("  8.  data_engineer_prompt          - ETL & data pipelines")
    logger.info("  9.  developer_database_prompt     - Application development")
    logger.info("  10. business_analyst_prompt       - Business intelligence")
    logger.info("  11. database_designer_prompt      - Schema design & architecture")

    logger.info("\n🔐 Configuration:")
    logger.info("  - TAVILY_API_KEY: (optional, for web search)")
    if MYSQL_AVAILABLE:
        logger.info(f"  - MYSQL_HOST:     {MYSQL_CONFIG['host']}")
        logger.info(f"  - MYSQL_USER:     {MYSQL_CONFIG['user']}")
        logger.info(f"  - MYSQL_PORT:     {MYSQL_CONFIG['port']}")
        logger.info("  - MYSQL_PASSWORD: ••••• (configured)")

    asyncio.run(
        mcp.run_async(
            transport="sse",
            host="0.0.0.0",
            port=port,
        )
    )

# import asyncio
# import logging
# import os
# import json
# from typing import Optional, List, Dict, Any

# try:
#     import mysql.connector
#     from mysql.connector import Error
#     MYSQL_AVAILABLE = True
# except ImportError:
#     MYSQL_AVAILABLE = False
#     Error = Exception

# import httpx
# from fastmcp import FastMCP

# logger = logging.getLogger(__name__)
# logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

# mcp = FastMCP("Multi-Purpose Information MCP Server 🌐")

# # API Keys from environment
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# # ============================================================================
# # MYSQL DATABASE CONFIGURATION
# # ============================================================================
# MYSQL_CONFIG = {
#     "host": os.getenv("MYSQL_HOST", "localhost"),
#     "user": os.getenv("MYSQL_USER", "root"),
#     "password": os.getenv("MYSQL_PASSWORD", "Maxis@123"),
#     "port": int(os.getenv("MYSQL_PORT", 3306)),
#     "autocommit": True,
# }


# def get_mysql_connection():
#     """Create and return a MySQL database connection."""
#     if not MYSQL_AVAILABLE:
#         raise ImportError("mysql-connector-python is not installed. Install with: pip install mysql-connector-python")
    
#     try:
#         connection = mysql.connector.connect(**MYSQL_CONFIG)
#         if connection.is_connected():
#             logger.info("✅ MySQL connection established")
#         return connection
#     except Error as e:
#         logger.error(f"❌ MySQL connection error: {e}")
#         raise


# @mcp.tool()
# def get_exchange_rate(
#     currency_from: str = "USD",
#     currency_to: str = "EUR",
#     currency_date: str = "latest",
# ):
#     """Use this to get current exchange rate.

#     Args:
#         currency_from: The currency to convert from (e.g., "USD").
#         currency_to: The currency to convert to (e.g., "EUR").
#         currency_date: The date for the exchange rate or "latest". Defaults to "latest".

#     Returns:
#         A dictionary containing the exchange rate data, or an error message if the request fails.
#     """
#     logger.info(
#         f"--- 🛠️ Tool: get_exchange_rate called for converting {currency_from} to {currency_to} ---"
#     )
#     try:
#         response = httpx.get(
#             f"https://api.frankfurter.app/{currency_date}",
#             params={"from": currency_from, "to": currency_to},
#         )
#         response.raise_for_status()

#         data = response.json()
#         if "rates" not in data:
#             logger.error(f"❌ rates not found in response: {data}")
#             return {"error": "Invalid API response format."}
#         logger.info(f"✅ API response: {data}")
#         return data
#     except httpx.HTTPError as e:
#         logger.error(f"❌ API request failed: {e}")
#         return {"error": f"API request failed: {e}"}
#     except ValueError:
#         logger.error("❌ Invalid JSON response from API")
#         return {"error": "Invalid JSON response from API."}


# @mcp.tool()
# def tavily_search(query: str, include_answer: bool = True, max_results: int = 5):
#     """Search the web using Tavily AI search engine.

#     Args:
#         query: The search query string
#         include_answer: Whether to include a direct answer to the query
#         max_results: Maximum number of results to return (1-20)

#     Returns:
#         A dictionary containing search results and optionally an answer
#     """
#     logger.info(f"--- 🔍 Tool: tavily_search called with query: {query} ---")
    
#     if not TAVILY_API_KEY:
#         logger.error("❌ TAVILY_API_KEY not configured")
#         return {"error": "TAVILY_API_KEY not configured. Set it as an environment variable."}
    
#     try:
#         response = httpx.post(
#             "https://api.tavily.com/search",
#             json={
#                 "api_key": TAVILY_API_KEY,
#                 "query": query,
#                 "include_answer": include_answer,
#                 "max_results": max_results,
#             },
#             timeout=10.0,
#         )
#         response.raise_for_status()
        
#         data = response.json()
#         logger.info(f"✅ Tavily search results: {len(data.get('results', []))} found")
#         return data
#     except httpx.HTTPError as e:
#         logger.error(f"❌ Tavily API request failed: {e}")
#         return {"error": f"Tavily search failed: {e}"}
#     except Exception as e:
#         logger.error(f"❌ Unexpected error in tavily_search: {e}")
#         return {"error": f"Unexpected error: {e}"}


# @mcp.tool()
# def get_crypto_prices(
#     symbols: str = "bitcoin,ethereum",
#     vs_currency: str = "usd",
# ):
#     """Get cryptocurrency prices using CoinGecko API (no key required).

#     Args:
#         symbols: Comma-separated cryptocurrency IDs (e.g., 'bitcoin,ethereum,cardano')
#         vs_currency: Currency to get prices in (e.g., 'usd', 'eur', 'gbp')

#     Returns:
#         A dictionary containing cryptocurrency prices and market data
#     """
#     logger.info(f"--- 💰 Tool: get_crypto_prices called for {symbols} ---")
    
#     try:
#         response = httpx.get(
#             "https://api.coingecko.com/api/v3/simple/price",
#             params={
#                 "ids": symbols,
#                 "vs_currencies": vs_currency,
#                 "include_market_cap": "true",
#                 "include_24hr_vol": "true",
#                 "include_24hr_change": "true",
#             },
#             timeout=10.0,
#         )
#         response.raise_for_status()
        
#         data = response.json()
#         logger.info(f"✅ Crypto prices retrieved: {list(data.keys())}")
#         return data
#     except httpx.HTTPError as e:
#         logger.error(f"❌ CoinGecko API request failed: {e}")
#         return {"error": f"Failed to fetch crypto prices: {e}"}
#     except Exception as e:
#         logger.error(f"❌ Error in get_crypto_prices: {e}")
#         return {"error": f"Unexpected error: {e}"}


# @mcp.tool()
# def weather_search(
#     city: str,
#     country_code: Optional[str] = None,
# ):
#     """Get current weather information for a city.

#     Args:
#         city: City name (e.g., 'London', 'New York')
#         country_code: Optional ISO 3166 country code (e.g., 'GB', 'US')

#     Returns:
#         A dictionary containing current weather data
#     """
#     logger.info(f"--- 🌤️ Tool: weather_search called for {city} ---")
    
#     try:
#         location = f"{city},{country_code}" if country_code else city
#         response = httpx.get(
#             "https://wttr.in",
#             params={"q": location, "format": "j1"},
#             timeout=10.0,
#         )
#         response.raise_for_status()
        
#         data = response.json()
#         logger.info(f"✅ Weather data retrieved for {city}")
#         return data
#     except httpx.HTTPError as e:
#         logger.error(f"❌ Weather API request failed: {e}")
#         return {"error": f"Failed to fetch weather: {e}"}
#     except Exception as e:
#         logger.error(f"❌ Error in weather_search: {e}")
#         return {"error": f"Unexpected error: {e}"}


# # ============================================================================
# # MULTIPLE PROMPTS FOR DIFFERENT USE CASES
# # ============================================================================

# @mcp.prompt()
# def financial_analyst_prompt() -> str:
#     """Prompt for financial analysis and market research."""
#     return """You are an expert financial analyst. Your role is to:
# 1. Analyze currency exchange rates and provide insights
# 2. Search for financial news and market updates
# 3. Track cryptocurrency prices and trends
# 4. Provide recommendations based on current market data

# Use the available tools to:
# - Get exchange rates for currency conversion
# - Search for financial news
# - Check cryptocurrency prices
# - Search for relevant market information

# Always cite sources and provide context for your analysis."""


# @mcp.prompt()
# def investment_advisor_prompt() -> str:
#     """Prompt for investment advice and market analysis."""
#     return """You are a professional investment advisor. Your expertise covers:
# 1. Cryptocurrency market analysis and trends
# 2. Currency market movements and implications
# 3. Economic news that affects investments
# 4. Risk assessment and portfolio recommendations

# When assisting clients:
# - Check real-time cryptocurrency and currency prices
# - Search for relevant economic and financial news
# - Analyze market trends
# - Provide balanced, research-backed recommendations
# - Always disclose that past performance doesn't guarantee future results

# Use all available tools to build a comprehensive market view."""


# @mcp.prompt()
# def travel_planner_prompt() -> str:
#     """Prompt for travel planning and advice."""
#     return """You are an expert travel advisor helping clients plan their trips. Your duties include:
# 1. Finding currency exchange rates for different countries
# 2. Researching weather conditions at various destinations
# 3. Identifying travel news and travel advisories
# 4. Providing currency exchange tips

# When planning trips:
# - Get exchange rates for the traveler's destination
# - Check weather forecasts for the travel dates
# - Search for travel news and advisories
# - Recommend the best times to exchange currency
# - Consider local events and news that might affect travel

# Create detailed, practical travel plans with all necessary information."""


# @mcp.prompt()
# def market_researcher_prompt() -> str:
#     """Prompt for comprehensive market and trend research."""
#     return """You are a market researcher analyzing trends, opportunities, and competitive landscape. Your focus areas:
# 1. Cryptocurrency and blockchain market trends
# 2. Global currency movements and forex opportunities
# 3. Industry-specific news and developments
# 4. Emerging technologies and innovations

# Your research methodology:
# - Conduct web searches using Tavily for comprehensive coverage
# - Find news articles on specific market segments
# - Track category-specific news (technology, business, etc.)
# - Analyze exchange rates and currency trends
# - Identify market gaps and opportunities

# Present findings with clear data, sources, and actionable insights."""


# @mcp.prompt()
# def weather_analyst_prompt() -> str:
#     """Prompt for weather and climate analysis."""
#     return """You are a weather analyst for planning and forecasting. Your responsibilities:
# 1. Providing accurate weather information for locations
# 2. Identifying weather patterns affecting travel and events
# 3. Finding weather-related news and alerts
# 4. Planning around climatic conditions

# When analyzing weather:
# - Get current and forecast weather data
# - Search for weather-related news and alerts
# - Consider implications for planned activities
# - Provide recommendations based on conditions
# - Check for severe weather warnings

# Always encourage safety and preparedness."""


# if __name__ == "__main__":
#     logger.info(f"🚀 Multi-Purpose MCP server starting on port {os.getenv('PORT', 7080)}")
#     logger.info("📋 Available Tools:")
#     logger.info("\n--- FINANCIAL & INFORMATION TOOLS ---")
#     logger.info("  - get_exchange_rate: Get currency exchange rates")
#     logger.info("  - tavily_search: Search the web using Tavily AI")
#     logger.info("  - get_crypto_prices: Get cryptocurrency prices")
#     logger.info("  - weather_search: Get weather information for cities")
    
#     if MYSQL_AVAILABLE:
#         logger.info("\n--- MYSQL DATABASE TOOLS ---")
#         logger.info("  ✅ MySQL database tools ARE available")
#         logger.info("  - DDL: create/drop/list databases, create/drop/alter/describe tables")
#         logger.info("  - DML: insert/update/delete records")
#         logger.info("  - SELECT: select/count/aggregate/group/order queries")
#     else:
#         logger.warning("\n--- MYSQL DATABASE TOOLS ---")
#         logger.warning("  ❌ MySQL tools NOT available (mysql-connector-python not installed)")
#         logger.warning("  To enable MySQL tools, install with:")
#         logger.warning("  pip install mysql-connector-python>=8.2.0")
    
#     logger.info("\n🎯 Available Prompts:")
#     logger.info("  - financial_analyst_prompt: For financial analysis")
#     logger.info("  - investment_advisor_prompt: For investment advice")
#     logger.info("  - travel_planner_prompt: For travel planning")
#     logger.info("  - market_researcher_prompt: For market research")
#     logger.info("  - weather_analyst_prompt: For weather analysis")
#     if MYSQL_AVAILABLE:
#         logger.info("  - database_administrator_prompt: For database management")
#         logger.info("  - data_analyst_prompt: For data analysis")
#         logger.info("  - data_engineer_prompt: For data engineering")
#         logger.info("  - developer_database_prompt: For application development")
#         logger.info("  - business_analyst_prompt: For business intelligence")
#         logger.info("  - database_designer_prompt: For schema design")
    
#     logger.info("\n🔐 Configuration:")
#     logger.info("  - TAVILY_API_KEY environment variable (optional, for web search)")
#     if MYSQL_AVAILABLE:
#         logger.info(f"  - MYSQL_HOST: {MYSQL_CONFIG['host']}")
#         logger.info(f"  - MYSQL_USER: {MYSQL_CONFIG['user']}")
#         logger.info(f"  - MYSQL_PORT: {MYSQL_CONFIG['port']}")
#         logger.info("  - MYSQL_PASSWORD: ••••• (configured)")
    
#     # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
#     asyncio.run(
#         mcp.run_async(
#             transport="sse",
#             host="0.0.0.0",
#             port=os.getenv("PORT", 7080),
#         )
#     )

