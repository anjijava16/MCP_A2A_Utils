# MySQL MCP Server - Practical Use Case Guide

## Quick Reference

### Most Common Operations

```python
# Create a database
mysql_create_database("my_app")

# Create a table
mysql_create_table(
    "my_app",
    "employees",
    "id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), department VARCHAR(50), salary DECIMAL(10,2)"
)

# Insert data
mysql_insert_record("my_app", "employees", "(name, department, salary) VALUES ('John', 'IT', 5000)")

# Query data
mysql_select_all("my_app", "employees")

# Update data
mysql_update_records("my_app", "employees", "salary=5500", "name='John'")

# Delete data
mysql_delete_records("my_app", "employees", "salary < 3000")
```

---

## Scenario 1: Building an E-commerce System

### Step 1: Create Database
```python
mysql_create_database("ecommerce_db")
```

### Step 2: Create Tables
```python
# Users table
mysql_create_table(
    "ecommerce_db",
    "users",
    """
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    """
)

# Products table
mysql_create_table(
    "ecommerce_db",
    "products",
    """
    id INT PRIMARY KEY AUTO_INCREMENT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    """
)

# Orders table
mysql_create_table(
    "ecommerce_db",
    "orders",
    """
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12, 2),
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id)
    """
)
```

### Step 3: Insert Sample Data
```python
# Add users
mysql_insert_multiple_records(
    "ecommerce_db",
    "users",
    """
    (username, email, password_hash, first_name, last_name, country)
    VALUES
    ('john_doe', 'john@example.com', 'hashed_password_1', 'John', 'Doe', 'USA'),
    ('jane_smith', 'jane@example.com', 'hashed_password_2', 'Jane', 'Smith', 'UK'),
    ('alex_brown', 'alex@example.com', 'hashed_password_3', 'Alex', 'Brown', 'Canada')
    """
)

# Add products
mysql_insert_multiple_records(
    "ecommerce_db",
    "products",
    """
    (sku, name, description, price, stock_quantity, category)
    VALUES
    ('LAPTOP-001', 'Gaming Laptop', '16GB RAM, RTX 3080', 1299.99, 50, 'Electronics'),
    ('PHONE-001', 'Smartphone Pro', '5G, 256GB Storage', 999.99, 100, 'Electronics'),
    ('DESK-001', 'Standing Desk', 'Adjustable Height', 399.99, 30, 'Furniture')
    """
)
```

### Step 4: Query Operations
```python
# Get all products
mysql_select_all("ecommerce_db", "products")

# Get products by category
mysql_select_where(
    "ecommerce_db",
    "products",
    "category='Electronics'",
    "name, price"
)

# Count total users
mysql_select_count("ecommerce_db", "users")

# Get average product price
mysql_select_aggregate(
    "ecommerce_db",
    "products",
    "AVG",
    "price"
)

# Get products sorted by price
mysql_select_ordered(
    "ecommerce_db",
    "products",
    "price",
    limit=10,
    ascending=False
)
```

---

## Scenario 2: Customer Analytics Dashboard

### Setup
```python
# Assuming ecommerce_db from Scenario 1

# Get top customers by order count
mysql_custom_query(
    "ecommerce_db",
    """
    SELECT 
        u.username,
        u.email,
        COUNT(o.id) as order_count,
        SUM(o.total_amount) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
    ORDER BY total_spent DESC
    LIMIT 10
    """
)

# Get product performance
mysql_custom_query(
    "ecommerce_db",
    """
    SELECT 
        p.name,
        p.price,
        p.stock_quantity,
        COUNT(oi.id) as times_ordered
    FROM products p
    LEFT JOIN order_items oi ON p.id = oi.product_id
    GROUP BY p.id
    ORDER BY times_ordered DESC
    """
)
```

---

## Scenario 3: User Account Management

### Create User Account
```python
mysql_insert_record(
    "ecommerce_db",
    "users",
    "(username, email, password_hash, first_name, last_name) VALUES ('new_user', 'new@example.com', 'hashed_pwd', 'New', 'User')"
)
```

### Update User Profile
```python
mysql_update_records(
    "ecommerce_db",
    "users",
    "first_name='Updated', country='Australia'",
    "username='new_user'"
)
```

### Get User Details
```python
mysql_select_where(
    "ecommerce_db",
    "users",
    "username='new_user'",
    "username, email, first_name, last_name, country, created_at"
)
```

---

## Scenario 4: Inventory Management

### Check Stock Levels
```python
# Low stock items (below 25 units)
mysql_select_where(
    "ecommerce_db",
    "products",
    "stock_quantity < 25",
    "sku, name, stock_quantity"
)

# Group by category
mysql_select_grouped(
    "ecommerce_db",
    "products",
    "category",
    "stock_quantity",
    "SUM"
)
```

### Update Stock After Sale
```python
mysql_update_records(
    "ecommerce_db",
    "products",
    "stock_quantity = stock_quantity - 1",
    "id=1"
)
```

### Restock Items
```python
mysql_update_records(
    "ecommerce_db",
    "products",
    "stock_quantity = stock_quantity + 100, updated_at = NOW()",
    "sku='LAPTOP-001'"
)
```

---

## Scenario 5: Data Maintenance & Cleanup

