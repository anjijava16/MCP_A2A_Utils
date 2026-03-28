# Start the MCP Server 

```

(a2a-examples) welcome@jaisairams-Laptop mcp_a2a_currency_example % cd mcp_server 
(a2a-examples) welcome@jaisairams-Laptop mcp_server % vi currency_mcp_server.py
(a2a-examples) welcome@jaisairams-Laptop mcp_server % 
(a2a-examples) welcome@jaisairams-Laptop mcp_server % ls -ltr
total 8
-rw-r--r--@ 1 welcome  staff  1997 Dec 21 17:20 currency_mcp_server.py
(a2a-examples) welcome@jaisairams-Laptop mcp_server % python currency_mcp_server.py 
[INFO]: 🚀 MCP server started on port 8080


                                            ╭──────────────────────────────────────────────────────────────────────────────╮                                            
                                            │                                                                              │                                            
                                            │                         ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█                        │                                            
                                            │                         █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀                        │                                            
                                            │                                                                              │                                            
                                            │                                FastMCP 2.14.1                                │                                            
                                            │                                                                              │                                            
                                            │                                                                              │                                            
                                            │                   🖥  Server name: Currency MCP Server 💵                     │                                            
                                            │                                                                              │                                            
                                            │                   📦 Transport:   SSE                                        │                                            
                                            │                   🔗 Server URL:  http://0.0.0.0:7080/sse                    │                                            
                                            │                                                                              │                                            
                                            │                   📚 Docs:        https://gofastmcp.com                      │                                            
                                            │                   🚀 Hosting:     https://fastmcp.cloud                      │                                            
                                            │                                                                              │                                            
                                            ╰──────────────────────────────────────────────────────────────────────────────╯                                            


[12/21/25 17:21:45] INFO     Starting MCP server 'Currency MCP Server 💵' with transport 'sse' on http://0.0.0.0:7080/sse                                 server.py:2618
INFO:     Started server process [13625]
INFO:     Waiting for application startup.
[INFO]: Starting worker 'jaisairams-Laptop.local#13625' with the following tasks:
[INFO]: * trace(message: str, ...)
[INFO]: * fail(message: str, ...)
[INFO]: * sleep(seconds: float, ...)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7080 (Press CTRL+C to quit)
INFO:     127.0.0.1:58948 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:58966 - "GET /sse HTTP/1.1" 200 OK


```


# Start th A2A Server 

```
(a2a-examples) welcome@jaisairams-Laptop agent % python3 currency_agent.py
/Users/welcome/Desktop/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/.venv/lib/python3.13/site-packages/google/cloud/aiplatform/models.py:52: FutureWarning: Support for google-cloud-storage < 3.0.0 will be removed in a future version of google-cloud-aiplatform. Please upgrade to google-cloud-storage >= 3.0.0.
  from google.cloud.aiplatform.utils import gcs_utils
[INFO]: --- 🔧 Loading MCP tools from MCP Server... ---
[INFO]: --- 🤖 Creating ADK Currency Agent... ---
/Users/welcome/Desktop/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/mcp_a2a_currency_example/agent/currency_agent.py:29: DeprecationWarning: MCPToolset class is deprecated, use `McpToolset` instead.
  MCPToolset(
/Users/welcome/Desktop/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/mcp_a2a_currency_example/agent/currency_agent.py:38: UserWarning: [EXPERIMENTAL] to_a2a: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  a2a_app = to_a2a(root_agent, port=10030)
/Users/welcome/Desktop/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/.venv/lib/python3.13/site-packages/google/adk/a2a/utils/agent_to_a2a.py:88: UserWarning: [EXPERIMENTAL] A2aAgentExecutor: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  agent_executor = A2aAgentExecutor(
/Users/welcome/Desktop/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/.venv/lib/python3.13/site-packages/google/adk/a2a/utils/agent_to_a2a.py:98: UserWarning: [EXPERIMENTAL] AgentCardBuilder: ADK Implementation for A2A support (A2aAgentExecutor, RemoteA2aAgent and corresponding supporting components etc.) is in experimental mode and is subjected to breaking changes. A2A protocol and SDK arethemselves not experimental. Once it's stable enough the experimental mode will be removed. Your feedback is welcome.
  card_builder = AgentCardBuilder(
--- 🚀 Starting Currency Agent A2A server on port 10030... ---
(a2a-examples) welcome@jaisairams-Laptop agent % 

```


# Start the A2A Server Client Code

