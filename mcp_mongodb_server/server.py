"""
MongoDB MCP Server using FastMCP
Comprehensive MongoDB document database operations with 28 tools
"""

import asyncio
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
import json
import logging
import os
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("MongoDB MCP Server 📀")

# Configuration from environment
MONGODB_CONFIG = {
    "uri": os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
    "database": os.getenv("MONGODB_DATABASE", "test"),
}

def get_mongodb_connection() -> tuple:
    """Get MongoDB client and database with configuration from environment."""
    try:
        client = MongoClient(MONGODB_CONFIG["uri"])
        # Test connection
        client.admin.command('ping')
        db = client[MONGODB_CONFIG["database"]]
        logger.info(f"✅ Connected to MongoDB: {MONGODB_CONFIG['database']}")
        return client, db
    except PyMongoError as e:
        logger.error(f"❌ MongoDB connection error: {str(e)}")
        raise

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize MongoDB document for JSON response."""
    if doc and "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

# ====================== DDL TOOLS (Collection Management) ======================

@mcp.tool()
def mongodb_create_collection(collection_name: str, validation_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a new collection.
    
    Args:
        collection_name: Collection name
        validation_schema: Optional JSON schema for validation
    
    Returns:
        Success status
    """
    try:
        client, db = get_mongodb_connection()
        
        if validation_schema:
            db.create_collection(collection_name, validator={"$jsonSchema": validation_schema})
        else:
            db.create_collection(collection_name)
        
        client.close()
        logger.info(f"🏗️ Collection created: {collection_name}")
        return {"success": True, "message": f"Collection '{collection_name}' created"}
    except PyMongoError as e:
        logger.error(f"❌ Error creating collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_drop_collection(collection_name: str) -> Dict[str, Any]:
    """Drop a collection.
    
    Args:
        collection_name: Collection name to drop
    
    Returns:
        Success status
    """
    try:
        client, db = get_mongodb_connection()
        db[collection_name].drop()
        client.close()
        
        logger.info(f"🗑️ Collection dropped: {collection_name}")
        return {"success": True, "message": f"Collection '{collection_name}' dropped"}
    except PyMongoError as e:
        logger.error(f"❌ Error dropping collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_list_collections() -> Dict[str, Any]:
    """List all collections in the database.
    
    Returns:
        List of collection names
    """
    try:
        client, db = get_mongodb_connection()
        collections = db.list_collection_names()
        client.close()
        
        logger.info(f"📋 Found {len(collections)} collections")
        return {"success": True, "collections": collections, "count": len(collections)}
    except PyMongoError as e:
        logger.error(f"❌ Error listing collections: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_rename_collection(old_name: str, new_name: str) -> Dict[str, Any]:
    """Rename a collection.
    
    Args:
        old_name: Current collection name
        new_name: New collection name
    
    Returns:
        Success status
    """
    try:
        client, db = get_mongodb_connection()
        db[old_name].rename(new_name)
        client.close()
        
        logger.info(f"✏️ Collection renamed: {old_name} → {new_name}")
        return {"success": True, "message": f"Collection renamed to '{new_name}'"}
    except PyMongoError as e:
        logger.error(f"❌ Error renaming collection: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_get_collection_info(collection_name: str) -> Dict[str, Any]:
    """Get collection information and schema.
    
    Args:
        collection_name: Collection name
    
    Returns:
        Collection info and validation rules
    """
    try:
        client, db = get_mongodb_connection()
        
        # Get validation rules
        collection_info = db.command("collStats", collection_name)
        
        # Get indexes
        indexes = db[collection_name].list_indexes()
        
        client.close()
        
        logger.info(f"📊 Collection info retrieved: {collection_name}")
        return {
            "success": True,
            "collection": collection_name,
            "count": collection_info.get("count", 0),
            "size": collection_info.get("size", 0),
            "indexes": [idx["name"] for idx in indexes]
        }
    except PyMongoError as e:
        logger.error(f"❌ Error getting collection info: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS (Document Operations) ======================

@mcp.tool()
def mongodb_insert_document(collection_name: str, document: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single document.
    
    Args:
        collection_name: Collection name
        document: Document data as dictionary
    
    Returns:
        Success status and inserted ID
    """
    try:
        client, db = get_mongodb_connection()
        result = db[collection_name].insert_one(document)
        client.close()
        
        logger.info(f"➕ Document inserted into {collection_name}")
        return {"success": True, "message": "Document inserted", "inserted_id": str(result.inserted_id)}
    except PyMongoError as e:
        logger.error(f"❌ Error inserting document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_insert_many(collection_name: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple documents.
    
    Args:
        collection_name: Collection name
        documents: List of documents
    
    Returns:
        Success status and inserted count
    """
    try:
        client, db = get_mongodb_connection()
        
        if not documents:
            return {"success": True, "message": "No documents to insert", "inserted": 0}
        
        result = db[collection_name].insert_many(documents)
        client.close()
        
        logger.info(f"➕ {len(documents)} documents inserted into {collection_name}")
        return {
            "success": True,
            "message": f"{len(documents)} documents inserted",
            "inserted": len(result.inserted_ids),
            "inserted_ids": [str(id) for id in result.inserted_ids]
        }
    except PyMongoError as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_update_one(collection_name: str, filter_criteria: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a single document.
    
    Args:
        collection_name: Collection name
        filter_criteria: Filter criteria
        update_data: Update data
    
    Returns:
        Success status and update count
    """
    try:
        client, db = get_mongodb_connection()
        result = db[collection_name].update_one(filter_criteria, {"$set": update_data})
        client.close()
        
        logger.info(f"✏️ Document updated in {collection_name}")
        return {
            "success": True,
            "matched": result.matched_count,
            "modified": result.modified_count
        }
    except PyMongoError as e:
        logger.error(f"❌ Error updating document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_update_many(collection_name: str, filter_criteria: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update multiple documents.
    
    Args:
        collection_name: Collection name
        filter_criteria: Filter criteria
        update_data: Update data
    
    Returns:
        Success status and update count
    """
    try:
        client, db = get_mongodb_connection()
        result = db[collection_name].update_many(filter_criteria, {"$set": update_data})
        client.close()
        
        logger.info(f"✏️ {result.modified_count} documents updated in {collection_name}")
        return {
            "success": True,
            "matched": result.matched_count,
            "modified": result.modified_count
        }
    except PyMongoError as e:
        logger.error(f"❌ Error updating documents: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_delete_one(collection_name: str, filter_criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a single document.
    
    Args:
        collection_name: Collection name
        filter_criteria: Filter criteria
    
    Returns:
        Success status and deleted count
    """
    try:
        client, db = get_mongodb_connection()
        result = db[collection_name].delete_one(filter_criteria)
        client.close()
        
        logger.info(f"🗑️ Document deleted from {collection_name}")
        return {
            "success": True,
            "message": f"{result.deleted_count} document deleted",
            "deleted": result.deleted_count
        }
    except PyMongoError as e:
        logger.error(f"❌ Error deleting document: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_delete_many(collection_name: str, filter_criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Delete multiple documents.
    
    Args:
        collection_name: Collection name
        filter_criteria: Filter criteria
    
    Returns:
        Success status and deleted count
    """
    try:
        client, db = get_mongodb_connection()
        result = db[collection_name].delete_many(filter_criteria)
        client.close()
        
        logger.info(f"🗑️ {result.deleted_count} documents deleted from {collection_name}")
        return {
            "success": True,
            "message": f"{result.deleted_count} documents deleted",
            "deleted": result.deleted_count
        }
    except PyMongoError as e:
        logger.error(f"❌ Error deleting documents: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== QUERY/FIND TOOLS ======================

@mcp.tool()
def mongodb_find_documents(collection_name: str, filter_criteria: Optional[Dict[str, Any]] = None, limit: int = 1000) -> Dict[str, Any]:
    """Find documents in a collection.
    
    Args:
        collection_name: Collection name
        filter_criteria: Filter criteria
        limit: Maximum documents to return
    
    Returns:
        Query results
    """
    try:
        client, db = get_mongodb_connection()
        filter_criteria = filter_criteria or {}
        
        docs = list(db[collection_name].find(filter_criteria).limit(limit))
        docs = [serialize_doc(d) for d in docs]
        
        client.close()
        
        logger.info(f"🔎 Found {len(docs)} documents in {collection_name}")
        return {"success": True, "documents": docs, "count": len(docs)}
    except PyMongoError as e:
        logger.error(f"❌ Find error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_find_one(collection_name: str, filter_criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Find a single document.
    
    Args:
        collection_name: Collection name
        filter_criteria: Filter criteria
    
    Returns:
        Document or None
    """
    try:
        client, db = get_mongodb_connection()
        doc = db[collection_name].find_one(filter_criteria)
        client.close()
        
        if doc:
            doc = serialize_doc(doc)
            logger.info(f"🔎 Document found in {collection_name}")
            return {"success": True, "document": doc}
        
        logger.info(f"🔎 No document found in {collection_name}")
        return {"success": True, "document": None}
    except PyMongoError as e:
        logger.error(f"❌ Find one error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_count_documents(collection_name: str, filter_criteria: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Count documents in a collection.
    
    Args:
        collection_name: Collection name
        filter_criteria: Optional filter criteria
    
    Returns:
        Document count
    """
    try:
        client, db = get_mongodb_connection()
        filter_criteria = filter_criteria or {}
        count = db[collection_name].count_documents(filter_criteria)
        client.close()
        
        logger.info(f"🔢 COUNT: {count} documents in {collection_name}")
        return {"success": True, "count": count}
    except PyMongoError as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_find_distinct(collection_name: str, field: str, filter_criteria: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get distinct values for a field.
    
    Args:
        collection_name: Collection name
        field: Field name
        filter_criteria: Optional filter criteria
    
    Returns:
        List of distinct values
    """
    try:
        client, db = get_mongodb_connection()
        filter_criteria = filter_criteria or {}
        values = db[collection_name].distinct(field, filter_criteria)
        client.close()
        
        logger.info(f"🔍 DISTINCT {field}: {len(values)} values")
        return {"success": True, "values": values, "count": len(values)}
    except PyMongoError as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_find_sorted(collection_name: str, sort_field: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Find documents with sorting.
    
    Args:
        collection_name: Collection name
        sort_field: Field to sort by
        direction: ASC or DESC
        limit: Maximum documents
    
    Returns:
        Sorted documents
    """
    try:
        client, db = get_mongodb_connection()
        sort_order = ASCENDING if direction.upper() == "ASC" else DESCENDING
        
        docs = list(db[collection_name].find().sort(sort_field, sort_order).limit(limit))
        docs = [serialize_doc(d) for d in docs]
        
        client.close()
        
        logger.info(f"🔎 Found {len(docs)} documents sorted by {sort_field}")
        return {"success": True, "documents": docs, "count": len(docs)}
    except PyMongoError as e:
        logger.error(f"❌ Sort error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_aggregate(collection_name: str, pipeline: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute aggregation pipeline.
    
    Args:
        collection_name: Collection name
        pipeline: Aggregation pipeline stages
    
    Returns:
        Aggregation results
    """
    try:
        client, db = get_mongodb_connection()
        result = list(db[collection_name].aggregate(pipeline))
        result = [serialize_doc(d) for d in result]
        client.close()
        
        logger.info(f"📊 Aggregation executed: {len(result)} results")
        return {"success": True, "results": result, "count": len(result)}
    except PyMongoError as e:
        logger.error(f"❌ Aggregation error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_group_by(collection_name: str, group_field: str, agg_expr: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Group documents by field.
    
    Args:
        collection_name: Collection name
        group_field: Field to group by
        agg_expr: Aggregation expressions (e.g., {"total": {"$sum": "$amount"}})
    
    Returns:
        Grouped results
    """
    try:
        client, db = get_mongodb_connection()
        
        group_expr = {"_id": f"${group_field}"}
        if agg_expr:
            group_expr.update(agg_expr)
        
        pipeline = [{"$group": group_expr}]
        result = list(db[collection_name].aggregate(pipeline))
        result = [serialize_doc(d) for d in result]
        
        client.close()
        
        logger.info(f"📊 GROUP BY {group_field}: {len(result)} groups")
        return {"success": True, "results": result, "count": len(result)}
    except PyMongoError as e:
        logger.error(f"❌ Group by error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== INDEX/ADMIN TOOLS ======================

@mcp.tool()
def mongodb_create_index(collection_name: str, fields: Dict[str, int], unique: bool = False, sparse: bool = False) -> Dict[str, Any]:
    """Create an index.
    
    Args:
        collection_name: Collection name
        fields: Fields and sort direction {field: 1 (ASC) or -1 (DESC)}
        unique: Create unique index
        sparse: Create sparse index
    
    Returns:
        Success status
    """
    try:
        client, db = get_mongodb_connection()
        index_name = db[collection_name].create_index(
            list(fields.items()),
            unique=unique,
            sparse=sparse
        )
        client.close()
        
        logger.info(f"📑 Index created: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' created"}
    except PyMongoError as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_drop_index(collection_name: str, index_name: str) -> Dict[str, Any]:
    """Drop an index.
    
    Args:
        collection_name: Collection name
        index_name: Index name to drop
    
    Returns:
        Success status
    """
    try:
        client, db = get_mongodb_connection()
        db[collection_name].drop_index(index_name)
        client.close()
        
        logger.info(f"🗑️ Index dropped: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' dropped"}
    except PyMongoError as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_list_indexes(collection_name: str) -> Dict[str, Any]:
    """List all indexes for a collection.
    
    Args:
        collection_name: Collection name
    
    Returns:
        List of indexes
    """
    try:
        client, db = get_mongodb_connection()
        indexes = list(db[collection_name].list_indexes())
        client.close()
        
        logger.info(f"📑 Found {len(indexes)} indexes")
        return {
            "success": True,
            "indexes": [{"name": idx.get("name"), "fields": idx.get("key")} for idx in indexes],
            "count": len(indexes)
        }
    except PyMongoError as e:
        logger.error(f"❌ Error listing indexes: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_get_collection_stats(collection_name: str) -> Dict[str, Any]:
    """Get collection statistics.
    
    Args:
        collection_name: Collection name
    
    Returns:
        Collection stats
    """
    try:
        client, db = get_mongodb_connection()
        stats = db.command("collStats", collection_name)
        client.close()
        
        logger.info(f"📊 Collection stats retrieved: {collection_name}")
        return {
            "success": True,
            "collection": collection_name,
            "document_count": stats.get("count", 0),
            "collection_size_mb": round(stats.get("size", 0) / (1024 * 1024), 2),
            "avg_document_size": stats.get("avgObjSize", 0),
            "storage_size_mb": round(stats.get("storageSize", 0) / (1024 * 1024), 2)
        }
    except PyMongoError as e:
        logger.error(f"❌ Error getting collection stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mongodb_validate_collection(collection_name: str) -> Dict[str, Any]:
    """Validate a collection.
    
    Args:
        collection_name: Collection name
    
    Returns:
        Validation results
    """
    try:
        client, db = get_mongodb_connection()
        result = db.command("validate", collection_name)
        client.close()
        
        logger.info(f"✅ Collection validation: {collection_name}")
        return {
            "success": True,
            "valid": result.get("valid", False),
            "details": result.get("errors", [])
        }
    except PyMongoError as e:
        logger.error(f"❌ Error validating collection: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a MongoDB Database Administrator. Your role is to:
- Create and manage collections with validation rules
- Manage indexes for optimal performance
- Monitor collection statistics and storage
- Perform collection maintenance and validation
- Manage collection structure and naming

Use these tools for DBA tasks:
- mongodb_create_collection, mongodb_drop_collection, mongodb_list_collections
- mongodb_rename_collection, mongodb_get_collection_info
- mongodb_create_index, mongodb_drop_index, mongodb_list_indexes
- mongodb_get_collection_stats, mongodb_validate_collection
"""

DATA_ENGINEER_PROMPT = """You are a MongoDB Data Engineer. Your role is to:
- Design efficient document schemas
- Build and maintain data pipelines
- Load and transform data
- Ensure data quality and consistency
- Manage bulk operations

Use these tools for data engineering:
- mongodb_insert_document, mongodb_insert_many
- mongodb_update_one, mongodb_update_many
- mongodb_delete_one, mongodb_delete_many
- mongodb_find_documents for validation
- mongodb_aggregate for ETL operations
"""

DATA_ANALYST_PROMPT = """You are a MongoDB Data Analyst. Your role is to:
- Query and analyze document data
- Generate insights and reports
- Explore data patterns and trends
- Create analytical queries

Use these tools for analysis:
- mongodb_find_documents, mongodb_find_one for exploration
- mongodb_count_documents, mongodb_find_distinct
- mongodb_aggregate, mongodb_group_by for statistics
- mongodb_find_sorted for trend analysis
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting MongoDB MCP Server...")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7087"))
    )

if __name__ == "__main__":
    asyncio.run(main())
