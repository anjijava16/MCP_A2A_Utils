"""
ADK Documentation MCP Server 📚
Custom Python FastMCP server for Google Agent Development Kit documentation
"""

import asyncio
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
import httpx
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("ADK-Docs 📚")

# Cache for documentation
_doc_cache = {
    "content": None,
    "last_updated": None,
    "sections": {}
}

async def fetch_adk_docs() -> str:
    """Fetch ADK documentation from official source"""
    try:
        url = "https://google.github.io/adk-docs/llms.txt"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            logger.info("✅ ADK documentation fetched successfully")
            return response.text
    except Exception as e:
        logger.error(f"❌ Error fetching ADK docs: {str(e)}")
        raise

async def ensure_docs_loaded():
    """Load docs into cache if not already present"""
    if _doc_cache["content"] is None:
        try:
            _doc_cache["content"] = await fetch_adk_docs()
            _doc_cache["last_updated"] = datetime.now().isoformat()
            _parse_sections()
            logger.info("✅ Documentation loaded and parsed")
        except Exception as e:
            logger.error(f"❌ Failed to load documentation: {str(e)}")
            raise

def _parse_sections():
    """Parse documentation into sections for indexing"""
    content = _doc_cache["content"]
    
    # Split by major sections (lines starting with # or ##)
    sections = re.split(r'^(#{1,3}\s+.*?)$', content, flags=re.MULTILINE)
    
    current_section = "Overview"
    for i, section in enumerate(sections):
        if section.startswith('#'):
            current_section = section.strip('#').strip()
        else:
            if current_section not in _doc_cache["sections"]:
                _doc_cache["sections"][current_section] = []
            _doc_cache["sections"][current_section].append(section)

# ==================== DOCUMENTATION RETRIEVAL ====================

