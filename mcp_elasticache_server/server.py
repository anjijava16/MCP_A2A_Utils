"""
AWS ElastiCache MCP Server using FastMCP
Provides tools for AWS ElastiCache Redis/Memcached operations
"""

import asyncio
import redis
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("elasticache-mcp-server")

class ElastiCacheConnectionPool:
    def __init__(self, endpoint: str, port: int, password: str = None):
        self.endpoint = endpoint
        self.port = port
        self.password = password
        self.client = None
    
    async def connect(self):
        """Connect to ElastiCache"""
        try:
            kwargs = {
                "host": self.endpoint,
                "port": self.port,
                "decode_responses": True
            }
            if self.password:
                kwargs["password"] = self.password
            
            self.client = redis.Redis(**kwargs)
            self.client.ping()
            logger.info(f"Connected to ElastiCache: {self.endpoint}:{self.port}")
        except Exception as err:
            logger.error(f"Error connecting to ElastiCache: {err}")
            raise
    
    async def disconnect(self):
        """Close ElastiCache connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from ElastiCache")

db_pool = None

@mcp.tool()
async def get_value(key: str) -> dict:
    """Get value from cache"""
    try:
        value = db_pool.client.get(key)
        return {"success": True, "value": value, "found": value is not None}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def set_value(key: str, value: str, ttl: int = None) -> dict:
    """Set value in cache"""
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
    """Delete key from cache"""
    try:
        count = db_pool.client.delete(key)
        return {"success": True, "deleted": count > 0}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_keys(pattern: str = "*") -> dict:
    """List keys matching pattern"""
    try:
        keys = db_pool.client.keys(pattern)
        return {"success": True, "keys": list(keys), "count": len(keys)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_cache_stats() -> dict:
    """Get cache statistics"""
    try:
        info = db_pool.client.info("stats")
        return {
            "success": True,
            "stats": {
                "total_connections": info.get("total_connections_received"),
                "total_commands": info.get("total_commands_processed"),
                "used_memory_human": db_pool.client.info("memory").get("used_memory_human")
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def increment_counter(key: str, increment_by: int = 1) -> dict:
    """Increment counter"""
    try:
        new_value = db_pool.client.incrby(key, increment_by)
        return {"success": True, "new_value": new_value}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def append_to_list(key: str, values: list) -> dict:
    """Append to list in cache"""
    try:
        count = db_pool.client.rpush(key, *values)
        return {"success": True, "list_length": count}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_list(key: str, start: int = 0, end: int = -1) -> dict:
    """Get list from cache"""
    try:
        values = db_pool.client.lrange(key, start, end)
        return {"success": True, "values": values}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def set_hash(key: str, data: dict) -> dict:
    """Set hash in cache"""
    try:
        db_pool.client.hset(key, mapping=data)
        return {"success": True, "message": "Hash set"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_hash(key: str) -> dict:
    """Get hash from cache"""
    try:
        h = db_pool.client.hgetall(key)
        return {"success": True, "hash": h}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def flush_cache() -> dict:
    """Flush entire cache"""
    try:
        db_pool.client.flushdb()
        return {"success": True, "message": "Cache flushed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    endpoint = os.getenv("ELASTICACHE_ENDPOINT", "localhost")
    port = int(os.getenv("ELASTICACHE_PORT", "6379"))
    password = os.getenv("ELASTICACHE_PASSWORD")
    
    db_pool = ElastiCacheConnectionPool(endpoint, port, password)
    await db_pool.connect()
    
    try:
        logger.info("Starting ElastiCache MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
