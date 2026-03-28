"""
Qdrant MCP Server using FastMCP
Provides tools for Qdrant vector database operations
"""

import asyncio
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("qdrant-mcp-server")

class QdrantConnectionPool:
    def __init__(self, url: str, api_key: str = None):
        self.url = url
        self.api_key = api_key
        
        if api_key:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            self.client = QdrantClient(url=url)
        
        logger.info(f"Connected to Qdrant: {url}")

db_pool = None

@mcp.tool()
async def list_collections() -> dict:
    """List all collections"""
    try:
        collections = db_pool.client.get_collections()
        collection_names = [coll.name for coll in collections.collections]
        return {"success": True, "collections": collection_names}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def collection_info(collection_name: str) -> dict:
    """Get collection information"""
    try:
        info = db_pool.client.get_collection(collection_name)
        return {
            "success": True,
            "info": {
                "name": collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "indexed_vectors_count": info.indexed_vectors_count
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def upsert_points(collection_name: str, points: list) -> dict:
    """Upsert points into collection"""
    try:
        # points should be list of PointStruct objs with id, vector, payload
        point_structs = [
            PointStruct(
                id=p.get("id"),
                vector=p.get("vector"),
                payload=p.get("payload", {})
            )
            for p in points
        ]
        
        db_pool.client.upsert(
            collection_name=collection_name,
            points=point_structs
        )
        
        return {"success": True, "message": f"Upserted {len(points)} points"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_points(collection_name: str, query_vector: list, top_k: int = 10, filter_cond: dict = None) -> dict:
    """Search for similar points"""
    try:
        results = db_pool.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=filter_cond
        )
        
        matches = [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            }
            for result in results
        ]
        
        return {"success": True, "matches": matches}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_point(collection_name: str, point_id: int) -> dict:
    """Get specific point"""
    try:
        point = db_pool.client.retrieve(
            collection_name=collection_name,
            ids=[point_id]
        )
        
        if point:
            p = point[0]
            return {
                "success": True,
                "point": {
                    "id": p.id,
                    "vector": p.vector,
                    "payload": p.payload
                }
            }
        else:
            return {"success": False, "error": "Point not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_point(collection_name: str, point_id: int) -> dict:
    """Delete point by ID"""
    try:
        db_pool.client.delete(
            collection_name=collection_name,
            points_selector=[point_id]
        )
        return {"success": True, "message": "Point deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_collection(collection_name: str) -> dict:
    """Delete entire collection"""
    try:
        db_pool.client.delete_collection(collection_name)
        return {"success": True, "message": f"Collection {collection_name} deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def count_points(collection_name: str) -> dict:
    """Count points in collection"""
    try:
        count = db_pool.client.count(collection_name)
        return {"success": True, "count": count.count}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def scroll_points(collection_name: str, limit: int = 10, offset: int = 0) -> dict:
    """Scroll through points"""
    try:
        points, next_offset = db_pool.client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset
        )
        
        result_points = [
            {
                "id": p.id,
                "vector": p.vector,
                "payload": p.payload
            }
            for p in points
        ]
        
        return {
            "success": True,
            "points": result_points,
            "next_offset": next_offset
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_server_info() -> dict:
    """Get Qdrant server information"""
    try:
        info = db_pool.client.get_lock()
        return {"success": True, "status": "healthy"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY")
    
    db_pool = QdrantConnectionPool(url, api_key)
    
    try:
        logger.info("Starting Qdrant MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
