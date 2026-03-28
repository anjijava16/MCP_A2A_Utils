curl -N -X POST http://localhost:7007/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "init-1",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "curl-client",
        "version": "0.1"
      }
    }
  }'

  event: message
data: {"jsonrpc":"2.0","id":"init-1","result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"MyStreamableServer","version":"1.25.0"}}}

(a2a-examples) welcome@jaisairams-Laptop A2A_Examples %

