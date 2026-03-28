# MySQL MCP Server - Setup & Testing Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- MySQL 5.7 or higher (8.0+ recommended)
- 2GB RAM minimum
- Network access to MySQL server

### Verify MySQL Installation

```bash
# Check MySQL version
mysql --version

# Test MySQL connection
mysql -h localhost -u root -p

# If successful, you should see the MySQL prompt:
mysql>
```

---

## Installation Steps

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd /Users/welcome/Library/Mobile\ Documents/com~apple~CloudDocs/Tech_Learn/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/mcp_expe/mcp_server

# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Verify installation
pip list | grep fastmcp
pip list | grep mysql-connector-python
```

### Step 3: Configure Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your MySQL credentials
nano .env  # macOS/Linux
# OR
notepad .env  # Windows
```

**Example .env file:**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=Maxis@123
MYSQL_PORT=3306
TAVILY_API_KEY=your_api_key_here
PORT=7080
```

### Step 4: Test MySQL Connection

Create a test script `test_connection.py`:

```python
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "Maxis@123"),
        port=int(os.getenv("MYSQL_PORT", 3306))
    )
    
    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"✅ Successfully connected to MySQL Server version {db_info}")
        
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        record = cursor.fetchone()
        print(f"Current database: {record}")
        cursor.close()
    
    connection.close()
    print("✅ Connection test passed!")
    
