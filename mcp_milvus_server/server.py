"""
Milvus MCP Server 🚀
Comprehensive MCP server for Milvus vector database operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Milvus 🚀")

def get_milvus_connection():
    """Get Milvus connection"""
    host = os.getenv("MILVUS_HOST", "localhost")
    port = int(os.getenv("MILVUS_PORT", "19530"))
    
    try:
        connections.connect("default", host=host, port=port)
        return True
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

# ==================== COLLECTION MANAGEMENT ====================

@mcp.tool()
async def list_collections() -> dict:
    """📋 List all collections"""
    try:
        get_milvus_connection()
        collections = utility.list_collections()
        
        logger.info(f"✅ Found {len(collections)} collections")
        return {"success": True, "collections": collections, "count": len(collections)}
    except Exception as e:
        logger.error(f"❌ Error listing collections: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_collection(collection_name: str, fields: List[Dict], metric_type: str = "L2") -> dict:
    """✨ Create new collection"""
    try:
        get_milvus_connection()
        
        # fields format: [{"name": "id", "dtype": DataType.INT64}, {"name": "embedding", "dtype": DataType.FLOAT_VECTOR, "dim": 768}]
        field_schemas = []
        for field in fields:
            if field.get("dtype") == "FLOAT_VECTOR":
                field_schemas.append(
                    FieldSchema(name=field["name"], dtype=DataType.FLOAT_VECTOR, dim=field.get("dim", 768))
                )
            elif field.get("dtype") == "INT64":
                field_schemas.append(
                    FieldSchema(name=field["name"], dtype=DataType.INT64, is_primary=field.get("is_primary", False))
                )
            else:
                field_schemas.append(
                    FieldSchema(name=field["name"], dtype=DataType.VARCHAR, max_length=65535)
                )
        
        schema = CollectionSchema(fields=field_schemas, description=f"Collection {collection_name}")
        collection = Collection(name=collection_name, schema=schema)
        
        logger.info(f"✅ Collection {collection_name} created")
        return {"success": True, "message": f"Collection {collection_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_collection(collection_name: str) -> dict:
    """❌ Drop collection (irreversible)"""
    try:
        get_milvus_connection()
        utility.drop_collection(collection_name)
        
        logger.info(f"✅ Collection {collection_name} dropped")
        return {"success": True, "message": f"Collection {collection_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_collection(collection_name: str) -> dict:
    """🔎 Get collection details"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        info = {
            "name": collection_name,
            "num_entities": collection.num_entities,
            "fields": [field.name for field in collection.schema.fields],
            "partitions": collection.partitions
        }
        
        logger.info(f"✅ Retrieved collection details")
        return {"success": True, "collection": info}
    except Exception as e:
        logger.error(f"❌ Error describing collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def load_collection(collection_name: str) -> dict:
    """⬆️ Load collection into memory"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.load()
        
        logger.info(f"✅ Collection {collection_name} loaded")
        return {"success": True, "message": f"Collection loaded"}
    except Exception as e:
        logger.error(f"❌ Error loading collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def release_collection(collection_name: str) -> dict:
    """⬇️ Release collection from memory"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.release()
        
        logger.info(f"✅ Collection {collection_name} released")
        return {"success": True, "message": f"Collection released"}
    except Exception as e:
        logger.error(f"❌ Error releasing collection: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ENTITY OPERATIONS ====================

@mcp.tool()
async def insert_vectors(collection_name: str, data: List[List]) -> dict:
    """✍️ Insert vector entities"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        mr = collection.insert(data)
        collection.flush()
        
        logger.info(f"✅ Inserted {len(data)} entities")
        return {"success": True, "inserted_count": len(data), "primary_keys": mr.primary_keys[:10]}
    except Exception as e:
        logger.error(f"❌ Error inserting vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def upsert_vectors(collection_name: str, data: List[List]) -> dict:
    """🔄 Upsert vector entities (insert or update)"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        mr = collection.upsert(data)
        collection.flush()
        
        logger.info(f"✅ Upserted {len(data)} entities")
        return {"success": True, "upserted_count": len(data)}
    except Exception as e:
        logger.error(f"❌ Error upserting vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_entities(collection_name: str, entity_ids: List[int]) -> dict:
    """🗑️ Delete entities by ID"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        expr = f"pk in {entity_ids}"
        collection.delete(expr)
        collection.flush()
        
        logger.info(f"✅ Deleted {len(entity_ids)} entities")
        return {"success": True, "deleted_count": len(entity_ids)}
    except Exception as e:
        logger.error(f"❌ Error deleting entities: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_entity(collection_name: str, entity_id: int) -> dict:
    """📖 Get entity by ID"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        expr = f"pk == {entity_id}"
        results = collection.query(expr=expr, output_fields=["*"])
        
        if results:
            logger.info(f"✅ Retrieved entity {entity_id}")
            return {"success": True, "entity": results[0]}
        else:
            logger.error(f"❌ Entity not found: {entity_id}")
            return {"success": False, "error": "Entity not found"}
    except Exception as e:
        logger.error(f"❌ Error getting entity: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SEARCH OPERATIONS ====================

@mcp.tool()
async def search_vectors(collection_name: str, query_vector: List[float], top_k: int = 10, metric_type: str = "L2") -> dict:
    """🔍 Search for similar vectors"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        search_params = {"metric_type": metric_type, "params": {"nprobe": 10}}
        
        results = collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["*"]
        )
        
        matches = []
        for hits in results:
            for hit in hits:
                matches.append({
                    "id": hit.id,
                    "distance": float(hit.distance),
                    "entity": hit.entity.to_dict() if hasattr(hit, "entity") else {}
                })
        
        logger.info(f"✅ Search returned {len(matches)} matches")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error searching vectors: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_by_ids(collection_name: str, query_ids: List[int], top_k: int = 10) -> dict:
    """🎯 Search by entity IDs"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        # Get vectors for these IDs first
        expr = f"pk in {query_ids}"
        entities = collection.query(expr=expr, output_fields=["*"])
        
        matches = []
        for entity in entities:
            matches.append({"id": entity.get("pk"), "entity": entity})
        
        logger.info(f"✅ Retrieved {len(matches)} entities by ID")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error searching by IDs: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def hybrid_search(collection_name: str, query_vector: List[float], filter_expr: Optional[str] = None, top_k: int = 10) -> dict:
    """⚡ Hybrid search with filtering"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        
        results = collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=filter_expr,
            output_fields=["*"]
        )
        
        matches = [
            {"id": hit.id, "distance": float(hit.distance)}
            for hits in results
            for hit in hits
        ]
        
        logger.info(f"✅ Hybrid search returned {len(matches)} results")
        return {"success": True, "matches": matches, "count": len(matches)}
    except Exception as e:
        logger.error(f"❌ Error in hybrid search: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== PARTITION OPERATIONS ====================

@mcp.tool()
async def list_partitions(collection_name: str) -> dict:
    """📋 List collection partitions"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        partitions = [p.name for p in collection.partitions]
        
        logger.info(f"✅ Found {len(partitions)} partitions")
        return {"success": True, "partitions": partitions, "count": len(partitions)}
    except Exception as e:
        logger.error(f"❌ Error listing partitions: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_partition(collection_name: str, partition_name: str) -> dict:
    """✨ Create partition"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.create_partition(partition_name)
        
        logger.info(f"✅ Partition {partition_name} created")
        return {"success": True, "message": f"Partition {partition_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating partition: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_partition(collection_name: str, partition_name: str) -> dict:
    """🗑️ Drop partition"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.drop_partition(partition_name)
        
        logger.info(f"✅ Partition {partition_name} dropped")
        return {"success": True, "message": f"Partition {partition_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping partition: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def load_partition(collection_name: str, partition_name: str) -> dict:
    """⬆️ Load partition into memory"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.load([partition_name])
        
        logger.info(f"✅ Partition {partition_name} loaded")
        return {"success": True, "message": f"Partition loaded"}
    except Exception as e:
        logger.error(f"❌ Error loading partition: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== INDEX OPERATIONS ====================

@mcp.tool()
async def create_index(collection_name: str, field_name: str, index_type: str = "IVF_FLAT") -> dict:
    """🔑 Create index on field"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        index_params = {
            "metric_type": "L2",
            "index_type": index_type,
            "params": {"nlist": 1024} if index_type == "IVF_FLAT" else {}
        }
        
        collection.create_index(field_name, index_params)
        
        logger.info(f"✅ Index created on {field_name}")
        return {"success": True, "message": f"Index created"}
    except Exception as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_index(collection_name: str, field_name: str) -> dict:
    """🗑️ Drop index"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.drop_index()
        
        logger.info(f"✅ Index dropped")
        return {"success": True, "message": f"Index dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_index(collection_name: str) -> dict:
    """🔎 Get index details"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        index = collection.indexes[0] if collection.indexes else None
        
        if index:
            info = {"type": index.index_type, "field_name": index.field_name}
            logger.info(f"✅ Retrieved index details")
            return {"success": True, "index": info}
        else:
            return {"success": False, "error": "No index found"}
    except Exception as e:
        logger.error(f"❌ Error describing index: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== STATISTICS & MONITORING ====================

@mcp.tool()
async def get_collection_stats(collection_name: str) -> dict:
    """📊 Get collection statistics"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        
        stats = {
            "name": collection_name,
            "num_entities": collection.num_entities,
            "num_partitions": len(collection.partitions),
            "loaded": collection.loaded
        }
        
        logger.info(f"✅ Retrieved collection statistics")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_entity_count(collection_name: str) -> dict:
    """📈 Get entity count"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        count = collection.num_entities
        
        logger.info(f"✅ Entity count: {count}")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ Error getting entity count: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def flush_collection(collection_name: str) -> dict:
    """💾 Flush collection to disk"""
    try:
        get_milvus_connection()
        collection = Collection(collection_name)
        collection.flush()
        
        logger.info(f"✅ Collection {collection_name} flushed")
        return {"success": True, "message": "Collection flushed"}
    except Exception as e:
        logger.error(f"❌ Error flushing collection: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Milvus MCP server"""
    try:
        logger.info("🚀 Starting Milvus MCP Server on port 7096")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7096)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
ML Engineer Prompt:
You are an ML Engineer using Milvus for large-scale vector similarity search. Help manage collections,
insert embeddings, create indexes for fast retrieval, and optimize search performance for ML models.

Data Scientist Prompt:
You are a Data Scientist working with vector embeddings in Milvus. Help organize vectors by partitions,
analyze search results, and refine embedding strategies for better similarity matching.

Backend Engineer Prompt:
You are a Backend Engineer building scalable similarity search services with Milvus. Help design 
collection schemas, manage load/release operations, and optimize vector indexing for production workloads.
"""
