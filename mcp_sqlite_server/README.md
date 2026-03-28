# SQLite MCP Server 📄

## Overview
FastMCP-based server for SQLite database operations with support for embedded SQL databases and file-based persistence.

## Features
- **Embedded Database**: File-based SQLite support
- **Zero Configuration**: No server setup required
- **ACID Compliance**: Full transaction support
- **Full SQL**: Complete SQL language support
- **Indexing**: Index creation and management
- **Lightweight**: Perfect for edge and embedded use

## Setup & Installation

### Prerequisites
- Python 3.9+
- SQLite 3.0+

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export SQLITE_DATABASE="myapp.db"
```

### Running
```bash
python server.py
```

## Tools Available

### execute_sql
Execute arbitrary SQL queries.

### list_tables
List all tables in database.

### describe_table
Get table schema information.

### insert_record
Insert records into tables.

### update_record
Update records with WHERE clause.

### delete_record
Delete records from tables.

### get_database_stats
Get database statistics.

### create_index
Create indexes for performance.

## Usage Examples

### Basic Query
```python
await client.call_tool("execute_sql", {
    "query": "SELECT * FROM users WHERE id = ?",
    "parameters": [1]
})
```

### Insert Data
```python
await client.call_tool("insert_record", {
    "table_name": "users",
    "data": {
        "name": "John",
        "email": "john@example.com"
    }
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
```

## Use Cases
- Mobile apps
- Desktop applications
- IoT devices
- Embedded systems
- Development/testing
- Single-user databases

## Advantages
- No server required
- Portable database file
- Zero dependencies beyond Python
- Full SQL support
- ACID transactions
