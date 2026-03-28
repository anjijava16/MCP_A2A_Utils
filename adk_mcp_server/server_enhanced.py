"""
🚀 Enhanced ADK Documentation & Dev Skills MCP Server
Integrates official Google ADK documentation with development skills
Provides comprehensive tools for ADK learning, development, and deployment
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

mcp = FastMCP("ADK-Pro 🚀")  # Enhanced ProThe cache for all documentation sources
_doc_cache = {
    "llms_txt": None,           # llms.txt - documentation index
    "llms_full": None,          # llms-full.txt - complete documentation
    "dev_skills": None,         # Dev skills metadata
    "last_updated": None,
    "sections": {},
    "skills_info": {}
}

# Dev Skills metadata (official ADK skills)
ADK_DEV_SKILLS = {
    "adk-cheatsheet": {
        "name": "adk-cheatsheet",
        "description": "Python API quick reference and documentation index",
        "category": "Reference",
        "url": "https://github.com/google/adk/tree/main/skills/adk-cheatsheet"
    },
    "adk-deploy-guide": {
        "name": "adk-deploy-guide",
        "description": "Agent Engine and Cloud Run deployment guide",
        "category": "Deployment",
        "url": "https://github.com/google/adk/tree/main/skills/adk-deploy-guide"
    },
    "adk-dev-guide": {
        "name": "adk-dev-guide",
        "description": "Development lifecycle and coding guidelines",
        "category": "Development",
        "url": "https://github.com/google/adk/tree/main/skills/adk-dev-guide"
    },
    "adk-eval-guide": {
        "name": "adk-eval-guide",
        "description": "Evaluation methodology and scoring framework",
        "category": "Evaluation",
        "url": "https://github.com/google/adk/tree/main/skills/adk-eval-guide"
    },
    "adk-observability-guide": {
        "name": "adk-observability-guide",
        "description": "Tracing, logging, and integration monitoring",
        "category": "Operations",
        "url": "https://github.com/google/adk/tree/main/skills/adk-observability-guide"
    },
    "adk-scaffold": {
        "name": "adk-scaffold",
        "description": "Project scaffolding and initialization",
        "category": "Setup",
        "url": "https://github.com/google/adk/tree/main/skills/adk-scaffold"
    }
}

# ==================== DOCUMENTATION FETCHING ====================

async def fetch_adk_llms_txt() -> str:
    """Fetch ADK documentation index (llms.txt)"""
    try:
        url = "https://google.github.io/adk-docs/llms.txt"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            logger.info(f"✅ ADK llms.txt fetched ({len(response.text)} chars)")
            return response.text
    except Exception as e:
        logger.error(f"❌ Error fetching llms.txt: {str(e)}")
        return None

async def fetch_adk_llms_full() -> str:
    """Fetch complete ADK documentation (llms-full.txt)"""
    try:
        url = "https://google.github.io/adk-docs/llms-full.txt"
        async with httpx.AsyncClient(timeout=60.0) as client:  # Longer timeout for large file
            response = await client.get(url)
            response.raise_for_status()
            logger.info(f"✅ ADK llms-full.txt fetched ({len(response.text)} chars)")
            return response.text
    except Exception as e:
        logger.error(f"❌ Error fetching llms-full.txt: {str(e)}")
        return None

async def ensure_docs_loaded():
    """Load all documentation sources into cache"""
    if _doc_cache["llms_txt"] is None or _doc_cache["llms_full"] is None:
        try:
            logger.info("📚 Loading ADK documentation from official sources...")
            
            # Fetch both documentation sources in parallel
            llms_txt_task = fetch_adk_llms_txt()
            llms_full_task = fetch_adk_llms_full()
            
            llms_txt, llms_full = await asyncio.gather(llms_txt_task, llms_full_task)
            
            if llms_txt:
                _doc_cache["llms_txt"] = llms_txt
            if llms_full:
                _doc_cache["llms_full"] = llms_full
            
            _doc_cache["last_updated"] = datetime.now().isoformat()
            _parse_sections()
            _populate_skills_info()
            
            logger.info("✅ All documentation loaded and indexed")
        except Exception as e:
            logger.error(f"❌ Failed to load documentation: {str(e)}")
            raise

def _parse_sections():
    """Parse documentation into searchable sections"""
    # Use full documentation for better section parsing
    content = _doc_cache["llms_full"] or _doc_cache["llms_txt"] or ""
    
    # Split by markdown headers
    sections = re.split(r'^(#{1,4}\s+.*?)$', content, flags=re.MULTILINE)
    
    current_section = "Overview"
    for i, section in enumerate(sections):
        if section.startswith('#'):
            current_section = section.strip('#').strip()
        else:
            if current_section not in _doc_cache["sections"]:
                _doc_cache["sections"][current_section] = []
            _doc_cache["sections"][current_section].append(section)

def _populate_skills_info():
    """Populate dev skills information"""
    _doc_cache["skills_info"] = ADK_DEV_SKILLS
    logger.info(f"✅ Loaded {len(ADK_DEV_SKILLS)} dev skills")

# ==================== CORE DOCUMENTATION TOOLS ====================

@mcp.tool()
async def search_all_documentation(query: str, max_results: int = 10, search_full: bool = True) -> dict:
    """🔍 Unified search across all ADK documentation and resources"""
    try:
        await ensure_docs_loaded()
        
        # Search in full documentation first (more comprehensive)
        search_content = (_doc_cache["llms_full"] or _doc_cache["llms_txt"] or "").lower()
        query_lower = query.lower()
        
        if not search_content:
            return {"success": False, "error": "No documentation available"}
        
        matches = []
        lines = search_content.split('\n')
        
        for i, line in enumerate(lines):
            if query_lower in line:
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                context = '\n'.join(lines[start:end])
                
                matches.append({
                    "line_num": i + 1,
                    "matched_line": line.strip()[:100],
                    "context": context[:300]
                })
        
        matches = matches[:max_results]
        logger.info(f"✅ Found {len(matches)} matches for '{query}'")
        
        return {
            "success": True,
            "query": query,
            "matches": matches,
            "total_matches": len(matches),
            "search_scope": "Full Documentation" if search_full else "Index"
        }
    except Exception as e:
        logger.error(f"❌ Error searching documentation: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_adk_documentation_overview() -> dict:
    """📖 Get comprehensive ADK documentation overview"""
    try:
        await ensure_docs_loaded()
        
        llms_txt = _doc_cache["llms_txt"] or ""
        llms_full = _doc_cache["llms_full"] or ""
        
        # Extract first section as overview
        overview = (llms_txt[:1500] or llms_full[:1500]).strip()
        
        return {
            "success": True,
            "overview": overview,
            "full_docs_available": len(llms_full) > 0,
            "index_docs_available": len(llms_txt) > 0,
            "full_size_chars": len(llms_full),
            "index_size_chars": len(llms_txt),
            "last_updated": _doc_cache["last_updated"]
        }
    except Exception as e:
        logger.error(f"❌ Error getting overview: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def browse_documentation_structure() -> dict:
    """📋 Browse the structure of ADK documentation"""
    try:
        await ensure_docs_loaded()
        
        sections = list(_doc_cache["sections"].keys())[:30]  # Top 30 sections
        
        return {
            "success": True,
            "sections": sections,
            "total_sections": len(_doc_cache["sections"]),
            "tip": "Use get_documentation_section() to retrieve detailed content"
        }
    except Exception as e:
        logger.error(f"❌ Error browsing structure: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_documentation_section(section_name: str) -> dict:
    """📄 Retrieve a complete documentation section"""
    try:
        await ensure_docs_loaded()
        
        # Try exact match first
        if section_name in _doc_cache["sections"]:
            content = '\n'.join(_doc_cache["sections"][section_name])
        else:
            # Try fuzzy match
            matches = [s for s in _doc_cache["sections"].keys() 
                      if section_name.lower() in s.lower()]
            if matches:
                section_name = matches[0]
                content = '\n'.join(_doc_cache["sections"][section_name])
            else:
                return {
                    "success": False,
                    "error": f"Section '{section_name}' not found",
                    "tip": "Use browse_documentation_structure() to see available sections"
                }
        
        return {
            "success": True,
            "section": section_name,
            "content": content,
            "length_chars": len(content),
            "lines": len(content.split('\n'))
        }
    except Exception as e:
        logger.error(f"❌ Error getting section: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DEV SKILLS TOOLS ====================

@mcp.tool()
async def list_adk_dev_skills() -> dict:
    """🛠️ List all official ADK development skills"""
    try:
        await ensure_docs_loaded()
        
        skills = [
            {
                "name": skill["name"],
                "description": skill["description"],
                "category": skill["category"]
            }
            for skill in ADK_DEV_SKILLS.values()
        ]
        
        # Group by category
        categories = {}
        for skill in skills:
            cat = skill["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(skill["name"])
        
        logger.info(f"✅ Listed {len(skills)} ADK dev skills")
        
        return {
            "success": True,
            "skills": skills,
            "by_category": categories,
            "total_skills": len(skills),
            "tip": "Use get_skill_details() to learn more about a specific skill"
        }
    except Exception as e:
        logger.error(f"❌ Error listing skills: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_skill_details(skill_name: str) -> dict:
    """📚 Get detailed information about an ADK development skill"""
    try:
        await ensure_docs_loaded()
        
        if skill_name not in ADK_DEV_SKILLS:
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not found",
                "available_skills": list(ADK_DEV_SKILLS.keys())
            }
        
        skill = ADK_DEV_SKILLS[skill_name]
        
        return {
            "success": True,
            "skill": skill,
            "installation_command": f"npx skills add google/adk-docs/skills/{skill_name} -y -g",
            "github_url": skill["url"]
        }
    except Exception as e:
        logger.error(f"❌ Error getting skill details: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_skill_by_category(category: str) -> dict:
    """🏗️ Get all ADK skills in a specific category"""
    try:
        await ensure_docs_loaded()
        
        category_skills = [
            skill for skill in ADK_DEV_SKILLS.values()
            if skill["category"].lower() == category.lower()
        ]
        
        if not category_skills:
            available_categories = set(
                skill["category"] for skill in ADK_DEV_SKILLS.values()
            )
            return {
                "success": False,
                "error": f"Category '{category}' not found",
                "available_categories": list(available_categories)
            }
        
        return {
            "success": True,
            "category": category,
            "skills": category_skills,
            "count": len(category_skills)
        }
    except Exception as e:
        logger.error(f"❌ Error getting skills by category: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== API & REFERENCE TOOLS ====================

@mcp.tool()
async def search_adk_api_reference(api_pattern: str) -> dict:
    """🔌 Search for ADK API references and class definitions"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["llms_full"] or _doc_cache["llms_txt"] or ""
        
        # Look for common API patterns
        patterns = [
            f'`{api_pattern}`',
            f'class {api_pattern}',
            f'def {api_pattern}',
            f'## {api_pattern}',
            f'### {api_pattern}',
            f'**{api_pattern}**'
        ]
        
        matches = {}
        for pattern in patterns:
            count = content.count(pattern)
            if count > 0:
                matches[pattern] = count
        
        if not matches:
            return {
                "success": False,
                "message": f"No API reference found for '{api_pattern}'",
                "tip": "Try searching with search_all_documentation()"
            }
        
        logger.info(f"✅ Found API reference patterns for {api_pattern}")
        
        return {
            "success": True,
            "api_pattern": api_pattern,
            "patterns_found": matches
        }
    except Exception as e:
        logger.error(f"❌ Error searching API: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def extract_code_examples(language: str = "python", max_examples: int = 10) -> dict:
    """💻 Extract code examples from documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["llms_full"] or _doc_cache["llms_txt"] or ""
        
        # Extract code blocks for specified language
        pattern = f'```{language}\n(.*?)\n```'
        code_blocks = re.findall(pattern, content, re.DOTALL)
        
        if not code_blocks:
            # Try generic code blocks
            pattern = r'```\n(.*?)\n```'
            code_blocks = re.findall(pattern, content, re.DOTALL)
        
        code_blocks = code_blocks[:max_examples]
        
        logger.info(f"✅ Found {len(code_blocks)} code examples")
        
        return {
            "success": True,
            "language": language,
            "code_examples": code_blocks,
            "count": len(code_blocks)
        }
    except Exception as e:
        logger.error(f"❌ Error extracting code: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== UTILITY TOOLS ====================

@mcp.tool()
async def get_documentation_statistics() -> dict:
    """📊 Get comprehensive documentation statistics"""
    try:
        await ensure_docs_loaded()
        
        llms_txt = _doc_cache["llms_txt"] or ""
        llms_full = _doc_cache["llms_full"] or ""
        
        stats = {
            "index_docs": {
                "characters": len(llms_txt),
                "lines": len(llms_txt.split('\n')),
                "code_blocks": llms_txt.count('```') // 2
            },
            "full_docs": {
                "characters": len(llms_full),
                "lines": len(llms_full.split('\n')),
                "code_blocks": llms_full.count('```') // 2
            },
            "sections_indexed": len(_doc_cache["sections"]),
            "dev_skills_available": len(ADK_DEV_SKILLS),
            "last_updated": _doc_cache["last_updated"]
        }
        
        logger.info("✅ Retrieved documentation statistics")
        
        return {
            "success": True,
            "statistics": stats,
            "total_docs_size_mb": round((len(llms_txt) + len(llms_full)) / 1024 / 1024, 2)
        }
    except Exception as e:
        logger.error(f"❌ Error getting statistics: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def reload_documentation_from_source() -> dict:
    """🔄 Reload all documentation from official sources"""
    try:
        logger.info("🔄 Reloading documentation from official sources...")
        
        # Clear cache
        _doc_cache["llms_txt"] = None
        _doc_cache["llms_full"] = None
        _doc_cache["sections"] = {}
        _doc_cache["last_updated"] = None
        
        # Reload
        await ensure_docs_loaded()
        
        logger.info("✅ Documentation reloaded successfully")
        
        return {
            "success": True,
            "message": "Documentation reloaded from official Google ADK sources",
            "last_updated": _doc_cache["last_updated"],
            "docs_size": {
                "index_chars": len(_doc_cache["llms_txt"] or ""),
                "full_chars": len(_doc_cache["llms_full"] or "")
            }
        }
    except Exception as e:
        logger.error(f"❌ Error reloading documentation: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== INSTALLATION & SETUP TOOLS ====================

@mcp.tool()
async def get_skill_installation_guide(tool_name: str = "all") -> dict:
    """⚙️ Get installation guide for ADK development skills"""
    try:
        if tool_name == "all":
            guides = {
                skill_name: f"npx skills add google/adk-docs/skills/{skill_name} -y -g"
                for skill_name in ADK_DEV_SKILLS.keys()
            }
            
            return {
                "success": True,
                "message": "ADK Dev Skills Installation Guide",
                "install_all": "npx skills add google/adk-docs/skills -y -g",
                "install_individual": guides,
                "requires": "Node.js and npx"
            }
        else:
            if tool_name not in ADK_DEV_SKILLS:
                return {
                    "success": False,
                    "error": f"Skill '{tool_name}' not found",
                    "available": list(ADK_DEV_SKILLS.keys())
                }
            
            return {
                "success": True,
                "skill": tool_name,
                "installation_command": f"npx skills add google/adk-docs/skills/{tool_name} -y -g",
                "github_source": ADK_DEV_SKILLS[tool_name]["url"],
                "description": ADK_DEV_SKILLS[tool_name]["description"]
            }
    except Exception as e:
        logger.error(f"❌ Error getting installation guide: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_mcp_integration_guide(tool_type: str = "claude") -> dict:
    """🔗 Get guide for integrating ADK MCP server with various tools"""
    try:
        integration_guides = {
            "claude": {
                "name": "Claude Code",
                "command": "claude mcp add adk-docs --transport stdio -- uvx --from mcpdoc mcpdoc --urls AgentDevelopmentKit:https://google.github.io/adk-docs/llms.txt --transport stdio",
                "description": "Add official ADK Docs MCP to Claude Code"
            },
            "cursor": {
                "name": "Cursor",
                "instruction": "Open Cursor Settings > Tools & MCP > New MCP Server > edit mcp.json with provided config",
                "config": {
                    "mcpServers": {
                        "adk-docs-mcp": {
                            "command": "uvx",
                            "args": ["--from", "mcpdoc", "mcpdoc", "--urls",
                                   "AgentDevelopmentKit:https://google.github.io/adk-docs/llms.txt",
                                   "--transport", "stdio"]
                        }
                    }
                }
            },
            "gemini": {
                "name": "Gemini CLI",
                "command": "gemini extensions install https://github.com/derailed-dash/adk-docs-ext",
                "description": "Install ADK Docs Extension for Gemini CLI"
            },
            "antigravity": {
                "name": "Antigravity",
                "instruction": "Open MCP Store > Manage MCP Servers > View raw config > add to mcp_config.json",
                "requires": "uv package manager"
            },
            "custom-python": {
                "name": "Custom Python MCP (This Server)",
                "description": "Use this enhanced Python FastMCP server directly",
                "command": "python adk_mcp_server/server_enhanced.py",
                "port": 7099,
                "features": ["Official llms.txt & llms-full.txt", "Dev Skills access", "Unified search"]
            }
        }
        
        if tool_type not in integration_guides:
            return {
                "success": True,
                "message": "Available integration guides",
                "tools": list(integration_guides.keys()),
                "tip": f"Use get_mcp_integration_guide('{integration_guides[list(integration_guides.keys())[0]]}') for details"
            }
        
        return {
            "success": True,
            "tool": tool_type,
            "guide": integration_guides[tool_type]
        }
    except Exception as e:
        logger.error(f"❌ Error getting integration guide: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Enhanced ADK Documentation MCP Server"""
    try:
        logger.info("🚀 Starting Enhanced ADK Documentation MCP Server on port 7099")
        logger.info("📚 This server provides:")
        logger.info("   • Official ADK documentation (llms.txt + llms-full.txt)")
        logger.info("   • 6 ADK Development Skills")
        logger.info("   • 12 comprehensive tools")
        logger.info("   • Unified search and reference")
        
        # Pre-load docs on startup
        await ensure_docs_loaded()
        
        logger.info("✅ Server ready! Starting to listen...")
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
# ADK Developer Prompt
You are an expert ADK (Agent Development Kit) developer with deep knowledge of:
- ADK APIs and patterns
- Python agent development
- FastMCP implementation
- Official ADK documentation

Use tools to:
1. Search documentation for specific patterns
2. Find relevant dev skills for the task
3. Extract code examples
4. Provide best practices

When users ask about ADK:
- Search documentation first for official guidance
- Recommend relevant dev skills
- Provide code examples from official docs
- Link to documented API references

# ADK Architect Prompt
You are an ADK systems architect designing scalable agent systems.

Use tools to:
1. Browse documentation structure for design patterns
2. Get skill details for architecture decisions
3. Find integration guidance
4. Understand deployment patterns

When designing systems:
- Understand deployment constraints (adk-deploy-guide)
- Plan evaluation strategy (adk-eval-guide)
- Design observability (adk-observability-guide)
- Consider scaffolding options (adk-scaffold)

# ADK Learner Prompt
You are learning Agent Development Kit and want to understand core concepts.

Use tools to:
1. Get documentation overview to understand basics
2. Extract and review code examples
3. Browse documentation structure to learn progressively
4. Find related topics for deeper learning

Learning path:
1. Start with get_adk_documentation_overview()
2. Browse structure with browse_documentation_structure()
3. Study sections with get_documentation_section()
4. Extract examples with extract_code_examples()
5. Install dev skills for interactive learning
"""