### Archive Old Orders
```python
# Find orders older than 365 days
mysql_select_where(
    "ecommerce_db",
    "orders",
    "order_date < DATE_SUB(NOW(), INTERVAL 365 DAY)",
    "*",
    limit=1000
)

# Delete old orders
mysql_delete_records(
    "ecommerce_db",
    "orders",
    "order_date < DATE_SUB(NOW(), INTERVAL 2 YEAR)"
)
```

### Remove Inactive Users
```python
# Find users who never placed orders
mysql_custom_query(
    "ecommerce_db",
    """
    SELECT u.id, u.username, u.created_at
    FROM users u
    WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id)
    AND u.created_at < DATE_SUB(NOW(), INTERVAL 6 MONTH)
    """
)
```

---

## Scenario 6: Reporting & Analytics

### Daily Sales Report
```python
mysql_custom_query(
    "ecommerce_db",
    """
    SELECT 
        DATE(order_date) as sales_date,
        COUNT(*) as order_count,
        SUM(total_amount) as daily_revenue,
        AVG(total_amount) as avg_order_value
    FROM orders
    WHERE order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    GROUP BY DATE(order_date)
    ORDER BY sales_date DESC
    """
)
```

### Customer Segmentation
```python
# High-value customers (top 20%)
mysql_custom_query(
    "ecommerce_db",
    """
    SELECT 
        u.id,
        u.username,
        u.email,
        SUM(o.total_amount) as customer_lifetime_value
    FROM users u
    JOIN orders o ON u.id = o.user_id
    GROUP BY u.id
    HAVING customer_lifetime_value > 5000
    ORDER BY customer_lifetime_value DESC
    """
)
```

---

## Scenario 7: Schema Evolution

### Add New Column
```python
mysql_alter_table(
    "ecommerce_db",
    "users",
    "ADD COLUMN phone_number VARCHAR(20)"
)
```

### Modify Column
```python
mysql_alter_table(
    "ecommerce_db",
    "products",
    "MODIFY COLUMN description TEXT CHARSET utf8mb4"
)
```

### Create Index for Performance
```python
mysql_alter_table(
    "ecommerce_db",
    "products",
    "ADD INDEX idx_category (category)"
)

mysql_alter_table(
    "ecommerce_db",
    "orders",
    "ADD INDEX idx_user_date (user_id, order_date)"
)
```

---

## Scenario 8: Data Validation & Quality

### Find Duplicates
```python
mysql_custom_query(
    "ecommerce_db",
    """
    SELECT email, COUNT(*) as count
    FROM users
    GROUP BY email
    HAVING count > 1
    """
)
```

### Identify Data Issues
```python
# Products with no category
mysql_select_where(
    "ecommerce_db",
    "products",
    "category IS NULL OR category = ''",
    "id, name, price"
)

# Negative stock
mysql_select_where(
    "ecommerce_db",
    "products",
    "stock_quantity < 0",
    "sku, name, stock_quantity"
)
```

---

## Best Practices Checklist

✅ **Do:**
- Use parameterized queries for security
- Validate input data before insertion
- Regular backups of critical data
- Monitor query performance
- Use indexes for frequently queried columns
- Implement proper error handling
- Log database operations
- Use transactions for multi-step operations

❌ **Don't:**
- Commit credentials to version control
- Use root user for application access
- Run unsafe DELETE queries without WHERE
- Store sensitive data in plain text
- Ignore backup procedures
- Forget to validate user input
- Make schema changes in production without testing
- Use SELECT * without LIMIT on large tables

---

## SQL Cheat Sheet

### Common Patterns

```sql
-- Date functions
WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
WHERE DATE(created_at) = CURDATE()
WHERE YEAR(created_at) = 2024

-- String functions
WHERE name LIKE '%search%'
WHERE UPPER(username) = 'JOHN'
WHERE LENGTH(password_hash) > 20

-- Numeric functions
WHERE price BETWEEN 100 AND 500
WHERE salary > (SELECT AVG(salary) FROM employees)
WHERE stock_quantity % 2 = 0  -- even numbers

-- NULL handling
WHERE email IS NOT NULL
WHERE phone_number IS NULL

-- Case expressions
SELECT name, CASE 
    WHEN price > 1000 THEN 'Premium'
    WHEN price > 500 THEN 'Mid-range'
    ELSE 'Budget'
END as price_segment
FROM products

-- Window functions (MySQL 8.0+)
SELECT name, price,
    ROW_NUMBER() OVER (ORDER BY price DESC) as rank
FROM products
```

---

## Troubleshooting Common Issues

### Issue: Connection Fails
```
Solution: 
1. Verify MySQL is running: mysql -u root -p
2. Check credentials in .env
3. Test connection: mysql -h localhost -u root -p
```

### Issue: Slow Queries
```
Solution:
1. Add indexes: ALTER TABLE table_name ADD INDEX idx_column (column_name)
2. Use EXPLAIN: EXPLAIN SELECT ...
3. Avoid SELECT *: Specify needed columns
4. Add LIMIT clause: ... LIMIT 100
```

### Issue: Duplicate Key Errors
```
Solution:
1. Check for duplicate emails: SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1
2. Use INSERT ... ON DUPLICATE KEY UPDATE
3. Or use INSERT IGNORE for duplicates
```

---

Remember: Always test queries in a development environment first!
