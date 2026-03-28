"""
MongoDB MCP Server using FastMCP
Provides tools for MongoDB document database operations
"""

import asyncio
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
import json
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("mongodb-mcp-server")

class MongoDBConnectionPool:
    def __init__(self, uri: str, database: str):
        self.uri = uri
        self.database_name = database
        self.client = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            # Test connection
            self.db.admin.command('ping')
            logger.info("Connected to MongoDB")
        except PyMongoError as err:
            logger.error(f"Error connecting to MongoDB: {err}")
            raise
    
    async def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

db_pool = None

@mcp.tool()
async def list_collections() -> dict:
    """List all collections in the database"""
    try:
        collections = db_pool.db.list_collection_names()
        return {"success": True, "collections": collections}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def find_documents(collection: str, filter: dict = None, limit: int = 10) -> dict:
    """Find documents in a collection"""
    try:
        filter = filter or {}
        query = db_pool.db[collection].find(filter).limit(limit)
        docs = []
        for doc in query:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            docs.append(doc)
        return {"success": True, "documents": docs}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def find_one_document(collection: str, filter: dict) -> dict:
    """Find a single document"""
    try:
        doc = db_pool.db[collection].find_one(filter)
        if doc:
            doc["_id"] = str(doc["_id"])
            return {"success": True, "document": doc}
        return {"success": True, "document": None}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_document(collection: str, document: dict) -> dict:
    """Insert a document"""
    try:
        result = db_pool.db[collection].insert_one(document)
        return {
            "success": True,
            "inserted_id": str(result.inserted_id)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_many(collection: str, documents: list) -> dict:
    """Insert multiple documents"""
    try:
        result = db_pool.db[collection].insert_many(documents)
        ids = [str(id) for id in result.inserted_ids]
        return {
            "success": True,
            "inserted_count": len(ids),
            "inserted_ids": ids
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_document(collection: str, filter: dict, update: dict) -> dict:
    """Update documents"""
    try:
        result = db_pool.db[collection].update_many(filter, {"$set": update})
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_documents(collection: str, filter: dict) -> dict:
    """Delete documents"""
    try:
        result = db_pool.db[collection].delete_many(filter)
        return {
            "success": True,
            "deleted_count": result.deleted_count
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def count_documents(collection: str, filter: dict = None) -> dict:
    """Count documents in collection"""
    try:
        filter = filter or {}
        count = db_pool.db[collection].count_documents(filter)
        return {"success": True, "count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def aggregate(collection: str, pipeline: list) -> dict:
    """Execute aggregation pipeline"""
    try:
        result = list(db_pool.db[collection].aggregate(pipeline))
        for doc in result:
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])
        return {"success": True, "results": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_index(collection: str, field: str, unique: bool = False) -> dict:
    """Create an index"""
    try:
        index_name = db_pool.db[collection].create_index(field, unique=unique)
        return {"success": True, "index_name": index_name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_collection_stats(collection: str) -> dict:
    """Get collection statistics"""
    try:
        stats = db_pool.db.command("collStats", collection)
        return {"success": True, "stats": stats}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database = os.getenv("MONGODB_DATABASE", "test")
    
    db_pool = MongoDBConnectionPool(uri, database)
    await db_pool.connect()
    
    try:
        logger.info("Starting MongoDB MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