```

(a2a-examples) welcome@jaisairams-Laptop agent % python test_client.py 
--- 🔄 Connecting to agent at http://localhost:10030... ---
/Users/welcome/Desktop/Tech_Repos/python_envs/A2A/A2A_event_agents/A2A_Examples/mcp_a2a_currency_example/agent/test_client.py:134: DeprecationWarning: A2AClient is deprecated and will be removed in a future version. Use ClientFactory to create a client with a JSON-RPC transport.
  client = A2AClient(
--- ✅ Connection successful. ---
--- ✉️  Single Turn Request ---
--- 📥 Single Turn Request Response ---
{"id":"eae55811-b38a-4a77-b0d1-99c4f26fe147","jsonrpc":"2.0","result":{"artifacts":[{"artifactId":"778cca97-c4ef-442e-8dd6-336ac975a1e0","name":"conversion_result","parts":[{"kind":"text","text":"As of the latest available data, the exchange rate is 1 USD = 1.3794 CAD. Therefore, 100 USD is equivalent to approximately 137.94 CAD."}]}],"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","history":[{"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","kind":"message","messageId":"b9b988f38fc74db9a2f9b27b9ef494d4","parts":[{"kind":"text","text":"how much is 100 USD in CAD?"}],"role":"user","taskId":"61c41354-9b3c-476f-a53e-ba143fd16209"},{"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","kind":"message","messageId":"de86b232-562d-4bcf-8c52-93095a10b8bf","parts":[{"kind":"text","text":"Looking up the exchange rates..."}],"role":"agent","taskId":"61c41354-9b3c-476f-a53e-ba143fd16209"},{"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","kind":"message","messageId":"3e7dc11b-38b5-40c7-ad0e-3012feb4ef2e","parts":[{"kind":"text","text":"Processing the exchange rates.."}],"role":"agent","taskId":"61c41354-9b3c-476f-a53e-ba143fd16209"}],"id":"61c41354-9b3c-476f-a53e-ba143fd16209","kind":"task","status":{"state":"completed","timestamp":"2025-12-21T22:33:21.914071+00:00"}}}

--- ❔ Query Task ---
--- 📥 Query Task Response ---
{"id":"bb31b9b5-960a-477b-8356-dd8bc41e2029","jsonrpc":"2.0","result":{"artifacts":[{"artifactId":"778cca97-c4ef-442e-8dd6-336ac975a1e0","name":"conversion_result","parts":[{"kind":"text","text":"As of the latest available data, the exchange rate is 1 USD = 1.3794 CAD. Therefore, 100 USD is equivalent to approximately 137.94 CAD."}]}],"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","history":[{"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","kind":"message","messageId":"b9b988f38fc74db9a2f9b27b9ef494d4","parts":[{"kind":"text","text":"how much is 100 USD in CAD?"}],"role":"user","taskId":"61c41354-9b3c-476f-a53e-ba143fd16209"},{"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","kind":"message","messageId":"de86b232-562d-4bcf-8c52-93095a10b8bf","parts":[{"kind":"text","text":"Looking up the exchange rates..."}],"role":"agent","taskId":"61c41354-9b3c-476f-a53e-ba143fd16209"},{"contextId":"42f23813-6801-4a36-b0c9-011f078a1124","kind":"message","messageId":"3e7dc11b-38b5-40c7-ad0e-3012feb4ef2e","parts":[{"kind":"text","text":"Processing the exchange rates.."}],"role":"agent","taskId":"61c41354-9b3c-476f-a53e-ba143fd16209"}],"id":"61c41354-9b3c-476f-a53e-ba143fd16209","kind":"task","status":{"state":"completed","timestamp":"2025-12-21T22:33:21.914071+00:00"}}}

--- 📝 Multi-Turn Request ---
--- 📥 Multi-Turn: First Turn Response ---
{"id":"946ae853-8df1-4d6d-863b-8b355030a8dc","jsonrpc":"2.0","result":{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","history":[{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"9407aa4e528749ba9e6af7d9faccfe04","parts":[{"kind":"text","text":"how much is 100 USD?"}],"role":"user","taskId":"bab51155-482b-4968-8533-befd260a62ff"}],"id":"bab51155-482b-4968-8533-befd260a62ff","kind":"task","status":{"message":{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"38b8f720-bc6b-4074-8a9e-744caaad0cde","parts":[{"kind":"text","text":"To provide you with the current exchange rate for 100 USD in another currency, please specify the currency you wish to convert to (e.g., EUR, GBP, JPY)."}],"role":"agent","taskId":"bab51155-482b-4968-8533-befd260a62ff"},"state":"input-required","timestamp":"2025-12-21T22:33:24.366992+00:00"}}}

--- 📝 Multi-Turn: Second Turn (Input Required) ---
--- Multi-Turn: Second Turn Response ---
{"id":"979b8dd5-c4b7-4174-8eb0-76487a67430b","jsonrpc":"2.0","result":{"artifacts":[{"artifactId":"96bbb832-37df-431b-9642-a56dadfa9f6e","name":"conversion_result","parts":[{"kind":"text","text":"The current exchange rate for 1 USD to GBP is approximately 0.74795. Therefore, 100 USD is equivalent to approximately 74.80 GBP."}]}],"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","history":[{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"9407aa4e528749ba9e6af7d9faccfe04","parts":[{"kind":"text","text":"how much is 100 USD?"}],"role":"user","taskId":"bab51155-482b-4968-8533-befd260a62ff"},{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"38b8f720-bc6b-4074-8a9e-744caaad0cde","parts":[{"kind":"text","text":"To provide you with the current exchange rate for 100 USD in another currency, please specify the currency you wish to convert to (e.g., EUR, GBP, JPY)."}],"role":"agent","taskId":"bab51155-482b-4968-8533-befd260a62ff"},{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"ab9c400a392c40c0994058831b94fa23","parts":[{"kind":"text","text":"in GBP"}],"role":"user","taskId":"bab51155-482b-4968-8533-befd260a62ff"},{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"7983bda1-e6f2-45aa-86b6-40ce71bfd275","parts":[{"kind":"text","text":"Looking up the exchange rates..."}],"role":"agent","taskId":"bab51155-482b-4968-8533-befd260a62ff"},{"contextId":"9a8198bd-d7c4-48cf-a073-3bca0f61cd43","kind":"message","messageId":"b63eac57-f973-442a-a2ee-c19c6c67b29f","parts":[{"kind":"text","text":"Processing the exchange rates.."}],"role":"agent","taskId":"bab51155-482b-4968-8533-befd260a62ff"}],"id":"bab51155-482b-4968-8533-befd260a62ff","kind":"task","status":{"state":"completed","timestamp":"2025-12-21T22:33:26.726375+00:00"}}}

(a2a-examples) welcome@jaisairams-Laptop agent % 

```
