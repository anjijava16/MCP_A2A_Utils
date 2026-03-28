# 🔗 ADK MCP Server Integration Guide

Complete guide for integrating Enhanced ADK Documentation MCP Server with various tools and workflows.

---

## 📊 Integration Matrix

| Tool | Method | Complexity | Status |
|------|--------|-----------|--------|
| **Claude Code** | CLI command | ⭐ Simple | ✅ Supported |
| **Cursor** | Config file | ⭐ Simple | ✅ Supported |
| **Gemini CLI** | Extension install | ⭐ Simple | ✅ Supported |
| **Antigravity** | MCP Store | ⭐⭐ Moderate | ✅ Supported |
| **VS Code** | MCP config | ⭐⭐ Moderate | ✅ Supported |
| **PyCharm** | Custom tools | ⭐⭐⭐ Advanced | ✅ Supported |
| **Neovim** | LSP integration | ⭐⭐⭐ Advanced | ✅ Supported |
| **Custom Agent** | Direct connection | ⭐ Simple | ✅ Supported |

---

## 🎯 Integration Options

### Option 1: Official ADK MCP Server (Recommended for Beginners)

**Best For**: Quickest setup, official Google solution

**Setup**:
```bash
# Claude Code
claude mcp add adk-docs --transport stdio -- uvx --from mcpdoc mcpdoc --urls AgentDevelopmentKit:https://google.github.io/adk-docs/llms.txt --transport stdio
```

**Pros**:
- ✅ Official, maintained by Google
- ✅ Works out of the box
- ✅ No installation needed

**Cons**:
- ⚠️ Limited to text output
- ⚠️ No dev skills integration
- ⚠️ Manual parsing required

---

### Option 2: Enhanced Python MCP Server (Recommended for Advanced Users)

**Best For**: Full power, all 12 tools, dev skills integration

**Setup**:
```bash
# 1. Navigate to workspace
cd /path/to/MCP_servers_and_a2a_utils

# 2. Install dependencies
pip install fastmcp>=1.0.0 httpx>=0.24.0

# 3. Run server
python adk_mcp_server/server_enhanced.py
```

**Configuration for Claude Desktop**:
```json
{
  "mcpServers": {
    "adk-docs-enhanced": {
      "command": "python",
      "args": ["/absolute/path/to/adk_mcp_server/server_enhanced.py"]
    }
  }
}
```

**Pros**:
- ✅ Full 12 tools available
- ✅ Dev skills access (6 skills)
- ✅ Unified search (llms.txt + llms-full)
- ✅ Code example extraction
- ✅ MCP integration guides
- ✅ Category-based browsing
- ✅ Can run locally offline (with reload)

**Cons**:
- ⚠️ Requires Python 3.9+
- ⚠️ Manual configuration needed
- ⚠️ Local server management

---

### Option 3: Hybrid Approach (Recommended for Production)

**Best For**: Leverage both official and enhanced capabilities

**Setup**:
```json
{
  "mcpServers": {
    "adk-docs-official": {
      "command": "uvx",
      "args": [
        "--from", "mcpdoc",
        "mcpdoc",
        "--urls", "AgentDevelopmentKit:https://google.github.io/adk-docs/llms.txt",
        "--transport", "stdio"
      ]
    },
    "adk-docs-enhanced": {
      "command": "python",
      "args": ["/path/to/adk_mcp_server/server_enhanced.py"]
    }
  }
}
```

**Benefits**:
- ✅ Official docs + enhanced tools
- ✅ Fallback redundancy
- ✅ Choice of access patterns
- ✅ Comparison reference

---

## 🚀 Tool-Specific Setup

### Claude Code

**Quick Setup**:
```bash
claude mcp add adk-docs-enhanced --transport stdio -- python /path/to/adk_mcp_server/server_enhanced.py
```

**Manual Config (`~/.claude/config/claude_desktop_config.json`)**:
```json
{
  "mcpServers": {
    "adk-docs-enhanced": {
      "command": "python",
      "args": ["/Users/welcome/Library/Mobile Documents/com~apple~CloudDocs/Tech_Learn/Tech_Repos/python_envs/mcp_utils/MCP_servers_and_a2a_utils/adk_mcp_server/server_enhanced.py"]
    }
  }
}
```

