# Complete Database MCP Servers Collection 🗄️

A comprehensive collection of FastMCP-based servers for various databases and data store operations. Each server provides full tool integration through the Model Context Protocol.

## Overview

This collection includes 12 production-ready MCP servers covering:
- **Relational Databases**: MySQL, PostgreSQL, SQL Server, Google Spanner
- **NoSQL Databases**: MongoDB, DynamoDB, Cassandra
- **Cache Stores**: Redis, AWS ElastiCache
- **Data Warehouses**: Databricks
- **Search Engines**: OpenSearch
- **Vector Databases**: Pinecone, Milvus, Qdrant

## Database Servers

### 1. MySQL MCP Server 📦
**Location**: `mcp_mysql_server/`

FastMCP server for MySQL relational database with full CRUD operations.

**Features**:
- Connection pooling
- Query execution
- Table management
- Schema operations
- Data manipulation

**Setup**:
```bash
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_USER="root"
export MYSQL_PASSWORD="password"
export MYSQL_DATABASE="myapp"
```

**Key Tools**: `list_tables`, `describe_table`, `execute_query`, `insert_data`, `update_data`, `delete_data`

---

### 2. PostgreSQL MCP Server 🐘
**Location**: `mcp_postgres_server/`

FastMCP server for PostgreSQL with advanced features like JSON support and stored procedures.

**Features**:
- Advanced SQL support
- JSON/JSONB operations
- Transaction management
- Array types support
- Full-text search

**Setup**:
```bash
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="password"
export POSTGRES_DATABASE="myapp"
```

**Key Tools**: `execute_query`, `list_schemas`, `describe_table`, `manage_transactions`, `json_operations`

---

### 3. MongoDB MCP Server 🍃
**Location**: `mcp_mongodb_server/`

FastMCP server for MongoDB NoSQL document database with aggregation pipelines.

**Features**:
- Document operations
- Aggregation pipelines
- Index management
- Transaction support
- Collection management

**Setup**:
```bash
export MONGODB_URI="mongodb://localhost:27017"
export MONGODB_DATABASE="myapp"
```

**Key Tools**: `insert_document`, `find_documents`, `aggregate`, `update_document`, `delete_document`, `create_index`

---

### 4. SQLite MCP Server 📄
**Location**: `mcp_sqlite_server/`

FastMCP server for SQLite embedded database, perfect for local/development use.

**Features**:
- File-based database
- Zero configuration
- Transaction support
- Full ACID compliance
- Lightweight

**Setup**:
```bash
export SQLITE_DATABASE="/path/to/database.db"
```

**Key Tools**: `execute_sql`, `list_tables`, `create_table`, `insert_data`, `query_data`

---

### 5. Cassandra MCP Server 📊
**Location**: `mcp_cassandra_server/`

FastMCP server for Apache Cassandra distributed NoSQL database.

**Features**:
- Distributed architecture
- CQL support
- Multi-node clusters
- High availability
- Automatic replication

**Setup**:
```bash
export CASSANDRA_CONTACT_POINTS="localhost,cassandra-2,cassandra-3"
export CASSANDRA_KEYSPACE="myapp"
export CASSANDRA_USER="cassandra"
export CASSANDRA_PASSWORD="password"
```

**Key Tools**: `execute_query`, `list_tables`, `insert_record`, `update_record`, `get_cluster_stats`

---

### 6. Redis MCP Server ⚡
**Location**: `mcp_redis_server/`

FastMCP server for Redis in-memory data store with multiple data types support.

**Features**:
- In-memory speed
- Multiple data types
- TTL expiration
- Pub-Subscribe
- Persistence options

**Setup**:
```bash
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_DB="0"
export REDIS_PASSWORD="password"  # Optional
```

**Key Tools**: `get_value`, `set_value`, `push_to_list`, `add_to_set`, `set_hash`, `increment_counter`

---

### 7. AWS DynamoDB MCP Server 🚀
**Location**: `mcp_dynamodb_server/`

FastMCP server for AWS DynamoDB serverless NoSQL database.

**Features**:
- Fully managed service
- Serverless pricing
- Global tables
- Auto-scaling
- Batch operations

**Setup**:
```bash
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
```

**Key Tools**: `list_tables`, `put_item`, `get_item`, `query_items`, `batch_write`, `update_item`

---

### 8. Databricks MCP Server 📊
**Location**: `mcp_databricks_server/`

FastMCP server for Databricks SQL warehouse and analytics.

**Features**:
- SQL warehouse support
- Schema management
- Table operations
- View creation
- Analytics queries

**Setup**:
```bash
export DATABRICKS_HOSTNAME="your-workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/warehouse-id"
export DATABRICKS_TOKEN="your_pat_token"
```

**Key Tools**: `execute_sql`, `list_schemas`, `create_table`, `insert_data`, `run_query_and_fetch`

