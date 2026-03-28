"""
Qdrant MCP Server 🎯
Comprehensive MCP server for Qdrant vector database operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter, 
    FieldCondition, MatchValue, HasIdCondition
)
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Qdrant 🎯")

def get_qdrant_connection():
    """Get Qdrant client connection"""
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", None)
    
    try:
        if api_key:
            client = QdrantClient(url=url, api_key=api_key)
        else:
            client = QdrantClient(url=url)
        
        return client
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

# ==================== COLLECTION MANAGEMENT ====================

@mcp.tool()
async def list_collections() -> dict:
    """📋 List all collections"""
    try:
        client = get_qdrant_connection()
        collections = client.get_collections()
        collection_names = [coll.name for coll in collections.collections]
        
        logger.info(f"✅ Found {len(collection_names)} collections")
        return {"success": True, "collections": collection_names, "count": len(collection_names)}
    except Exception as e:
        logger.error(f"❌ Error listing collections: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_collection(collection_name: str) -> dict:
    """🔎 Get collection details"""
    try:
        client = get_qdrant_connection()
        info = client.get_collection(collection_name)
        
        details = {
            "name": collection_name,
            "points_count": info.points_count,
            "vectors_count": getattr(info, 'vectors_count', 'N/A'),
            "indexed_vectors_count": getattr(info, 'indexed_vectors_count', 'N/A'),
            "status": str(info.status)
        }
        
        logger.info(f"✅ Retrieved collection details")
        return {"success": True, "collection": details}
    except Exception as e:
        logger.error(f"❌ Error describing collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_collection(collection_name: str, vector_size: int, distance: str = "Cosine") -> dict:
    """✨ Create new collection"""
    try:
        client = get_qdrant_connection()
        
        distance_metric = Distance[distance.upper()]
        
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance_metric
            )
        )
        
        logger.info(f"✅ Collection {collection_name} created")
        return {"success": True, "message": f"Collection {collection_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_collection(collection_name: str) -> dict:
    """❌ Delete collection (irreversible)"""
    try:
        client = get_qdrant_connection()
        client.delete_collection(collection_name)
        
        logger.info(f"✅ Collection {collection_name} deleted")
        return {"success": True, "message": f"Collection {collection_name} deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def collection_exists(collection_name: str) -> dict:
    """🔍 Check if collection exists"""
    try:
        client = get_qdrant_connection()
        client.collection_exists(collection_name)
        
        logger.info(f"✅ Collection exists")
        return {"success": True, "exists": True}
    except Exception as e:
        logger.error(f"❌ Collection not found")
        return {"success": True, "exists": False}

# ==================== POINT OPERATIONS - UPSERT/INSERT ====================

@mcp.tool()
async def upsert_points(collection_name: str, points: List[Dict]) -> dict:
    """📝 Upsert points (insert or update)"""
    try:
        client = get_qdrant_connection()
        
        point_structs = [
            PointStruct(
                id=p.get("id"),
                vector=p.get("vector"),
                payload=p.get("payload", {})
            )
            for p in points
        ]
        
        client.upsert(
            collection_name=collection_name,
            points=point_structs
        )
        
        logger.info(f"✅ Upserted {len(points)} points")
        return {"success": True, "upserted_count": len(points)}
    except Exception as e:
        logger.error(f"❌ Error upserting points: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_upsert_points(collection_name: str, points: List[Dict], batch_size: int = 100) -> dict:
    """⚡ Batch upsert large point sets"""
    try:
        client = get_qdrant_connection()
        
        total_upserted = 0
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            point_structs = [
                PointStruct(
                    id=p.get("id"),
                    vector=p.get("vector"),
                    payload=p.get("payload", {})
                )
                for p in batch
            ]
            
            client.upsert(
                collection_name=collection_name,
                points=point_structs
            )
            total_upserted += len(batch)
        
        logger.info(f"✅ Batch upserted {total_upserted} points")
        return {"success": True, "total_upserted": total_upserted}
    except Exception as e:
        logger.error(f"❌ Error batch upserting: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== POINT OPERATIONS - RETRIEVE ====================

@mcp.tool()
async def get_point(collection_name: str, point_id: int) -> dict:
    """📖 Get point by ID"""
    try:
        client = get_qdrant_connection()
        points = client.retrieve(
            collection_name=collection_name,
            ids=[point_id],
            with_vectors=True
        )
        
        if points:
            p = points[0]
            result = {
                "id": p.id,
                "vector": p.vector,
                "payload": p.payload
            }
            logger.info(f"✅ Retrieved point {point_id}")
            return {"success": True, "point": result}
        else:
            logger.error(f"❌ Point not found: {point_id}")
            return {"success": False, "error": "Point not found"}
    except Exception as e:
        logger.error(f"❌ Error getting point: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_points(collection_name: str, point_ids: List[int]) -> dict:
    """🔠 Get multiple points by IDs"""
    try:
        client = get_qdrant_connection()
        points = client.retrieve(
            collection_name=collection_name,
            ids=point_ids,
            with_vectors=True
        )
        
        results = [
            {
                "id": p.id,
                "vector": p.vector[:5] if len(p.vector) > 5 else p.vector,  # Truncate vectors in response
                "payload": p.payload
            }
            for p in points
        ]
        
        logger.info(f"✅ Retrieved {len(results)} points")
        return {"success": True, "points": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ Error getting points: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SEARCH OPERATIONS ====================

@mcp.tool()
async def search_points(collection_name: str, query_vector: List[float], top_k: int = 10, score_threshold: Optional[float] = None) -> dict:
    """🔍 Search for similar vectors"""
    try:
        client = get_qdrant_connection()
        
        results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold
        )
        
        matches = [
            {
                "id": result.id,
                "score": float(result.score),
                "payload": result.payload
            }
            for result in results
        ]
        
        logger.info(f"✅ Search returned {len(matches)} matches")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error searching points: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_with_filter(collection_name: str, query_vector: List[float], filter_expr: Dict, top_k: int = 10) -> dict:
    """🎯 Search with metadata filtering"""
    try:
        client = get_qdrant_connection()
        
        # Convert dict to Filter object (simplified)
        results = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=filter_expr
        )
        
        matches = [
            {
                "id": result.id,
                "score": float(result.score),
                "payload": result.payload
            }
            for result in results
        ]
        
        logger.info(f"✅ Filtered search returned {len(matches)} matches")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error searching with filter: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def recommend_vectors(collection_name: str, positive_ids: List[int], negative_ids: Optional[List[int]] = None, top_k: int = 10) -> dict:
    """💡 Recommend vectors based on positive examples"""
    try:
        client = get_qdrant_connection()
        
        results = client.recommend(
            collection_name=collection_name,
            positive=positive_ids,
            negative=negative_ids or [],
            limit=top_k
        )
        
        matches = [
            {
                "id": result.id,
                "score": float(result.score),
                "payload": result.payload
            }
            for result in results
        ]
        
        logger.info(f"✅ Recommendation returned {len(matches)} matches")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error getting recommendations: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== POINT DELETION ====================

@mcp.tool()
async def delete_point(collection_name: str, point_id: int) -> dict:
    """🗑️ Delete point by ID"""
    try:
        client = get_qdrant_connection()
        client.delete(
            collection_name=collection_name,
            points_selector=[point_id]
        )
        
        logger.info(f"✅ Deleted point {point_id}")
        return {"success": True, "message": "Point deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting point: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_points(collection_name: str, point_ids: List[int]) -> dict:
    """🗑️ Delete multiple points"""
    try:
        client = get_qdrant_connection()
        client.delete(
            collection_name=collection_name,
            points_selector=point_ids
        )
        
        logger.info(f"✅ Deleted {len(point_ids)} points")
        return {"success": True, "deleted_count": len(point_ids)}
    except Exception as e:
        logger.error(f"❌ Error deleting points: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SCROLLING & PAGINATION ====================

@mcp.tool()
async def scroll_points(collection_name: str, limit: int = 10, offset: int = 0, with_vectors: bool = False) -> dict:
    """📜 Scroll through points with pagination"""
    try:
        client = get_qdrant_connection()
        
        points, next_offset = client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset,
            with_vectors=with_vectors
        )
        
        result_points = [
            {
                "id": p.id,
                "payload": p.payload
            }
            for p in points
        ]
        
        logger.info(f"✅ Scrolled {len(result_points)} points")
        return {
            "success": True,
            "points": result_points,
            "count": len(result_points),
            "next_offset": next_offset
        }
    except Exception as e:
        logger.error(f"❌ Error scrolling points: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== STATISTICS ====================

@mcp.tool()
async def count_points(collection_name: str) -> dict:
    """📊 Count points in collection"""
    try:
        client = get_qdrant_connection()
        count = client.count(collection_name)
        
        logger.info(f"✅ Point count: {count.count}")
        return {"success": True, "count": count.count}
    except Exception as e:
        logger.error(f"❌ Error counting points: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_collection_stats(collection_name: str) -> dict:
    """📈 Get collection statistics"""
    try:
        client = get_qdrant_connection()
        info = client.get_collection(collection_name)
        
        stats = {
            "name": collection_name,
            "points_count": info.points_count,
            "vectors_count": getattr(info, 'vectors_count', 0),
            "indexed_vectors_count": getattr(info, 'indexed_vectors_count', 0),
            "status": str(info.status)
        }
        
        logger.info(f"✅ Retrieved collection stats")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SNAPSHOTS (BACKUPS) ====================

@mcp.tool()
async def create_snapshot(collection_name: str) -> dict:
    """💾 Create collection snapshot"""
    try:
        client = get_qdrant_connection()
        snapshot_result = client.create_snapshot(collection_name)
        
        logger.info(f"✅ Snapshot created")
        return {"success": True, "snapshot_name": snapshot_result}
    except Exception as e:
        logger.error(f"❌ Error creating snapshot: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_snapshots(collection_name: str) -> dict:
    """📋 List snapshots for collection"""
    try:
        client = get_qdrant_connection()
        snapshots = client.list_snapshots(collection_name)
        
        snapshot_names = [s.name for s in snapshots]
        logger.info(f"✅ Found {len(snapshot_names)} snapshots")
        return {"success": True, "snapshots": snapshot_names, "count": len(snapshot_names)}
    except Exception as e:
        logger.error(f"❌ Error listing snapshots: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ALIASES ====================

@mcp.tool()
async def create_alias(alias_name: str, collection_name: str) -> dict:
    """🔗 Create collection alias"""
    try:
        client = get_qdrant_connection()
        client.create_alias(alias_name, collection_name)
        
        logger.info(f"✅ Alias {alias_name} created")
        return {"success": True, "message": f"Alias {alias_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating alias: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_aliases(collection_name: str) -> dict:
    """🔍 List aliases for collection"""
    try:
        client = get_qdrant_connection()
        aliases = client.get_aliases()
        
        col_aliases = [a.alias_name for a in aliases.aliases if a.collection_name == collection_name]
        logger.info(f"✅ Found {len(col_aliases)} aliases")
        return {"success": True, "aliases": col_aliases, "count": len(col_aliases)}
    except Exception as e:
        logger.error(f"❌ Error listing aliases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_alias(alias_name: str) -> dict:
    """🗑️ Delete alias"""
    try:
        client = get_qdrant_connection()
        client.delete_alias(alias_name)
        
        logger.info(f"✅ Alias {alias_name} deleted")
        return {"success": True, "message": f"Alias {alias_name} deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting alias: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== INDEXING ====================

@mcp.tool()
async def update_payload(collection_name: str, point_ids: List[int], payload_update: Dict) -> dict:
    """💾 Update point payloads"""
    try:
        client = get_qdrant_connection()
        client.set_payload(
            collection_name=collection_name,
            payload=payload_update,
            points=point_ids
        )
        
        logger.info(f"✅ Updated payloads for {len(point_ids)} points")
        return {"success": True, "updated_count": len(point_ids)}
    except Exception as e:
        logger.error(f"❌ Error updating payloads: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_payload_keys(collection_name: str, point_ids: List[int], keys: List[str]) -> dict:
    """🗑️ Delete specific payload keys"""
    try:
        client = get_qdrant_connection()
        client.delete_payload(
            collection_name=collection_name,
            keys=keys,
            points=point_ids
        )
        
        logger.info(f"✅ Deleted payload keys from {len(point_ids)} points")
        return {"success": True, "updated_count": len(point_ids)}
    except Exception as e:
        logger.error(f"❌ Error deleting payload keys: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Qdrant MCP server"""
    try:
        logger.info("🎯 Starting Qdrant MCP Server on port 7097")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7097)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
ML Engineer Prompt:
You are an ML Engineer using Qdrant for similarity search in production. Manage vector collections,
perform semantic searches with filtering, handle batch operations, and optimize search performance
for machine learning applications.

Vector Architect Prompt:
You are a Vector Data Architect designing efficient vector databases with Qdrant. Help design
collection schemas, manage indexes, create snapshots for disaster recovery, and optimize vector storage
and retrieval strategies.

Application Developer Prompt:
You are an Application Developer building vector-powered features with Qdrant. Help manage point
lifecycle (create/update/delete), implement recommendation engines, and integrate vector search
into production applications.
"""
    api_key = os.getenv("QDRANT_API_KEY")
    
    db_pool = QdrantConnectionPool(url, api_key)
    
    try:
        logger.info("Starting Qdrant MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