**Usage in Claude**:
```
You: "Show me how to create an ADK agent"
→ Claude uses search_all_documentation()
→ Returns relevant sections + code examples

You: "What's the adk-deploy-guide skill?"
→ Claude uses get_skill_details("adk-deploy-guide")
→ Returns installation command + GitHub URL

You: "Find Python code examples"
→ Claude uses extract_code_examples("python")
→ Returns runnable code snippets
```

### Cursor

**Setup Steps**:
1. Open Cursor Settings (Cmd+,)
2. Navigate to **Tools & MCP**
3. Click **New MCP Server**
4. Edit `mcp.json`:

```json
{
  "mcpServers": {
    "adk-docs-enhanced": {
      "command": "python",
      "args": ["/path/to/adk_mcp_server/server_enhanced.py"]
    }
  }
}
```

5. Restart Cursor

**File Location**: `~/.cursor/mcp.json`

**Usage**:
- Inline documentation lookup
- Code completion with ADK patterns
- Quick ref lookup in sidebarpanel

### Gemini CLI

**Official ADK Docs Extension**:
```bash
gemini extensions install https://github.com/derailed-dash/adk-docs-ext
```

**For Enhanced Server**:
```bash
# Configure Gemini to use enhanced server
gemini config add mcp-server adk-docs-enhanced \
  --type python \
  --path /path/to/adk_mcp_server/server_enhanced.py
```

### VS Code

**Setup with VS Code AI Extensions**:

1. Install [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) or similar
2. Setup MCP in VS Code settings:

```json
{
  "mcp.servers": {
    "adk-docs": {
      "command": "python",
      "args": ["/path/to/adk_mcp_server/server_enhanced.py"]
    }
  }
}
```

3. Configure in `.vscode/settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "mcp.enabled": true,
  "mcp.servers": {
    "adk-docs-enhanced": {
      "command": "python",
      "args": ["/path/to/adk_mcp_server/server_enhanced.py"],
      "transport": "sse",
      "port": 7099
    }
  }
}
```

---

## 🔧 Advanced Integration Patterns

### Pattern 1: Eclipse with AI-Assisted Development

```bash
# Setup Eclipse Language Server Protocol
# Configure MCP bridge for ADK documentation
# Tools: Lemminx + MCP connector
```

### Pattern 2: PyCharm with ADK Tools

**Install Plugin**:
1. PyCharm → Preferences → Plugins
2. Search "MCP" or "Model Context Protocol"
3. Install MCP plugin

**Configure**:
```python
# File: ~/.scripts/adk_pycharm_bridge.py
import hatchery.mcp as mcp

client = mcp.Client(
    server_url="http://localhost:7099",
    tools=[
        "search_all_documentation",
        "get_skill_details",
        "extract_code_examples"
    ]
)
```

### Pattern 3: Neovim with LSP + MCP

**Install Plugin** (using packer.nvim):
```lua
use {
  "nvim-lua/nvim-mcp",
  config = function()
    require("mcp").setup({
      servers = {
        adk_enhanced = {
          cmd = "python",
          args = {"/path/to/adk_mcp_server/server_enhanced.py"},
          port = 7099
        }
      }
    })
  end
}
```

### Pattern 4: Custom Python Agent

**Direct Integration**:
```python
import httpx
import asyncio

async def get_adk_help(query: str):
    """Query ADK MCP server directly"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:7099/mcp/tools/search_all_documentation",
            json={"query": query}
        )
        return response.json()

# Usage
result = asyncio.run(get_adk_help("agent callback"))
print(result)
```

---

## 📚 Workflow Examples

### Workflow 1: Rapid Prototyping with Claude

```
Step 1: Ask Claude about ADK
  "How do I create an agent with callbacks?"

Step 2: Claude searches documentation
  Uses: search_all_documentation("agent callback")
  
Step 3: Claude extracts examples
  Uses: extract_code_examples("python")
  
Step 4: You get answer + working code
  Claude provides: Definition + example code + best practices

Step 5: You prototype quickly
  Copy code, modify, test
```

### Workflow 2: Structured Learning Path

```
Week 1-2: Fundamentals
├── get_adk_documentation_overview()
├── browse_documentation_structure()
└── read Key sections

Week 3: Core Concepts
├── search_all_documentation("agent patterns")
├── extract_code_examples("python")
└── Study patterns

Week 4: Development
├── get_skill_details("adk-dev-guide")
├── search_all_documentation("callbacks")
└── Build project

Week 5: Deployment
├── get_skill_details("adk-deploy-guide")
├── search_all_documentation("deployment")
└── Deploy agent
```