---

### 9. Google Cloud Spanner MCP Server 🌍
**Location**: `mcp_spanner_server/`

FastMCP server for Google Cloud Spanner with global scale and strong consistency.

**Features**:
- Global distribution
- ACID transactions
- Strong consistency
- Automatic backup
- Horizontal scaling

**Setup**:
```bash
export GCP_PROJECT_ID="your-project-id"
export SPANNER_INSTANCE_ID="my-instance"
export SPANNER_DATABASE_ID="my-database"
```

**Key Tools**: `execute_query`, `insert_row`, `update_row`, `batch_insert`, `describe_table`

---

### 10. AWS ElastiCache MCP Server 💾
**Location**: `mcp_elasticache_server/`

FastMCP server for AWS ElastiCache Redis/Memcached operations.

**Features**:
- Fully managed caching
- Redis & Memcached
- High performance
- Auto-failover
- Encryption support

**Setup**:
```bash
export ELASTICACHE_ENDPOINT="your-cluster.cache.amazonaws.com"
export ELASTICACHE_PORT="6379"
export ELASTICACHE_PASSWORD="password"  # Optional
```

**Key Tools**: `get_value`, `set_value`, `increment_counter`, `append_to_list`, `get_cache_stats`

---

### 11. Pinecone MCP Server 🔍
**Location**: `mcp_pinecone_server/`

FastMCP server for Pinecone vector database for semantic search and RAG.

**Features**:
- Vector search
- Semantic similarity
- Metadata filtering
- Namespaces
- Low latency queries

**Setup**:
```bash
export PINECONE_API_KEY="your_api_key"
export PINECONE_ENVIRONMENT="us-west1-gcp"  # Optional
```

**Key Tools**: `list_indexes`, `upsert_vectors`, `query_vectors`, `get_vector`, `delete_vectors`

---

### 12. OpenSearch MCP Server 🔎
**Location**: `mcp_opensearch_server/`

FastMCP server for OpenSearch (Elasticsearch alternative) with full-text search.

**Features**:
- Full-text search
- Open source
- Scalable architecture
- Real-time analytics
- Fine-grained access control

**Setup**:
```bash
export OPENSEARCH_HOSTS="localhost:9200"
export OPENSEARCH_USER="admin"
export OPENSEARCH_PASSWORD="AdminPassword123!"
export OPENSEARCH_USE_SSL="true"
```

**Key Tools**: `list_indices`, `create_index`, `index_document`, `search_documents`, `bulk_index`

---

### 13. Milvus MCP Server 🎯
**Location**: `mcp_milvus_server/`

FastMCP server for Milvus open-source vector database.

**Features**:
- Open source
- Scalable architecture
- Multiple index types
- GPU support
- Partitioning

**Setup**:
```bash
export MILVUS_HOST="localhost"
export MILVUS_PORT="19530"
```

**Key Tools**: `list_collections`, `insert_vectors`, `search_vectors`, `create_index`, `create_partition`

---

### 14. Qdrant MCP Server 🔷
**Location**: `mcp_qdrant_server/`

FastMCP server for Qdrant vector database with focus on ease of use.

**Features**:
- Python-native interface
- Flexible distance metrics
- Scalable architecture
- Payload-based filtering
- Open source

**Setup**:
```bash
export QDRANT_URL="http://localhost:6333"
export QDRANT_API_KEY="optional_api_key"  # Optional
```

**Key Tools**: `list_collections`, `upsert_points`, `search_points`, `scroll_points`, `count_points`

---

## Server Categories

### Relational Databases
- MySQL
- PostgreSQL
- SQLite
- Google Spanner

### NoSQL Databases
- MongoDB
- Cassandra
- AWS DynamoDB

### Caching & In-Memory
- Redis
- AWS ElastiCache

### Data Warehouses & Analytics
- Databricks

### Search Engines
- OpenSearch

### Vector Databases
- Pinecone
- Milvus
- Qdrant

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- FastMCP framework
- Database client libraries (specific to each server)

### Install All Servers
```bash
# For each server directory:
pip install -r requirements.txt
```

### Start Individual Server
```bash
cd mcp_<database>_server/
python server.py
```

---

## Common Patterns

### Connection Management
All servers follow similar connection patterns:
```python
# Environment-based configuration
db_pool = ConnectionClass(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
await db_pool.connect()
```

