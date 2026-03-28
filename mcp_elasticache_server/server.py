"""
AWS ElastiCache MCP Server 🔴
Comprehensive MCP server for AWS ElastiCache (Redis/Memcached) management and operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
import redis
import boto3
from botocore.exceptions import ClientError
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("ElastiCache 🔴")

def get_elasticache_connection():
    """Get ElastiCache Redis connection"""
    endpoint = os.getenv("ELASTICACHE_ENDPOINT", "localhost")
    port = int(os.getenv("ELASTICACHE_PORT", "6379"))
    password = os.getenv("ELASTICACHE_PASSWORD")
    
    kwargs = {
        "host": endpoint,
        "port": port,
        "decode_responses": True
    }
    if password:
        kwargs["password"] = password
    
    try:
        client = redis.Redis(**kwargs)
        client.ping()
        return client
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

def get_elasticache_client():
    """Get AWS ElastiCache boto3 client for cluster management"""
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("elasticache", region_name=region)

# ==================== CLUSTER MANAGEMENT ====================

@mcp.tool()
async def list_clusters() -> dict:
    """📋 List all ElastiCache clusters"""
    try:
        client = get_elasticache_client()
        response = client.describe_cache_clusters()
        clusters = response.get("CacheClusters", [])
        
        cluster_info = [
            {
                "id": c["CacheClusterId"],
                "engine": c["Engine"],
                "node_type": c["CacheNodeType"],
                "status": c["CacheClusterStatus"],
                "node_count": len(c.get("CacheNodes", [])),
                "endpoint": c.get("CacheNodes", [{}])[0].get("Endpoint", {}).get("Address")
            }
            for c in clusters
        ]
        
        logger.info(f"✅ Found {len(cluster_info)} clusters")
        return {"success": True, "clusters": cluster_info, "count": len(cluster_info)}
    except ClientError as e:
        logger.error(f"❌ Error listing clusters: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_cluster(cluster_id: str) -> dict:
    """🔎 Get cluster details"""
    try:
        client = get_elasticache_client()
        response = client.describe_cache_clusters(CacheClusterId=cluster_id)
        cluster = response["CacheClusters"][0]
        
        info = {
            "id": cluster["CacheClusterId"],
            "engine": cluster["Engine"],
            "engine_version": cluster["EngineVersion"],
            "node_type": cluster["CacheNodeType"],
            "status": cluster["CacheClusterStatus"],
            "node_count": len(cluster.get("CacheNodes", [])),
            "parameter_group": cluster.get("CacheParameterGroup", {}).get("CacheParameterGroupName"),
            "port": cluster.get("CacheNodes", [{}])[0].get("Endpoint", {}).get("Port")
        }
        
        logger.info(f"✅ Retrieved cluster info")
        return {"success": True, "cluster": info}
    except ClientError as e:
        logger.error(f"❌ Error describing cluster: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_cluster(cluster_id: str, node_type: str = "cache.t3.micro", engine: str = "redis", num_cache_nodes: int = 1) -> dict:
    """✨ Create new ElastiCache cluster"""
    try:
        client = get_elasticache_client()
        client.create_cache_cluster(
            CacheClusterId=cluster_id,
            CacheNodeType=node_type,
            Engine=engine,
            NumCacheNodes=num_cache_nodes
        )
        
        logger.info(f"✅ Cluster {cluster_id} creation initiated")
        return {"success": True, "message": f"Cluster {cluster_id} creation initiated"}
    except ClientError as e:
        logger.error(f"❌ Error creating cluster: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_cluster(cluster_id: str, final_snapshot: Optional[str] = None) -> dict:
    """❌ Delete cluster (irreversible)"""
    try:
        client = get_elasticache_client()
        kwargs = {"CacheClusterId": cluster_id}
        if final_snapshot:
            kwargs["FinalCacheNodeSnapshotIdentifier"] = final_snapshot
        
        client.delete_cache_cluster(**kwargs)
        
        logger.info(f"✅ Cluster {cluster_id} deletion initiated")
        return {"success": True, "message": f"Cluster {cluster_id} deletion initiated"}
    except ClientError as e:
        logger.error(f"❌ Error deleting cluster: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def modify_cluster(cluster_id: str, node_type: Optional[str] = None, num_cache_nodes: Optional[int] = None, parameter_group: Optional[str] = None) -> dict:
    """⚙️ Modify cluster configuration"""
    try:
        client = get_elasticache_client()
        kwargs = {"CacheClusterId": cluster_id}
        
        if node_type:
            kwargs["CacheNodeType"] = node_type
        if num_cache_nodes:
            kwargs["NumCacheNodes"] = num_cache_nodes
        if parameter_group:
            kwargs["CacheParameterGroupName"] = parameter_group
        
        client.modify_cache_cluster(**kwargs)
        
        logger.info(f"✅ Cluster {cluster_id} modification initiated")
        return {"success": True, "message": f"Cluster {cluster_id} modified"}
    except ClientError as e:
        logger.error(f"❌ Error modifying cluster: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== PARAMETER GROUP OPERATIONS ====================

@mcp.tool()
async def list_parameter_groups() -> dict:
    """📋 List parameter groups"""
    try:
        client = get_elasticache_client()
        response = client.describe_cache_parameter_groups()
        groups = response.get("CacheParameterGroups", [])
        
        group_info = [
            {
                "name": g["CacheParameterGroupName"],
                "family": g["CacheParameterGroupFamily"],
                "description": g.get("Description")
            }
            for g in groups
        ]
        
        logger.info(f"✅ Found {len(group_info)} parameter groups")
        return {"success": True, "groups": group_info, "count": len(group_info)}
    except ClientError as e:
        logger.error(f"❌ Error listing parameter groups: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_parameter_group(group_name: str, family: str, description: str) -> dict:
    """✨ Create parameter group"""
    try:
        client = get_elasticache_client()
        client.create_cache_parameter_group(
            CacheParameterGroupName=group_name,
            CacheParameterGroupFamily=family,
            Description=description
        )
        
        logger.info(f"✅ Parameter group {group_name} created")
        return {"success": True, "message": f"Parameter group {group_name} created"}
    except ClientError as e:
        logger.error(f"❌ Error creating parameter group: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_parameter_group(group_name: str) -> dict:
    """🗑️ Delete parameter group"""
    try:
        client = get_elasticache_client()
        client.delete_cache_parameter_group(CacheParameterGroupName=group_name)
        
        logger.info(f"✅ Parameter group {group_name} deleted")
        return {"success": True, "message": f"Parameter group {group_name} deleted"}
    except ClientError as e:
        logger.error(f"❌ Error deleting parameter group: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SNAPSHOT & BACKUP OPERATIONS ====================

@mcp.tool()
async def create_snapshot(cluster_id: str, snapshot_id: str) -> dict:
    """💾 Create cluster snapshot"""
    try:
        client = get_elasticache_client()
        client.create_snapshot(
            CacheClusterId=cluster_id,
            SnapshotName=snapshot_id
        )
        
        logger.info(f"✅ Snapshot {snapshot_id} creation initiated")
        return {"success": True, "message": f"Snapshot {snapshot_id} created"}
    except ClientError as e:
        logger.error(f"❌ Error creating snapshot: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_snapshots() -> dict:
    """📋 List snapshots"""
    try:
        client = get_elasticache_client()
        response = client.describe_snapshots()
        snapshots = response.get("Snapshots", [])
        
        snapshot_info = [
            {
                "id": s["SnapshotName"],
                "cluster_id": s.get("CacheClusterId"),
                "status": s["SnapshotStatus"],
                "created": str(s.get("SnapshotCreateTime")),
                "size_mb": s.get("SnapshotSizeInMegabytes")
            }
            for s in snapshots
        ]
        
        logger.info(f"✅ Found {len(snapshot_info)} snapshots")
        return {"success": True, "snapshots": snapshot_info, "count": len(snapshot_info)}
    except ClientError as e:
        logger.error(f"❌ Error listing snapshots: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def restore_from_snapshot(snapshot_id: str, target_cluster_id: str) -> dict:
    """♻️ Restore cluster from snapshot"""
    try:
        client = get_elasticache_client()
        client.restore_cache_cluster_from_snapshot(
            CacheClusterId=target_cluster_id,
            SnapshotName=snapshot_id
        )
        
        logger.info(f"✅ Restore from {snapshot_id} initiated")
        return {"success": True, "message": f"Restore to {target_cluster_id} initiated"}
    except ClientError as e:
        logger.error(f"❌ Error restoring: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== STRING DATA OPERATIONS ====================

@mcp.tool()
async def get_value(key: str) -> dict:
    """📖 Get string value"""
    try:
        client = get_elasticache_connection()
        value = client.get(key)
        logger.info(f"✅ Retrieved key {key}")
        return {"success": True, "value": value, "found": value is not None}
    except Exception as e:
        logger.error(f"❌ Error getting value: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def set_value(key: str, value: str, ttl: Optional[int] = None) -> dict:
    """✍️ Set string value"""
    try:
        client = get_elasticache_connection()
        
        if ttl:
            client.setex(key, ttl, value)
        else:
            client.set(key, value)
        
        logger.info(f"✅ Set key {key}")
        return {"success": True, "message": "Value set"}
    except Exception as e:
        logger.error(f"❌ Error setting value: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def mget_values(keys: List[str]) -> dict:
    """🎯 Get multiple values"""
    try:
        client = get_elasticache_connection()
        values = client.mget(keys)
        logger.info(f"✅ Retrieved {len(values)} values")
        return {"success": True, "values": values}
    except Exception as e:
        logger.error(f"❌ Error getting multiple values: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def mset_values(key_values: Dict[str, str]) -> dict:
    """📦 Set multiple values"""
    try:
        client = get_elasticache_connection()
        client.mset(key_values)
        logger.info(f"✅ Set {len(key_values)} values")
        return {"success": True, "message": f"Set {len(key_values)} values"}
    except Exception as e:
        logger.error(f"❌ Error setting multiple values: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_key(key: str) -> dict:
    """🗑️ Delete key"""
    try:
        client = get_elasticache_connection()
        count = client.delete(key)
        logger.info(f"✅ Deleted key {key}")
        return {"success": True, "deleted": count > 0}
    except Exception as e:
        logger.error(f"❌ Error deleting key: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== KEY MANAGEMENT ====================

@mcp.tool()
async def list_keys(pattern: str = "*", limit: int = 1000) -> dict:
    """🔍 List keys matching pattern"""
    try:
        client = get_elasticache_connection()
        keys = client.keys(pattern)
        limited_keys = list(keys)[:limit]
        logger.info(f"✅ Found {len(limited_keys)} keys")
        return {"success": True, "keys": limited_keys, "count": len(limited_keys)}
    except Exception as e:
        logger.error(f"❌ Error listing keys: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def exists_key(key: str) -> dict:
    """✔️ Check if key exists"""
    try:
        client = get_elasticache_connection()
        exists = client.exists(key)
        logger.info(f"✅ Key exists check done")
        return {"success": True, "exists": exists > 0}
    except Exception as e:
        logger.error(f"❌ Error checking key: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def set_ttl(key: str, seconds: int) -> dict:
    """⏰ Set key expiration"""
    try:
        client = get_elasticache_connection()
        client.expire(key, seconds)
        logger.info(f"✅ TTL set for {key}")
        return {"success": True, "message": f"TTL set to {seconds} seconds"}
    except Exception as e:
        logger.error(f"❌ Error setting TTL: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_ttl(key: str) -> dict:
    """🕐 Get key TTL"""
    try:
        client = get_elasticache_connection()
        ttl = client.ttl(key)
        logger.info(f"✅ Retrieved TTL for {key}")
        return {"success": True, "ttl_seconds": ttl}
    except Exception as e:
        logger.error(f"❌ Error getting TTL: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== LIST OPERATIONS ====================

@mcp.tool()
async def lpush_to_list(key: str, values: List[str]) -> dict:
    """➕ Push values to list (head)"""
    try:
        client = get_elasticache_connection()
        count = client.lpush(key, *values)
        logger.info(f"✅ Pushed {len(values)} values to list")
        return {"success": True, "list_length": count}
    except Exception as e:
        logger.error(f"❌ Error pushing to list: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def rpush_to_list(key: str, values: List[str]) -> dict:
    """➕ Push values to list (tail)"""
    try:
        client = get_elasticache_connection()
        count = client.rpush(key, *values)
        logger.info(f"✅ Pushed {len(values)} values")
        return {"success": True, "list_length": count}
    except Exception as e:
        logger.error(f"❌ Error pushing to list: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_list_range(key: str, start: int = 0, end: int = -1) -> dict:
    """📖 Get list range"""
    try:
        client = get_elasticache_connection()
        values = client.lrange(key, start, end)
        logger.info(f"✅ Retrieved {len(values)} list items")
        return {"success": True, "values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ Error getting list range: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== HASH OPERATIONS ====================

@mcp.tool()
async def set_hash(key: str, data: Dict[str, str]) -> dict:
    """✍️ Set hash fields"""
    try:
        client = get_elasticache_connection()
        client.hset(key, mapping=data)
        logger.info(f"✅ Set {len(data)} hash fields")
        return {"success": True, "message": f"Set {len(data)} fields"}
    except Exception as e:
        logger.error(f"❌ Error setting hash: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_hash(key: str) -> dict:
    """📖 Get entire hash"""
    try:
        client = get_elasticache_connection()
        h = client.hgetall(key)
        logger.info(f"✅ Retrieved hash with {len(h)} fields")
        return {"success": True, "hash": h, "field_count": len(h)}
    except Exception as e:
        logger.error(f"❌ Error getting hash: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_hash_field(key: str, field: str) -> dict:
    """🔍 Get hash field value"""
    try:
        client = get_elasticache_connection()
        value = client.hget(key, field)
        logger.info(f"✅ Retrieved hash field")
        return {"success": True, "value": value}
    except Exception as e:
        logger.error(f"❌ Error getting hash field: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== MONITORING & STATS ====================

@mcp.tool()
async def get_cache_stats() -> dict:
    """📊 Get Redis statistics"""
    try:
        client = get_elasticache_connection()
        info = client.info("stats")
        memory_info = client.info("memory")
        
        stats = {
            "total_connections": info.get("total_connections_received"),
            "total_commands": info.get("total_commands_processed"),
            "used_memory": memory_info.get("used_memory_human"),
            "max_memory": memory_info.get("maxmemory_human"),
            "evicted_keys": info.get("evicted_keys")
        }
        
        logger.info(f"✅ Retrieved cache statistics")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_server_info() -> dict:
    """🔎 Get Redis server info"""
    try:
        client = get_elasticache_connection()
        info = client.info("server")
        
        server_info = {
            "redis_version": info.get("redis_version"),
            "process_id": info.get("process_id"),
            "uptime_seconds": info.get("uptime_in_seconds"),
            "tcp_port": info.get("tcp_port")
        }
        
        logger.info(f"✅ Retrieved server info")
        return {"success": True, "server_info": server_info}
    except Exception as e:
        logger.error(f"❌ Error getting server info: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def flush_cache(flush_all: bool = False) -> dict:
    """🧹 Flush cache data"""
    try:
        client = get_elasticache_connection()
        if flush_all:
            client.flushall()
        else:
            client.flushdb()
        
        logger.info(f"✅ Cache flushed")
        return {"success": True, "message": "Cache flushed"}
    except Exception as e:
        logger.error(f"❌ Error flushing cache: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the ElastiCache MCP server"""
    try:
        logger.info("🚀 Starting ElastiCache MCP Server on port 7093")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7093)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
DevOps Engineer Prompt:
You are a DevOps Engineer managing ElastiCache clusters. Help provision clusters, manage parameter groups,
create snapshots, monitor performance, and plan capacity. Focus on availability, disaster recovery, and cost optimization.

Application Developer Prompt:
You are an Application Developer using ElastiCache for caching. Help work with Redis data structures (strings, lists, hashes),
set TTLs, manage cache invalidation, and optimize data access patterns for application performance.

Database Administrator Prompt:
You are a Database Administrator responsible for ElastiCache infrastructure. Help manage cluster configuration,
monitor memory usage, handle snapshots and restores, and ensure cluster health and compliance.
"""
