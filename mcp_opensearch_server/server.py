"""
OpenSearch MCP Server using FastMCP
Provides tools for OpenSearch operations (Elasticsearch alternative)
"""

import asyncio
from opensearchpy import OpenSearch
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("opensearch-mcp-server")

class OpenSearchConnectionPool:
    def __init__(self, hosts: list, username: str, password: str, use_ssl: bool = True):
        self.hosts = hosts
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        
        self.client = OpenSearch(
            hosts=hosts,
            http_auth=(username, password),
            use_ssl=use_ssl,
            verify_certs=use_ssl,
            ssl_show_warn=False
        )
        logger.info(f"Connected to OpenSearch: {hosts}")

db_pool = None

@mcp.tool()
async def list_indices() -> dict:
    """List all indices"""
    try:
        indices = db_pool.client.cat.indices(format="json")
        index_list = [idx["index"] for idx in indices]
        return {"success": True, "indices": index_list}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_index(index_name: str, settings: dict = None, mappings: dict = None) -> dict:
    """Create new index"""
    try:
        body = {}
        if settings:
            body["settings"] = settings
        if mappings:
            body["mappings"] = mappings
        
        db_pool.client.indices.create(index=index_name, body=body if body else None)
        return {"success": True, "message": f"Index {index_name} created"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_index(index_name: str) -> dict:
    """Delete index"""
    try:
        db_pool.client.indices.delete(index=index_name)
        return {"success": True, "message": f"Index {index_name} deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def index_document(index_name: str, doc_id: str, document: dict) -> dict:
    """Index a document"""
    try:
        result = db_pool.client.index(index=index_name, id=doc_id, body=document)
        return {
            "success": True,
            "message": "Document indexed",
            "id": result["_id"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_document(index_name: str, doc_id: str) -> dict:
    """Get document by ID"""
    try:
        result = db_pool.client.get(index=index_name, id=doc_id)
        return {
            "success": True,
            "document": result["_source"],
            "id": result["_id"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_documents(index_name: str, query: dict, size: int = 10) -> dict:
    """Search documents"""
    try:
        search_body = {"query": query, "size": size}
        result = db_pool.client.search(index=index_name, body=search_body)
        
        hits = []
        for hit in result["hits"]["hits"]:
            hits.append({
                "id": hit["_id"],
                "score": hit["_score"],
                "document": hit["_source"]
            })
        
        return {
            "success": True,
            "hits": hits,
            "total": result["hits"]["total"].get("value", 0)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_document(index_name: str, doc_id: str) -> dict:
    """Delete document by ID"""
    try:
        db_pool.client.delete(index=index_name, id=doc_id)
        return {"success": True, "message": "Document deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def bulk_index(index_name: str, documents: list) -> dict:
    """Bulk index documents"""
    try:
        operations = []
        for doc in documents:
            operations.append({"index": {"_index": index_name, "_id": doc.get("id")}})
            operations.append(doc.get("data", {}))
        
        result = db_pool.client.bulk(body=operations)
        return {
            "success": True,
            "message": f"Indexed {len(documents)} documents",
            "errors": result.get("errors", False)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_index_stats(index_name: str) -> dict:
    """Get index statistics"""
    try:
        stats = db_pool.client.indices.stats(index=index_name)
        index_stats = stats["indices"].get(index_name, {})
        
        return {
            "success": True,
            "stats": {
                "docs": index_stats.get("primaries", {}).get("docs", {}),
                "store": index_stats.get("primaries", {}).get("store", {}),
                "indexing": index_stats.get("primaries", {}).get("indexing", {})
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    hosts = os.getenv("OPENSEARCH_HOSTS", "localhost:9200").split(",")
    username = os.getenv("OPENSEARCH_USER", "admin")
    password = os.getenv("OPENSEARCH_PASSWORD", "AdminPassword123!")
    use_ssl = os.getenv("OPENSEARCH_USE_SSL", "true").lower() == "true"
    
    db_pool = OpenSearchConnectionPool(hosts, username, password, use_ssl)
    
    try:
        logger.info("Starting OpenSearch MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