### Tool Definition
All tools follow FastMCP pattern:
```python
@mcp.tool()
async def operation_name(param1: str, param2: int) -> dict:
    """Operation description"""
    try:
        # Implementation
        return {"success": True, "result": value}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

---

## Use Cases by Database

### User Authentication & Sessions
- **Best**: Redis, MongoDB, PostgreSQL

### Real-time Analytics
- **Best**: OpenSearch, Databricks, DynamoDB

### Document Storage
- **Best**: MongoDB, DynamoDB, CosmosDB

### Vector Search/RAG
- **Best**: Pinecone, Qdrant, Milvus

### Time-series Data
- **Best**: Cassandra, MongoDB, PostgreSQL

### Caching Layer
- **Best**: Redis, ElastiCache

### Global Applications
- **Best**: Spanner, DynamoDB, Cassandra

### Full-text Search
- **Best**: OpenSearch, PostgreSQL

---

## Performance Comparison

| Database | Latency | Throughput | Scale | Best For |
|----------|---------|-----------|-------|----------|
| Redis | <1ms | Very High | GB-100GB | Caching |
| DynamoDB | <10ms | High | Unlimited | Serverless |
| MongoDB | 1-10ms | High | TB-PB | Documents |
| PostgreSQL | 1-10ms | High | TB | Relational |
| Cassandra | 1-10ms | Very High | PB | Time-series |
| Spanner | 10-100ms | High | Unlimited | Global |
| OpenSearch | 10-100ms | Medium | TB | Search |
| Pinecone | <100ms | High | GB | Vectors |

---

## Monitoring & Production

### Health Checks
Implement periodic health checks:
```python
# In your application
async def health_check():
    try:
        result = await client.call_tool("get_server_info", {})
        return result["success"]
    except:
        return False
```

### Connection Pooling
All servers implement connection pooling for efficiency.

### Error Handling
Standardized error responses:
```json
{
    "success": false,
    "error": "Error message"
}
```

### Logging
All servers use Python's logging module for observability.

---

## Configuration Best Practices

1. **Use Environment Variables**: Store sensitive credentials in env vars
2. **Connection Pooling**: Reuse connections across requests
3. **Timeouts**: Set appropriate timeout values
4. **Retry Logic**: Implement exponential backoff
5. **Monitoring**: Track performance metrics
6. **Security**: Use TLS where applicable
7. **Authentication**: Use strong credentials

---

## Troubleshooting

### Connection Issues
- Verify host and port configuration
- Check network connectivity
- Validate credentials
- Review firewall rules

### Performance Issues
- Monitor query execution
- Check index usage
- Review memory usage
- Analyze slow queries

### Data Issues
- Verify schema compatibility
- Check data types
- Review batch sizes
- Monitor disk space

---

## Contributing

To add new database support:

1. Create new directory: `mcp_<database>_server/`
2. Implement server.py with FastMCP
3. Add README.md with documentation
4. Create requirements.txt
5. Test with sample data

---

## License

Open source - Feel free to use and modify for your needs.

---

## Support & Documentation

Each server includes:
- Detailed README.md
- requirements.txt with dependencies
- Example tool usage
- Configuration guide
- Troubleshooting section

---

## Quick Start Guide

### 1. Choose Your Database
```bash
ls mcp_*_server/
```

### 2. Install Dependencies
```bash
cd mcp_<database>_server/
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
export DB_HOST="your_host"
export DB_PORT="your_port"
# ... other settings
```

### 4. Start Server
```bash
python server.py
```

### 5. Use in Your Application
```python
# Make MCP calls to use database tools
result = await client.call_tool("tool_name", {"param": "value"})
```

---

## Performance Optimization Tips

### For All Databases
- Use connection pooling
- Batch operations when possible
- Index frequently queried columns
- Monitor slow queries
- Implement caching strategies

### Database-Specific
- **Redis/ElastiCache**: Use pipelining
- **MongoDB**: Use compound indexes
- **PostgreSQL**: Use EXPLAIN ANALYZE
- **DynamoDB**: Design partition keys carefully
- **Cassandra**: Use clustering keys
- **Vector DBs**: Use appropriate distance metrics

---

## Architecture Overview

```
MCP Servers Collection
├── Relational Databases
│   ├── MySQL
│   ├── PostgreSQL
│   ├── SQLite
│   └── Spanner
├── NoSQL Databases
│   ├── MongoDB
│   ├── Cassandra
│   └── DynamoDB
├── Cache & Real-time
│   ├── Redis
│   └── ElastiCache
├── Analytics
│   └── Databricks
├── Search Engines
│   └── OpenSearch
└── Vector Databases
    ├── Pinecone
    ├── Milvus
    └── Qdrant
```

---

## Summary

This collection provides comprehensive FastMCP server coverage for 14+ major databases and data stores, enabling seamless integration through the Model Context Protocol. Each server is production-ready with proper error handling, connection management, and comprehensive tooling.

**Total Servers**: 14 (MySQL, PostgreSQL, MongoDB, SQLite, Cassandra, Redis, DynamoDB, Databricks, Spanner, ElastiCache, Pinecone, OpenSearch, Milvus, Qdrant)

**Total Tools**: 100+ database operation tools

**Status**: ✅ Complete and Production-Ready
