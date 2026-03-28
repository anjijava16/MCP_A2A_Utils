"""
OpenSearch MCP Server 🔍
Comprehensive MCP server for OpenSearch search and analytics operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from opensearchpy import OpenSearch
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("OpenSearch 🔍")

def get_opensearch_connection():
    """Get OpenSearch client connection"""
    hosts = os.getenv("OPENSEARCH_HOSTS", "localhost:9200").split(",")
    username = os.getenv("OPENSEARCH_USER", "admin")
    password = os.getenv("OPENSEARCH_PASSWORD", "AdminPassword123!")
    use_ssl = os.getenv("OPENSEARCH_USE_SSL", "true").lower() == "true"
    
    try:
        client = OpenSearch(
            hosts=hosts,
            http_auth=(username, password),
            use_ssl=use_ssl,
            verify_certs=False,
            ssl_show_warn=False
        )
        return client
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

# ==================== INDEX MANAGEMENT ====================

@mcp.tool()
async def list_indices() -> dict:
    """📋 List all indices"""
    try:
        client = get_opensearch_connection()
        indices = client.cat.indices(format="json")
        
        index_list = [
            {
                "name": idx.get("index"),
                "status": idx.get("status"),
                "doc_count": int(idx.get("docs.count", 0)),
                "store_size": idx.get("store.size", "N/A"),
                "replicas": idx.get("rep")
            }
            for idx in indices
        ]
        
        logger.info(f"✅ Found {len(index_list)} indices")
        return {"success": True, "indices": index_list, "count": len(index_list)}
    except Exception as e:
        logger.error(f"❌ Error listing indices: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_index(index_name: str, shards: int = 1, replicas: int = 0, 
                       mappings: Optional[Dict] = None) -> dict:
    """✨ Create new index"""
    try:
        client = get_opensearch_connection()
        
        body = {
            "settings": {
                "index": {
                    "number_of_shards": shards,
                    "number_of_replicas": replicas
                }
            }
        }
        
        if mappings:
            body["mappings"] = mappings
        
        client.indices.create(index=index_name, body=body)
        
        logger.info(f"✅ Index {index_name} created")
        return {"success": True, "message": f"Index {index_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_index(index_name: str) -> dict:
    """❌ Delete index (irreversible)"""
    try:
        client = get_opensearch_connection()
        client.indices.delete(index=index_name)
        
        logger.info(f"✅ Index {index_name} deleted")
        return {"success": True, "message": f"Index {index_name} deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_index(index_name: str) -> dict:
    """🔎 Get index details"""
    try:
        client = get_opensearch_connection()
        response = client.indices.get(index=index_name)
        
        index_info = response.get(index_name, {})
        
        details = {
            "name": index_name,
            "shards": index_info.get("settings", {}).get("index", {}).get("number_of_shards"),
            "replicas": index_info.get("settings", {}).get("index", {}).get("number_of_replicas"),
            "status": index_info.get("status")
        }
        
        logger.info(f"✅ Retrieved index details")
        return {"success": True, "index": details}
    except Exception as e:
        logger.error(f"❌ Error describing index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def open_index(index_name: str) -> dict:
    """🔓 Open closed index"""
    try:
        client = get_opensearch_connection()
        client.indices.open(index=index_name)
        
        logger.info(f"✅ Index {index_name} opened")
        return {"success": True, "message": f"Index {index_name} opened"}
    except Exception as e:
        logger.error(f"❌ Error opening index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def close_index(index_name: str) -> dict:
    """🔒 Close index"""
    try:
        client = get_opensearch_connection()
        client.indices.close(index=index_name)
        
        logger.info(f"✅ Index {index_name} closed")
        return {"success": True, "message": f"Index {index_name} closed"}
    except Exception as e:
        logger.error(f"❌ Error closing index: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DOCUMENT OPERATIONS ====================

@mcp.tool()
async def index_document(index_name: str, doc_id: str, document: Dict) -> dict:
    """✍️ Index single document"""
    try:
        client = get_opensearch_connection()
        result = client.index(index=index_name, id=doc_id, body=document)
        
        logger.info(f"✅ Document indexed: {doc_id}")
        return {"success": True, "message": "Document indexed", "id": result.get("_id")}
    except Exception as e:
        logger.error(f"❌ Error indexing document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_document(index_name: str, doc_id: str) -> dict:
    """📖 Get document by ID"""
    try:
        client = get_opensearch_connection()
        result = client.get(index=index_name, id=doc_id)
        
        logger.info(f"✅ Retrieved document {doc_id}")
        return {"success": True, "document": result.get("_source"), "id": result.get("_id")}
    except Exception as e:
        logger.error(f"❌ Error getting document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_document(index_name: str, doc_id: str, updates: Dict) -> dict:
    """🔄 Update document fields"""
    try:
        client = get_opensearch_connection()
        body = {"doc": updates}
        client.update(index=index_name, id=doc_id, body=body)
        
        logger.info(f"✅ Document updated: {doc_id}")
        return {"success": True, "message": "Document updated"}
    except Exception as e:
        logger.error(f"❌ Error updating document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_document(index_name: str, doc_id: str) -> dict:
    """🗑️ Delete document"""
    try:
        client = get_opensearch_connection()
        client.delete(index=index_name, id=doc_id)
        
        logger.info(f"✅ Document deleted: {doc_id}")
        return {"success": True, "message": "Document deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def bulk_index(index_name: str, documents: List[Dict]) -> dict:
    """📦 Bulk index multiple documents"""
    try:
        client = get_opensearch_connection()
        
        operations = []
        for doc in documents:
            operations.append({"index": {"_index": index_name, "_id": doc.get("id")}})
            operations.append(doc.get("data", {}))
        
        result = client.bulk(body=operations)
        
        logger.info(f"✅ Bulk indexed {len(documents)} documents")
        return {
            "success": True,
            "indexed_count": len(documents),
            "errors": result.get("errors", False)
        }
    except Exception as e:
        logger.error(f"❌ Error bulk indexing: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SEARCH OPERATIONS ====================

@mcp.tool()
async def search_documents(index_name: str, query: Dict, size: int = 10, from_: int = 0) -> dict:
    """🔍 Search documents"""
    try:
        client = get_opensearch_connection()
        
        body = {
            "query": query,
            "size": size,
            "from": from_
        }
        
        result = client.search(index=index_name, body=body)
        
        hits = [
            {
                "id": hit.get("_id"),
                "score": hit.get("_score"),
                "document": hit.get("_source")
            }
            for hit in result.get("hits", {}).get("hits", [])
        ]
        
        total = result.get("hits", {}).get("total", {}).get("value", 0)
        
        logger.info(f"✅ Search returned {len(hits)} hits")
        return {"success": True, "hits": hits, "total": total}
    except Exception as e:
        logger.error(f"❌ Error searching: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def advanced_search(index_name: str, query_string: str, fields: Optional[List[str]] = None) -> dict:
    """⚡ Advanced query string search"""
    try:
        client = get_opensearch_connection()
        
        query = {"query_string": {"query": query_string}}
        if fields:
            query["query_string"]["fields"] = fields
        
        body = {"query": query, "size": 100}
        result = client.search(index=index_name, body=body)
        
        hits = [
            {
                "id": hit.get("_id"),
                "score": hit.get("_score"),
                "document": hit.get("_source")
            }
            for hit in result.get("hits", {}).get("hits", [])
        ]
        
        logger.info(f"✅ Advanced search returned {len(hits)} hits")
        return {"success": True, "hits": hits, "count": len(hits)}
    except Exception as e:
        logger.error(f"❌ Error in advanced search: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def count_documents(index_name: str, query: Optional[Dict] = None) -> dict:
    """📈 Count documents matching query"""
    try:
        client = get_opensearch_connection()
        
        body = {"query": query} if query else {}
        result = client.count(index=index_name, body=body)
        count = result.get("count", 0)
        
        logger.info(f"✅ Document count: {count}")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ Error counting documents: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def aggregate_documents(index_name: str, aggregation: Dict) -> dict:
    """📊 Run aggregation query"""
    try:
        client = get_opensearch_connection()
        
        body = {"aggs": aggregation, "size": 0}
        result = client.search(index=index_name, body=body)
        
        agg_results = result.get("aggregations", {})
        
        logger.info(f"✅ Aggregation completed")
        return {"success": True, "aggregations": agg_results}
    except Exception as e:
        logger.error(f"❌ Error in aggregation: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_by_query(index_name: str, query: Dict) -> dict:
    """🧹 Delete documents by query"""
    try:
        client = get_opensearch_connection()
        
        body = {"query": query}
        result = client.delete_by_query(index=index_name, body=body)
        
        deleted = result.get("deleted", 0)
        
        logger.info(f"✅ Deleted {deleted} documents")
        return {"success": True, "deleted_count": deleted}
    except Exception as e:
        logger.error(f"❌ Error deleting by query: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== INDEX SETTINGS & MAPPINGS ====================

@mcp.tool()
async def get_index_mappings(index_name: str) -> dict:
    """🗺️ Get index field mappings"""
    try:
        client = get_opensearch_connection()
        mappings = client.indices.get_mapping(index=index_name)
        
        index_mappings = mappings.get(index_name, {}).get("mappings", {})
        
        logger.info(f"✅ Retrieved mappings")
        return {"success": True, "mappings": index_mappings}
    except Exception as e:
        logger.error(f"❌ Error getting mappings: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_index_settings(index_name: str) -> dict:
    """⚙️ Get index settings"""
    try:
        client = get_opensearch_connection()
        settings = client.indices.get_settings(index=index_name)
        
        index_settings = settings.get(index_name, {}).get("settings", {})
        
        logger.info(f"✅ Retrieved settings")
        return {"success": True, "settings": index_settings}
    except Exception as e:
        logger.error(f"❌ Error getting settings: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_index_settings(index_name: str, settings: Dict) -> dict:
    """🔧 Update index settings"""
    try:
        client = get_opensearch_connection()
        body = {"settings": settings}
        client.indices.put_settings(body=body, index=index_name)
        
        logger.info(f"✅ Index settings updated")
        return {"success": True, "message": "Settings updated"}
    except Exception as e:
        logger.error(f"❌ Error updating settings: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ADMIN & MONITORING ====================

@mcp.tool()
async def get_cluster_health() -> dict:
    """❤️ Get cluster health status"""
    try:
        client = get_opensearch_connection()
        health = client.cluster.health()
        
        status = {
            "status": health.get("status"),
            "active_shards": health.get("active_shards"),
            "relocating_shards": health.get("relocating_shards"),
            "initializing_shards": health.get("initializing_shards"),
            "unassigned_shards": health.get("unassigned_shards"),
            "nodes": health.get("number_of_nodes")
        }
        
        logger.info(f"✅ Retrieved cluster health")
        return {"success": True, "health": status}
    except Exception as e:
        logger.error(f"❌ Error getting cluster health: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_cluster_stats() -> dict:
    """📊 Get cluster statistics"""
    try:
        client = get_opensearch_connection()
        stats = client.cluster.stats()
        
        cluster_stats = {
            "nodes": stats.get("nodes", {}).get("count", {}).get("total"),
            "indices": stats.get("indices", {}).get("count"),
            "total_docs": stats.get("indices", {}).get("docs", {}).get("count"),
            "total_size_bytes": stats.get("indices", {}).get("store", {}).get("size_in_bytes")
        }
        
        logger.info(f"✅ Retrieved cluster stats")
        return {"success": True, "stats": cluster_stats}
    except Exception as e:
        logger.error(f"❌ Error getting cluster stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_index_stats(index_name: str) -> dict:
    """📈 Get index statistics"""
    try:
        client = get_opensearch_connection()
        stats = client.indices.stats(index=index_name)
        
        index_stats = stats.get("indices", {}).get(index_name, {})
        
        stats_info = {
            "doc_count": index_stats.get("primaries", {}).get("docs", {}).get("count"),
            "store_size": index_stats.get("primaries", {}).get("store", {}).get("size_in_bytes"),
            "indexing_ops": index_stats.get("primaries", {}).get("indexing", {}).get("index_total")
        }
        
        logger.info(f"✅ Retrieved index statistics")
        return {"success": True, "stats": stats_info}
    except Exception as e:
        logger.error(f"❌ Error getting index stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def optimize_index(index_name: str, max_num_segments: int = 1) -> dict:
    """⚡ Optimize/force merge index"""
    try:
        client = get_opensearch_connection()
        client.indices.forcemerge(index=index_name, max_num_segments=max_num_segments)
        
        logger.info(f"✅ Index {index_name} optimized")
        return {"success": True, "message": f"Index optimized"}
    except Exception as e:
        logger.error(f"❌ Error optimizing index: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the OpenSearch MCP server"""
    try:
        logger.info("🚀 Starting OpenSearch MCP Server on port 7095")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7095)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
Search Engineer Prompt:
You are a Search Engineer building search functionality with OpenSearch. Help create indexes,
design mappings, write search queries, configure analyzers, and optimize query performance.

Data Analyst Prompt:
You are a Data Analyst using OpenSearch for log and metrics analysis. Help search logs,
run aggregations, create dashboards queries, and analyze trends in data.

DevOps Engineer Prompt:
You are a DevOps Engineer managing OpenSearch infrastructure. Help monitor cluster health,
manage indices, optimize performance, handle backups, and ensure availability.
"""
