"""
Redis MCP Server using FastMCP
Provides tools for Redis in-memory data store operations
"""

import asyncio
import redis
from redis import Redis
import json
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("redis-mcp-server")

class RedisConnectionPool:
    def __init__(self, host: str, port: int, db: int = 0, password: str = None):
        self.config = {
            "host": host,
            "port": port,
            "db": db,
            "decode_responses": True
        }
        if password:
            self.config["password"] = password
        
        self.client = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.Redis(**self.config)
            self.client.ping()
            logger.info("Connected to Redis")
        except Exception as err:
            logger.error(f"Error connecting to Redis: {err}")
            raise
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from Redis")

db_pool = None

@mcp.tool()
async def get_value(key: str) -> dict:
    """Get value by key"""
    try:
        value = db_pool.client.get(key)
        return {"success": True, "value": value}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def set_value(key: str, value: str, ttl: int = None) -> dict:
    """Set key-value pair"""
    try:
        if ttl:
            db_pool.client.setex(key, ttl, value)
        else:
            db_pool.client.set(key, value)
        return {"success": True, "message": "Value set"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_key(key: str) -> dict:
    """Delete a key"""
    try:
        count = db_pool.client.delete(key)
        return {"success": True, "deleted_count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def check_key_exists(key: str) -> dict:
    """Check if key exists"""
    try:
        exists = db_pool.client.exists(key) > 0
        return {"success": True, "exists": exists}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_keys(pattern: str = "*") -> dict:
    """List keys matching pattern"""
    try:
        keys = db_pool.client.keys(pattern)
        return {"success": True, "keys": list(keys)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def push_to_list(key: str, values: list) -> dict:
    """Push values to list"""
    try:
        count = db_pool.client.rpush(key, *values)
        return {"success": True, "pushed_count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def pop_from_list(key: str, count: int = 1) -> dict:
    """Pop values from list"""
    try:
        values = [db_pool.client.lpop(key) for _ in range(count)]
        return {"success": True, "values": [v for v in values if v]}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_list_range(key: str, start: int = 0, end: int = -1) -> dict:
    """Get range from list"""
    try:
        values = db_pool.client.lrange(key, start, end)
        return {"success": True, "values": values}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def add_to_set(key: str, values: list) -> dict:
    """Add values to set"""
    try:
        count = db_pool.client.sadd(key, *values)
        return {"success": True, "added_count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_set_members(key: str) -> dict:
    """Get all set members"""
    try:
        members = db_pool.client.smembers(key)
        return {"success": True, "members": list(members)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def set_hash(key: str, data: dict) -> dict:
    """Set hash fields"""
    try:
        db_pool.client.hset(key, mapping=data)
        return {"success": True, "message": "Hash set"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_hash(key: str) -> dict:
    """Get entire hash"""
    try:
        h = db_pool.client.hgetall(key)
        return {"success": True, "hash": h}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_redis_info() -> dict:
    """Get Redis server info"""
    try:
        info = db_pool.client.info()
        return {
            "success": True,
            "info": {
                "redis_version": info.get("redis_version"),
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed")
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def flush_database() -> dict:
    """Flush current database"""
    try:
        db_pool.client.flushdb()
        return {"success": True, "message": "Database flushed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    password = os.getenv("REDIS_PASSWORD")
    
    db_pool = RedisConnectionPool(host, port, db, password)
    await db_pool.connect()
    
    try:
        logger.info("Starting Redis MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
