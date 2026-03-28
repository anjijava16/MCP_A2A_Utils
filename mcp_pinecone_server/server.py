"""
Pinecone MCP Server 📌
Comprehensive MCP server for Pinecone vector database operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Tuple
from pinecone import Pinecone, ServerlessSpec, PodSpec
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Pinecone 📌")

def get_pinecone_client():
    """Get Pinecone client connection"""
    api_key = os.getenv("PINECONE_API_KEY")
    
    if not api_key:
        raise ValueError("PINECONE_API_KEY environment variable is required")
    
    try:
        client = Pinecone(api_key=api_key)
        return client
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

# ==================== INDEX MANAGEMENT ====================

@mcp.tool()
async def list_indexes() -> dict:
    """📋 List all indexes"""
    try:
        client = get_pinecone_client()
        indexes = client.list_indexes()
        
        index_list = [
            {
                "name": idx.get("name"),
                "dimension": idx.get("dimension"),
                "metric": idx.get("metric"),
                "status": idx.get("status"),
                "spec": idx.get("spec")
            }
            for idx in indexes.get("indexes", [])
        ]
        
        logger.info(f"✅ Found {len(index_list)} indexes")
        return {"success": True, "indexes": index_list, "count": len(index_list)}
    except Exception as e:
        logger.error(f"❌ Error listing indexes: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_index(index_name: str) -> dict:
    """🔎 Get index details"""
    try:
        client = get_pinecone_client()
        info = client.describe_index(index_name)
        
        details = {
            "name": info.get("name"),
            "dimension": info.get("dimension"),
            "metric": info.get("metric"),
            "status": info.get("status"),
            "host": info.get("host"),
            "spec": info.get("spec")
        }
        
        logger.info(f"✅ Retrieved index details")
        return {"success": True, "index": details}
    except Exception as e:
        logger.error(f"❌ Error describing index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_index(index_name: str, dimension: int, metric: str = "cosine", 
                       serverless: bool = True, region: str = "us-east-1") -> dict:
    """✨ Create new index"""
    try:
        client = get_pinecone_client()
        
        if serverless:
            spec = ServerlessSpec(cloud="aws", region=region)
        else:
            spec = PodSpec(environment="production")
        
        client.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=spec
        )
        
        logger.info(f"✅ Index {index_name} creation initiated")
        return {"success": True, "message": f"Index {index_name} creation initiated"}
    except Exception as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_index(index_name: str) -> dict:
    """❌ Delete index (irreversible)"""
    try:
        client = get_pinecone_client()
        client.delete_index(index_name)
        
        logger.info(f"✅ Index {index_name} deleted")
        return {"success": True, "message": f"Index {index_name} deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def scale_index(index_name: str, replicas: int) -> dict:
    """⚡ Scale index replicas"""
    try:
        client = get_pinecone_client()
        client.scale_index(index_name, desired_replicas=replicas)
        
        logger.info(f"✅ Index {index_name} scaled to {replicas} replicas")
        return {"success": True, "message": f"Scaled to {replicas} replicas"}
    except Exception as e:
        logger.error(f"❌ Error scaling index: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== VECTOR OPERATIONS ====================

@mcp.tool()
async def upsert_vectors(index_name: str, vectors: List[Tuple[str, List[float], Dict]], namespace: str = "") -> dict:
    """✍️ Upsert vectors (insert or update)"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        # vectors format: [(id, values, metadata), ...]
        index.upsert(vectors=vectors, namespace=namespace)
        
        logger.info(f"✅ Upserted {len(vectors)} vectors")
        return {"success": True, "upserted_count": len(vectors)}
    except Exception as e:
        logger.error(f"❌ Error upserting vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_vectors(index_name: str, query_vector: List[float], top_k: int = 10, 
                        namespace: str = "", filter: Optional[Dict] = None) -> dict:
    """🔍 Query similar vectors"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        results = index.query(
            vector=query_vector,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True,
            filter=filter
        )
        
        matches = [
            {
                "id": match.get("id"),
                "score": match.get("score"),
                "metadata": match.get("metadata", {})
            }
            for match in results.get("matches", [])
        ]
        
        logger.info(f"✅ Query returned {len(matches)} matches")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error querying vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_vector(index_name: str, vector_id: str, namespace: str = "") -> dict:
    """📖 Get specific vector"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        result = index.fetch(ids=[vector_id], namespace=namespace)
        vectors = result.get("vectors", {})
        
        if vector_id in vectors:
            vec = vectors[vector_id]
            vector_info = {
                "id": vector_id,
                "values": vec.get("values"),
                "metadata": vec.get("metadata", {})
            }
            logger.info(f"✅ Retrieved vector {vector_id}")
            return {"success": True, "vector": vector_info}
        else:
            logger.error(f"❌ Vector not found: {vector_id}")
            return {"success": False, "error": "Vector not found"}
    except Exception as e:
        logger.error(f"❌ Error getting vector: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def fetch_vectors(index_name: str, vector_ids: List[str], namespace: str = "") -> dict:
    """🎯 Fetch multiple vectors"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        result = index.fetch(ids=vector_ids, namespace=namespace)
        vectors_dict = result.get("vectors", {})
        
        vectors = [
            {
                "id": vid,
                "values": vec.get("values"),
                "metadata": vec.get("metadata", {})
            }
            for vid, vec in vectors_dict.items()
        ]
        
        logger.info(f"✅ Fetched {len(vectors)} vectors")
        return {"success": True, "vectors": vectors, "count": len(vectors)}
    except Exception as e:
        logger.error(f"❌ Error fetching vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_vectors(index_name: str, vector_ids: List[str], namespace: str = "") -> dict:
    """🗑️ Delete vectors"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        index.delete(ids=vector_ids, namespace=namespace)
        
        logger.info(f"✅ Deleted {len(vector_ids)} vectors")
        return {"success": True, "deleted_count": len(vector_ids)}
    except Exception as e:
        logger.error(f"❌ Error deleting vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_all_in_namespace(index_name: str, namespace: str) -> dict:
    """🧹 Delete all vectors in namespace"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        index.delete(delete_all=True, namespace=namespace)
        
        logger.info(f"✅ Deleted all vectors in namespace {namespace}")
        return {"success": True, "message": f"Deleted namespace {namespace}"}
    except Exception as e:
        logger.error(f"❌ Error deleting namespace: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_vector_metadata(index_name: str, vector_id: str, metadata: Dict, namespace: str = "") -> dict:
    """🔄 Update vector metadata"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        index.update(id=vector_id, set_metadata=metadata, namespace=namespace)
        
        logger.info(f"✅ Updated metadata for {vector_id}")
        return {"success": True, "message": "Metadata updated"}
    except Exception as e:
        logger.error(f"❌ Error updating metadata: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== NAMESPACE OPERATIONS ====================

@mcp.tool()
async def list_namespaces(index_name: str) -> dict:
    """📋 List all namespaces in index"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        stats = index.describe_index_stats()
        namespaces = list(stats.get("namespaces", {}).keys())
        
        ns_info = [
            {
                "name": ns,
                "vector_count": stats["namespaces"][ns].get("vector_count", 0)
            }
            for ns in namespaces
        ]
        
        logger.info(f"✅ Found {len(ns_info)} namespaces")
        return {"success": True, "namespaces": ns_info, "count": len(ns_info)}
    except Exception as e:
        logger.error(f"❌ Error listing namespaces: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_namespace_stats(index_name: str, namespace: str = "") -> dict:
    """📊 Get namespace statistics"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        stats = index.describe_index_stats()
        ns_stats = stats.get("namespaces", {}).get(namespace, {})
        
        info = {
            "namespace": namespace,
            "vector_count": ns_stats.get("vector_count", 0),
            "dimension": stats.get("dimension")
        }
        
        logger.info(f"✅ Retrieved namespace stats")
        return {"success": True, "stats": info}
    except Exception as e:
        logger.error(f"❌ Error getting namespace stats: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== COLLECTION OPERATIONS ====================

@mcp.tool()
async def list_collections() -> dict:
    """📚 List all collections"""
    try:
        client = get_pinecone_client()
        collections = client.list_collections()
        
        collection_list = [
            {
                "name": col.get("name"),
                "size": col.get("size"),
                "status": col.get("status")
            }
            for col in collections.get("collections", [])
        ]
        
        logger.info(f"✅ Found {len(collection_list)} collections")
        return {"success": True, "collections": collection_list, "count": len(collection_list)}
    except Exception as e:
        logger.error(f"❌ Error listing collections: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_collection(collection_name: str, index_name: str) -> dict:
    """✨ Create collection from index"""
    try:
        client = get_pinecone_client()
        client.create_collection(
            name=collection_name,
            source=index_name
        )
        
        logger.info(f"✅ Collection {collection_name} created")
        return {"success": True, "message": f"Collection {collection_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_collection(collection_name: str) -> dict:
    """🗑️ Delete collection"""
    try:
        client = get_pinecone_client()
        client.delete_collection(collection_name)
        
        logger.info(f"✅ Collection {collection_name} deleted")
        return {"success": True, "message": f"Collection {collection_name} deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_collection(collection_name: str) -> dict:
    """🔎 Get collection details"""
    try:
        client = get_pinecone_client()
        info = client.describe_collection(collection_name)
        
        details = {
            "name": info.get("name"),
            "size": info.get("size"),
            "status": info.get("status"),
            "dimension": info.get("dimension")
        }
        
        logger.info(f"✅ Retrieved collection details")
        return {"success": True, "collection": details}
    except Exception as e:
        logger.error(f"❌ Error describing collection: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== INDEX STATISTICS & MONITORING ====================

@mcp.tool()
async def get_index_stats(index_name: str) -> dict:
    """📊 Get index statistics"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        stats = index.describe_index_stats()
        
        info = {
            "total_vectors": stats.get("total_vector_count", 0),
            "dimension": stats.get("dimension"),
            "index_fullness": stats.get("index_fullness", 0),
            "namespace_count": len(stats.get("namespaces", {}))
        }
        
        logger.info(f"✅ Retrieved index statistics")
        return {"success": True, "stats": info}
    except Exception as e:
        logger.error(f"❌ Error getting index stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_vector_count(index_name: str, namespace: str = "") -> dict:
    """📈 Get vector count"""
    try:
        client = get_pinecone_client()
        index = client.Index(index_name)
        
        stats = index.describe_index_stats()
        ns_stats = stats.get("namespaces", {}).get(namespace, {})
        count = ns_stats.get("vector_count", 0)
        
        logger.info(f"✅ Vector count: {count}")
        return {"success": True, "vector_count": count}
    except Exception as e:
        logger.error(f"❌ Error getting vector count: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Pinecone MCP server"""
    try:
        logger.info("🚀 Starting Pinecone MCP Server on port 7094")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7094)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
ML Engineer Prompt:
You are an ML Engineer using Pinecone for vector embeddings and semantic search. Help manage indexes,
upsert vector embeddings from models, query for similar vectors, and organize vectors with namespaces.

Data Architect Prompt:
You are a Data Architect designing vector database schemas. Help design index structures, plan namespace
organization for different use cases, create collections for backup/reference, and monitor index health.

Application Developer Prompt:
You are an Application Developer building semantic search features. Help query vectors, manage metadata,
update embeddings, and integrate vector similarity search into applications at scale.
"""