@mcp.tool()
async def search_adk_docs(query: str, max_results: int = 5) -> dict:
    """🔍 Search ADK documentation for specific terms"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"].lower()
        query_lower = query.lower()
        
        # Find all occurrences with context
        matches = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if query_lower in line:
                # Get context (3 lines before and after)
                start = max(0, i - 3)
                end = min(len(lines), i + 4)
                context = '\n'.join(lines[start:end])
                
                matches.append({
                    "line": i + 1,
                    "match": line.strip(),
                    "context": context
                })
        
        matches = matches[:max_results]
        logger.info(f"✅ Found {len(matches)} matches for '{query}'")
        return {
            "success": True,
            "query": query,
            "matches": matches,
            "count": len(matches)
        }
    except Exception as e:
        logger.error(f"❌ Error searching docs: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_adk_overview() -> dict:
    """📖 Get overview of ADK documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        # Get first 2000 characters as overview
        overview = content[:2000] if len(content) > 2000 else content
        
        logger.info("✅ Retrieved ADK overview")
        return {
            "success": True,
            "overview": overview,
            "total_chars": len(content),
            "last_updated": _doc_cache["last_updated"]
        }
    except Exception as e:
        logger.error(f"❌ Error getting overview: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_adk_sections() -> dict:
    """📋 List all sections in ADK documentation"""
    try:
        await ensure_docs_loaded()
        
        sections = list(_doc_cache["sections"].keys())
        
        logger.info(f"✅ Listed {len(sections)} sections")
        return {
            "success": True,
            "sections": sections,
            "count": len(sections)
        }
    except Exception as e:
        logger.error(f"❌ Error listing sections: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_adk_section(section_name: str) -> dict:
    """🔎 Get specific section from documentation"""
    try:
        await ensure_docs_loaded()
        
        if section_name not in _doc_cache["sections"]:
            # Try fuzzy match
            matches = [s for s in _doc_cache["sections"].keys() if section_name.lower() in s.lower()]
            if not matches:
                return {"success": False, "error": f"Section '{section_name}' not found"}
            section_name = matches[0]
        
        content = '\n'.join(_doc_cache["sections"][section_name])
        
        logger.info(f"✅ Retrieved section: {section_name}")
        return {
            "success": True,
            "section": section_name,
            "content": content,
            "length": len(content)
        }
    except Exception as e:
        logger.error(f"❌ Error getting section: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_guides() -> dict:
    """📚 Search for guides and tutorials in documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"].lower()
        
        # Look for guide-related terms
        keywords = ['guide', 'tutorial', 'example', 'quickstart', 'howto', 'step']
        results = {}
        
        for keyword in keywords:
            if keyword in content:
                results[keyword] = content.count(keyword)
        
        logger.info(f"✅ Found guide references: {len(results)}")
        return {
            "success": True,
            "guide_types": results,
            "message": "Use search_adk_docs() with specific guide names for detailed content"
        }
    except Exception as e:
        logger.error(f"❌ Error searching guides: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== API REFERENCE ====================

@mcp.tool()
async def search_api_reference(api_name: str) -> dict:
    """🔌 Search for API reference in documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        
        # Look for class/function definitions with backticks or code blocks
        patterns = [
            f'`{api_name}',
            f'class {api_name}',
            f'def {api_name}',
            f'## {api_name}',
            f'### {api_name}'
        ]
        
        matches = {}
        for pattern in patterns:
            count = content.count(pattern)
            if count > 0:
                matches[pattern] = count
        
        if not matches:
            logger.warning(f"⚠️ No API reference found for: {api_name}")
            return {
                "success": False,
                "message": f"No API reference found for '{api_name}'. Try searching with search_adk_docs()."
            }
        
        logger.info(f"✅ Found API reference patterns for {api_name}")
        return {
            "success": True,
            "api_name": api_name,
            "patterns_found": matches
        }
    except Exception as e:
        logger.error(f"❌ Error searching API reference: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_full_documentation() -> dict:
    """📄 Get complete documentation content"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        
        logger.info(f"✅ Retrieved full documentation ({len(content)} chars)")
        return {
            "success": True,
            "content": content,
            "length": len(content),
            "lines": len(content.split('\n')),
            "last_updated": _doc_cache["last_updated"]
        }
    except Exception as e:
        logger.error(f"❌ Error getting full documentation: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DOCUMENTATION UTILITIES ====================

@mcp.tool()
async def get_doc_stats() -> dict:
    """📊 Get documentation statistics"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        
        stats = {
            "total_characters": len(content),
            "total_lines": len(content.split('\n')),
            "total_sections": len(_doc_cache["sections"]),
            "last_updated": _doc_cache["last_updated"],
            "has_code_blocks": '```' in content,
            "code_blocks_count": content.count('```') // 2
        }
        
        logger.info("✅ Retrieved documentation statistics")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def reload_documentation() -> dict:
    """🔄 Reload documentation from remote source"""
    try:
        # Clear cache and reload
        _doc_cache["content"] = None
        _doc_cache["last_updated"] = None
        _doc_cache["sections"] = {}
        
        await ensure_docs_loaded()
        
        logger.info("✅ Documentation reloaded successfully")
        return {
            "success": True,
            "message": "Documentation reloaded from remote source",
            "last_updated": _doc_cache["last_updated"]
        }
    except Exception as e:
        logger.error(f"❌ Error reloading documentation: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def extract_code_examples() -> dict:
    """💻 Extract code examples from documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        
        # Extract code blocks
        code_blocks = re.findall(r'```(?:python|py)?\n(.*?)\n```', content, re.DOTALL)
        
        logger.info(f"✅ Found {len(code_blocks)} code examples")
        return {
            "success": True,
            "code_blocks": code_blocks[:10],  # Return first 10
            "total_code_blocks": len(code_blocks),
            "message": "Showing first 10 code blocks"
        }
    except Exception as e:
        logger.error(f"❌ Error extracting code: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def find_related_topics(topic: str, related_count: int = 5) -> dict:
    """🔗 Find related topics in documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"].lower()
        topic_lower = topic.lower()
        
        lines = content.split('\n')
        topic_context = []
        
        for i, line in enumerate(lines):
            if topic_lower in line:
                # Get surrounding lines as related topics
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                context = ' '.join(lines[start:end])
                topic_context.append(context)
        
        related = topic_context[:related_count]
        
        logger.info(f"✅ Found {len(related)} related topics for '{topic}'")
        return {
            "success": True,
            "topic": topic,
            "related_sections": related,
            "count": len(related)
        }
    except Exception as e:
        logger.error(f"❌ Error finding related topics: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the ADK Documentation MCP server"""
    try:
        logger.info("📚 Starting ADK Documentation MCP Server on port 7099")
        # Pre-load docs on startup
        await ensure_docs_loaded()
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7099)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
ADK Developer Prompt:
You are an Agent Development Kit (ADK) expert. Help developers understand and implement
ADK features, patterns, and best practices. Reference the official documentation for
accurate information about agents, tools, and orchestration.

ADK Architect Prompt:
You are designing agentic systems using ADK. Help design agent architectures, tool integration,
callback patterns, and state management strategies. Use documentation as reference source.

ADK Learner Prompt:
You are learning to build agents with ADK. Help understand basic concepts, walk through
tutorials and examples, and clarify how different ADK components work together.
"""
