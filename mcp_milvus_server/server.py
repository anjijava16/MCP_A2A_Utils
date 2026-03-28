"""
Milvus MCP Server using FastMCP
Provides tools for Milvus vector database operations
"""

import asyncio
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("milvus-mcp-server")

class MilvusConnectionPool:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        
        connections.connect("default", host=host, port=port)
        logger.info(f"Connected to Milvus: {host}:{port}")

db_pool = None

@mcp.tool()
async def list_collections() -> dict:
    """List all collections"""
    try:
        from pymilvus import utility
        collections = utility.list_collections()
        return {"success": True, "collections": collections}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_collection_info(collection_name: str) -> dict:
    """Get collection information"""
    try:
        collection = Collection(collection_name)
        
        return {
            "success": True,
            "info": {
                "name": collection_name,
                "num_entities": collection.num_entities,
                "fields": [field.name for field in collection.schema.fields]
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_vectors(collection_name: str, vectors_data: list) -> dict:
    """Insert vectors into collection"""
    try:
        collection = Collection(collection_name)
        # vectors_data should be list of lists matching schema
        mr = collection.insert(vectors_data)
        collection.flush()
        
        return {
            "success": True,
            "inserted_count": len(vectors_data),
            "primary_keys": mr.primary_keys
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_vectors(collection_name: str, query_vector: list, top_k: int = 10) -> dict:
    """Search for similar vectors"""
    try:
        collection = Collection(collection_name)
        
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10}
        }
        
        results = collection.search(
            data=[query_vector],
            anns_field="embeddings",
            param=search_params,
            limit=top_k,
            output_fields=["*"]
        )
        
        matches = []
        for hits in results:
            for hit in hits:
                matches.append({
                    "id": hit.id,
                    "distance": hit.distance,
                    "entity": hit.entity.to_dict() if hasattr(hit, "entity") else {}
                })
        
        return {"success": True, "matches": matches}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_entities(collection_name: str, ids: list) -> dict:
    """Delete entities by ID"""
    try:
        collection = Collection(collection_name)
        
        # Create expression for deletion
        expr = f"pk in {ids}"
        collection.delete(expr)
        collection.flush()
        
        return {"success": True, "message": f"Deleted {len(ids)} entities"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def flush_collection(collection_name: str) -> dict:
    """Flush collection to disk"""
    try:
        collection = Collection(collection_name)
        collection.flush()
        return {"success": True, "message": "Collection flushed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_partition(collection_name: str, partition_name: str) -> dict:
    """Create partition in collection"""
    try:
        collection = Collection(collection_name)
        collection.create_partition(partition_name)
        return {"success": True, "message": f"Partition {partition_name} created"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_partition(collection_name: str, partition_name: str) -> dict:
    """Drop partition from collection"""
    try:
        collection = Collection(collection_name)
        collection.drop_partition(partition_name)
        return {"success": True, "message": f"Partition {partition_name} dropped"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_index(collection_name: str, field_name: str, index_params: dict) -> dict:
    """Create index on field"""
    try:
        collection = Collection(collection_name)
        collection.create_index(field_name, index_params)
        return {"success": True, "message": f"Index created on {field_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_collection_stats(collection_name: str) -> dict:
    """Get collection statistics"""
    try:
        collection = Collection(collection_name)
        
        return {
            "success": True,
            "stats": {
                "collection_name": collection_name,
                "num_entities": collection.num_entities,
                "partitions": len(collection.partitions)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    host = os.getenv("MILVUS_HOST", "localhost")
    port = int(os.getenv("MILVUS_PORT", "19530"))
    
    db_pool = MilvusConnectionPool(host, port)
    
    try:
        logger.info("Starting Milvus MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