### Workflow 3: Development with All Tools

```
IDE/Editor Setup:
├── Cursor with MCP
├── Claude Desktop
├── Terminal with local server
└── Official docs bookmark

Development Process:
1. Code in Cursor with inline ADK help
2. Ask Claude for complex questions
3. Use terminal for quick lookups
4. Cross-reference official docs
```

---

## 🔄 Docker Deployment

### Single Server

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY adk_mcp_server/ ./adk_mcp_server/
COPY docs_servers_requirements.txt .

RUN pip install -r docs_servers_requirements.txt

EXPOSE 7099

CMD ["python", "adk_mcp_server/server_enhanced.py"]
```

### Build & Run

```bash
docker build -t adk-mcp-server .
docker run -p 7099:7099 adk-mcp-server
```

### Docker Compose

```yaml
version: '3.8'

services:
  adk-docs:
    build: .
    ports:
      - "7099:7099"
    environment:
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7099/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Optional: Add other MCP servers
  mcp-protocol:
    image: mcp-protocol:latest
    ports:
      - "7100:7100"
    depends_on:
      - adk-docs
```

---

## ✅ Integration Checklist

Before Deploying:

- [ ] Python 3.9+ installed
- [ ] httpx and fastmcp installed
- [ ] Server starts without errors
- [ ] Documentation loads successfully
- [ ] All 12 tools are accessible
- [ ] MCP transport is running on port 7099
- [ ] IDE/tool is configured correctly
- [ ] Can call tools from tool
- [ ] Getting expected responses
- [ ] Error handling works

---

## 🐛 Troubleshooting Integration

### Issue: Module not found
```bash
pip install fastmcp>=1.0.0 httpx>=0.24.0
```

### Issue: Port 7099 already in use
```bash
# Find process using port
lsof -i :7099

# Kill process
kill -9 <PID>

# Or use different port in code
await mcp.run_async(host="0.0.0.0", port=7100)
```

### Issue: Documentation not loading
```bash
# Test network connectivity
curl https://google.github.io/adk-docs/llms.txt
curl https://google.github.io/adk-docs/llms-full.txt

# Check firewall settings
# Increase timeout in server_enhanced.py
```

### Issue: IDE not finding MCP server
```bash
# Verify config path is correct
# Check file permissions
chmod +x adk_mcp_server/server_enhanced.py

# Restart IDE/tool
# Check IDE logs for errors
```

### Issue: Slow performance
```bash
# Check memory usage
ps aux | grep server_enhanced.py

# Restart server to clear cache
# Reduce max_results in search calls
```

---

## 📈 Scaling for Teams

### Centralized Server Setup

```
Team Network:
┌─────────────────────────────────────┐
│  Shared MCP Server (7099)           │
│  - One instance for team            │
│  - Shared documentation cache       │
│  - Monitoring & logging             │
└─────────────────────────────────────┘
         ↑ ↑ ↑ ↑ ↑
    ┌────┴─┴─┴─┴──┐
    │  Team Tools │
┌───┴──┐ ┌──────┐ ┌──────┐
│Claude│ │Cursor│ │ IDE  │
└──────┘ └──────┘ └──────┘
```

### Load Balancing

```yaml
version: '3.8'
services:
  adk-lb:
    image: nginx:latest
    ports:
      - "7099:7099"
    depends_on:
      - adk-1
      - adk-2
      - adk-3
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

  adk-1:
    build: .
    expose:
      - "7099"
  adk-2:
    build: .
    expose:
      - "7099"
  adk-3:
    build: .
    expose:
      - "7099"
```

---

## 🎓 Integration Best Practices

1. **Start Simple**: Begin with one tool
2. **Document Setup**: Keep integration docs updated
3. **Test Thoroughly**: Verify all workflows before team use
4. **Monitor Performance**: Track response times and errors
5. **Update Regularly**: Keep server and dependencies current
6. **Backup Configs**: Version control your MCP configurations
7. **Plan Fallbacks**: Have offline alternatives
8. **Train Team**: Ensure team knows available tools
9. **Gather Feedback**: Iterate based on team needs
10. **Automate Setup**: Create scripts for team onboarding

---

**Version**: 1.0  
**Date**: March 2024  
**Status**: ✅ Complete  
**Maintained**: Actively
