# MCP_understanding




# Sample Demo App

<img width="1035" alt="image" src="https://github.com/user-attachments/assets/69e59e25-728c-4e49-affe-372c140d5d94" />

# Sample Config File

<img width="1059" alt="image" src="https://github.com/user-attachments/assets/3edd58cc-5d3f-40cf-9c2a-fa1de9a4a98b" />


# MCP Logs Location
1. Path : /Users/welcome/Library/Logs/Claude/

```

(mcp_python_ws) welcome@jaisairams-Laptop Claude % pwd
/Users/welcome/Library/Logs/Claude
(mcp_python_ws) welcome@jaisairams-Laptop Claude % ls -ltr
total 784
-rw-r--r--  1 welcome  staff  133561 Mar 28 00:46 mcp-server-greeter.log
-rw-r--r--  1 welcome  staff   64782 Mar 28 00:46 mcp-server-weather.log
-rw-r--r--  1 welcome  staff  150576 Mar 28 00:46 mcp.log

(mcp_python_ws) welcome@jaisairams-Laptop Claude % 
(mcp_python_ws) welcome@jaisairams-Laptop Claude % tail -20f mcp-server-greeter.log
2025-03-28T04:47:13.383Z [greeter] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":123}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:13.385Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":123,"result":{"prompts":[]}}
2025-03-28T04:47:19.333Z [greeter] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":124}
[03/28/25 00:47:19] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:19.337Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":124,"result":{"resources":[]}}
2025-03-28T04:47:19.337Z [greeter] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":125}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:19.339Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":125,"result":{"prompts":[]}}
2025-03-28T04:47:24.332Z [greeter] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":126}
[03/28/25 00:47:24] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:24.336Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":126,"result":{"resources":[]}}
2025-03-28T04:47:24.336Z [greeter] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":127}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:24.338Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":127,"result":{"prompts":[]}}
2025-03-28T04:47:29.333Z [greeter] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":128}
[03/28/25 00:47:29] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:29.337Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":128,"result":{"resources":[]}}
2025-03-28T04:47:29.338Z [greeter] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":129}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:29.339Z [greeter] [info] Message from server: {"jsonrpc":"2.0","id":129,"result":{"prompts":[]}}
^Z
zsh: suspended  tail -20f mcp-server-greeter.log
(mcp_python_ws) welcome@jaisairams-Laptop Claude % tail -20f mcp-server-weather.log
2025-03-28T04:47:24.336Z [weather] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":129}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:24.338Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":129,"result":{"prompts":[]}}
2025-03-28T04:47:29.334Z [weather] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":130}
[03/28/25 00:47:29] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:29.337Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":130,"result":{"resources":[]}}
2025-03-28T04:47:29.338Z [weather] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":131}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:29.339Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":131,"result":{"prompts":[]}}
2025-03-28T04:47:34.335Z [weather] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":132}
[03/28/25 00:47:34] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:34.340Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":132,"result":{"resources":[]}}
2025-03-28T04:47:34.341Z [weather] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":133}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:34.343Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":133,"result":{"prompts":[]}}
2025-03-28T04:47:39.333Z [weather] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":134}
[03/28/25 00:47:39] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:39.336Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":134,"result":{"resources":[]}}
2025-03-28T04:47:39.337Z [weather] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":135}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:39.339Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":135,"result":{"prompts":[]}}
2025-03-28T04:47:44.330Z [weather] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":136}
[03/28/25 00:47:44] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:44.335Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":136,"result":{"resources":[]}}
2025-03-28T04:47:44.335Z [weather] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":137}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:44.337Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":137,"result":{"prompts":[]}}
2025-03-28T04:47:49.332Z [weather] [info] Message from client: {"method":"resources/list","params":{},"jsonrpc":"2.0","id":138}
[03/28/25 00:47:49] INFO     Processing request of type            server.py:534
                             ListResourcesRequest                               
2025-03-28T04:47:49.339Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":138,"result":{"resources":[]}}
2025-03-28T04:47:49.340Z [weather] [info] Message from client: {"method":"prompts/list","params":{},"jsonrpc":"2.0","id":139}
                    INFO     Processing request of type            server.py:534
                             ListPromptsRequest                                 
2025-03-28T04:47:49.347Z [weather] [info] Message from server: {"jsonrpc":"2.0","id":139,"result":{"prompts":[]}}



```

# References

1. https://medium.com/data-and-beyond/the-model-context-protocol-mcp-the-ultimate-guide-c40539e2a8e7
2. https://github.com/coleam00/ottomator-agents/blob/main/nba-agent/nba_agent.py
3. https://www.youtube.com/watch?v=v_6EXt6T83I
4. https://modelcontextprotocol.io/introduction
5. https://github.com/coleam00/ottomator-agents/tree/main/pydantic-ai-mcp-agent

# Example References
1. https://www.dremio.com/blog/building-a-basic-mcp-server-with-python/
2. https://github.com/HeetVekariya/Linear-Regression-MCP
3. https://github.com/singlestore-labs/mcp-server-singlestore