except mysql.connector.Error as e:
    print(f"❌ Error while connecting to MySQL: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

Run the test:
```bash
python test_connection.py
```

Expected output:
```
✅ Successfully connected to MySQL Server version 8.0.x
Current database: None
✅ Connection test passed!
```

---

## Running the Server

### Development Mode

```bash
# Start the server
python currency_mcp_server.py

# Expected output:
# 🚀 Multi-Purpose MCP server starting on port 7080
# 📋 Available Tools:
# --- FINANCIAL & INFORMATION TOOLS ---
# ...
# --- MYSQL DATABASE TOOLS - DDL OPERATIONS ---
# ...
```

### Production Deployment

```bash
# Set environment variables for production
export MYSQL_HOST=your.production.mysql.host
export MYSQL_USER=prod_user
export MYSQL_PASSWORD=strong_password
export TAVILY_API_KEY=your_api_key
export PORT=7080

# Run with gunicorn (install: pip install gunicorn)
gunicorn -w 4 -b 0.0.0.0:7080 currency_mcp_server:app
```

---

## Testing the Tools

### Test Script: `test_tools.py`

```python
#!/usr/bin/env python3
"""
Test script for MySQL MCP Server tools
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the MCP server (this would normally be done through the server)
import mysql.connector
from mysql.connector import Error

def get_mysql_connection():
    """Create and return a MySQL database connection."""
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "Maxis@123"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "autocommit": True,
    }
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        print(f"❌ Connection error: {e}")
        raise

def test_database_operations():
    """Test basic database operations"""
    print("\n" + "="*50)
    print("TESTING MYSQL DATABASE OPERATIONS")
    print("="*50)
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    
    try:
        # Test 1: Create database
        print("\n1️⃣ Creating test database...")
        cursor.execute("DROP DATABASE IF EXISTS test_mcp_db")
        cursor.execute("CREATE DATABASE test_mcp_db")
        print("✅ Database created successfully")
        
        # Test 2: Create table
        print("\n2️⃣ Creating test table...")
        cursor.execute("USE test_mcp_db")
        create_table_sql = """
        CREATE TABLE users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_sql)
        print("✅ Table created successfully")
        
        # Test 3: Insert data
        print("\n3️⃣ Inserting test data...")
        insert_sql = """
        INSERT INTO users (name, email, age) VALUES
        ('Alice Johnson', 'alice@example.com', 28),
        ('Bob Smith', 'bob@example.com', 35),
        ('Charlie Brown', 'charlie@example.com', 42),
        ('Diana Prince', 'diana@example.com', 31),
        ('Evan Williams', 'evan@example.com', 26)
        """
        cursor.execute(insert_sql)
        connection.commit()
        print(f"✅ Inserted {cursor.rowcount} records")
        
        # Test 4: Select data
        print("\n4️⃣ Selecting all data...")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"  - {user[1]} ({user[2]}): age {user[3]}")
        print(f"✅ Retrieved {len(users)} records")
        
        # Test 5: Count records
        print("\n5️⃣ Counting records...")
        cursor.execute("SELECT COUNT(*) FROM users WHERE age > 30")
        count = cursor.fetchone()[0]
        print(f"✅ Users over 30: {count}")
        
        # Test 6: Aggregate functions
        print("\n6️⃣ Testing aggregate functions...")
        cursor.execute("SELECT AVG(age), MIN(age), MAX(age) FROM users")
        avg_age, min_age, max_age = cursor.fetchone()
        print(f"✅ Average age: {avg_age:.1f}, Min: {min_age}, Max: {max_age}")
        
        # Test 7: Update records
        print("\n7️⃣ Updating records...")
        cursor.execute("UPDATE users SET age = age + 1 WHERE name = 'Alice Johnson'")
        connection.commit()
        print(f"✅ Updated {cursor.rowcount} record(s)")
        
        # Test 8: Delete records
        print("\n8️⃣ Deleting records...")
        cursor.execute("DELETE FROM users WHERE age > 40")
        connection.commit()
        print(f"✅ Deleted {cursor.rowcount} record(s)")
        
        # Test 9: Describe table
        print("\n9️⃣ Getting table structure...")
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Test 10: Cleanup
        print("\n🔟 Cleaning up...")
        cursor.execute("DROP DATABASE test_mcp_db")
        connection.commit()
        print("✅ Test database removed")
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("="*50)
        
    except Error as e:
        print(f"\n❌ Test failed: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    try:
        test_database_operations()
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        sys.exit(1)
```

Run the test:
```bash
python test_tools.py
```

---

## Advanced Configuration

### Custom MySQL Port

If MySQL is running on a non-standard port (e.g., 3307):

```env
MYSQL_PORT=3307
```

### Remote MySQL Server

```env
MYSQL_HOST=192.168.1.100
MYSQL_USER=remote_user
MYSQL_PASSWORD=secure_password
MYSQL_PORT=3306
```

### SSL/TLS Connection

For secure remote connections, create `config.py`:

```python
import mysql.connector
import ssl

MYSQL_SSL_CONFIG = {
    'ca': '/path/to/ca.pem',
    'cert': '/path/to/client-cert.pem',
    'key': '/path/to/client-key.pem',
    'check_hostname': True,
    'verify_cert': True,
}

connection = mysql.connector.connect(
    host='remote.server.com',
    user='root',
    password='password',
    database='mydb',
    ssl_disabled=False,
    **MYSQL_SSL_CONFIG
)
```

---

## Monitoring & Logging

### Enable Query Logging

```sql
-- Execute in MySQL
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'TABLE';

-- View logs
SELECT * FROM mysql.general_log LIMIT 100;

-- Disable when done
SET GLOBAL general_log = 'OFF';
```

### Check Slow Queries

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  -- Log queries slower than 2 seconds

-- View slow queries
SELECT * FROM mysql.slow_log;
```

---

## Performance Tuning

### Create Indexes

```python
# After connecting to server
cursor.execute("CREATE INDEX idx_email ON users(email)")
cursor.execute("CREATE INDEX idx_created_at ON users(created_at)")
cursor.execute("CREATE COMPOSITE INDEX idx_user_date ON orders(user_id, order_date)")
```

### Analyze Query Performance

```python
# Use EXPLAIN to analyze queries
cursor.execute("EXPLAIN SELECT * FROM users WHERE email = 'test@example.com'")
explain_result = cursor.fetchall()
print(explain_result)
```

---

## Backup & Recovery

### Backup Database

```bash
# Backup specific database
mysqldump -u root -p mydb > mydb_backup.sql

# Backup all databases
mysqldump -u root -p --all-databases > full_backup.sql

# Backup with compression
mysqldump -u root -p mydb | gzip > mydb_backup.sql.gz
```

### Restore Database

```bash
# Restore from backup
mysql -u root -p mydb < mydb_backup.sql

# Restore compressed backup
gunzip < mydb_backup.sql.gz | mysql -u root -p mydb
```

### Python Backup Script

```python
import subprocess
import datetime

def backup_database(db_name, user='root', password='Maxis@123'):
    """Create a database backup"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{db_name}_backup_{timestamp}.sql"
    
    command = f"mysqldump -h localhost -u {user} -p{password} {db_name} > {filename}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Backup created: {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")
        return None

# Usage
backup_database('ecommerce_db')
```

---

## Troubleshooting Checklist

```
[ ] MySQL service is running
[ ] Correct host/port in .env
[ ] Correct username/password
[ ] User has required permissions
[ ] Network connectivity to server
[ ] Firewall allows port 3306
[ ] Database exists (if connecting to specific DB)
[ ] Table names are correct
[ ] Column names are correct
[ ] SQL syntax is valid
[ ] No reserved keywords used without backticks
```

---

## Common Issues & Solutions

### Issue: "Can't connect to MySQL server"
```
Solution:
1. Ensure MySQL is running: sudo systemctl start mysql
2. Check credentials: mysql -u root -p
3. Verify port: netstat -an | grep 3306
```

### Issue: "Unknown column"
```
Solution:
1. Check column spelling
2. Use backticks: `column_name`
3. Verify table selected: USE database_name
```

### Issue: "Duplicate entry"
```
Solution:
1. Check for UNIQUE constraints
2. Use INSERT IGNORE
3. Use INSERT ... ON DUPLICATE KEY UPDATE
```

---

## Next Steps

1. ✅ Set up environment variables
2. ✅ Test MySQL connection
3. ✅ Run the test suite
4. ✅ Start the MCP server
5. ✅ Begin using the tools
6. ✅ Review PRACTICAL_GUIDE.md for examples
7. ✅ Implement in your application

---

## Support Resources

- MySQL Documentation: https://dev.mysql.com/doc/
- FastMCP: https://fastmcp.readthedocs.io/
- MySQL Connector/Python: https://dev.mysql.com/doc/connector-python/
- Model Context Protocol: https://modelcontextprotocol.io/

---

Happy coding! 🚀
