"""
Pinecone MCP Server using FastMCP
Provides tools for Pinecone vector database operations
"""

import asyncio
from pinecone import Pinecone
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("pinecone-mcp-server")

class PineconeConnectionPool:
    def __init__(self, api_key: str, environment: str = None):
        self.api_key = api_key
        self.environment = environment
        
        kwargs = {"api_key": api_key}
        if environment:
            kwargs["environment"] = environment
        
        self.client = Pinecone(**kwargs)
        logger.info("Connected to Pinecone")

db_pool = None

@mcp.tool()
async def list_indexes() -> dict:
    """List all Pinecone indexes"""
    try:
        indexes = db_pool.client.list_indexes()
        index_names = [idx.get("name") for idx in indexes]
        return {"success": True, "indexes": index_names}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_index_stats(index_name: str) -> dict:
    """Get index statistics"""
    try:
        index = db_pool.client.Index(index_name)
        stats = index.describe_index_stats()
        return {
            "success": True,
            "stats": {
                "dimension": stats.get("dimension"),
                "index_fullness": stats.get("index_fullness"),
                "namespaces": stats.get("namespaces", {})
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def upsert_vectors(index_name: str, vectors: list, namespace: str = "") -> dict:
    """Upsert vectors into index"""
    try:
        index = db_pool.client.Index(index_name)
        # vectors should be list of (id, values, metadata) tuples
        index.upsert(vectors=vectors, namespace=namespace)
        return {"success": True, "message": f"Upserted {len(vectors)} vectors"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_vectors(index_name: str, query_vector: list, top_k: int = 10, namespace: str = "") -> dict:
    """Query similar vectors"""
    try:
        index = db_pool.client.Index(index_name)
        results = index.query(
            vector=query_vector,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True
        )
        
        matches = []
        for match in results.get("matches", []):
            matches.append({
                "id": match.get("id"),
                "score": match.get("score"),
                "metadata": match.get("metadata", {})
            })
        
        return {"success": True, "matches": matches}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_vector(index_name: str, vector_id: str, namespace: str = "") -> dict:
    """Get specific vector"""
    try:
        index = db_pool.client.Index(index_name)
        result = index.fetch(ids=[vector_id], namespace=namespace)
        
        vectors = result.get("vectors", {})
        if vector_id in vectors:
            vec = vectors[vector_id]
            return {
                "success": True,
                "vector": {
                    "id": vector_id,
                    "values": vec.get("values"),
                    "metadata": vec.get("metadata", {})
                }
            }
        else:
            return {"success": False, "error": "Vector not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_vectors(index_name: str, vector_ids: list, namespace: str = "") -> dict:
    """Delete vectors from index"""
    try:
        index = db_pool.client.Index(index_name)
        index.delete(ids=vector_ids, namespace=namespace)
        return {"success": True, "message": f"Deleted {len(vector_ids)} vectors"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_namespace(index_name: str, namespace: str) -> dict:
    """Delete entire namespace"""
    try:
        index = db_pool.client.Index(index_name)
        index.delete(delete_all=True, namespace=namespace)
        return {"success": True, "message": f"Deleted namespace: {namespace}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_vector_metadata(index_name: str, vector_id: str, metadata: dict, namespace: str = "") -> dict:
    """Update vector metadata"""
    try:
        index = db_pool.client.Index(index_name)
        index.update(id=vector_id, set_metadata=metadata, namespace=namespace)
        return {"success": True, "message": "Metadata updated"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT")
    
    if not api_key:
        raise ValueError("PINECONE_API_KEY environment variable is required")
    
    db_pool = PineconeConnectionPool(api_key, environment)
    
    try:
        logger.info("Starting Pinecone MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
