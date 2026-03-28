from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient({
   # "math": {"transport": "stdio", "command": "python", "args": ["math.py"]},
    "Documentation and Calculator": {"transport": "streamable-http", "url": "http://localhost:8447/mcp"}
})

async def main():
    tools = await client.get_tools()
    print(f" tools ={tools}")
    agent = create_agent("claude-sonnet-4-5-20250929", tools)
    result = await agent.ainvoke({"messages": [{"role": "user", "content": "What's 5+3 "}]})
    print(f"Result: = {result}")
    
    print("Full Result:")
    import pprint
    pprint.pprint(result)

    
    print("Messages:")
    for msg in result["messages"]:
        print(msg)
    
    print("\n \n")
    print("stream mode test:")
    async for event in agent.astream({
        "messages": [{"role": "user", "content": "What's 5+3 and code review for 'def add(a, b): return a + b'?"}]
    }):
        print(event)




import asyncio
asyncio.run(main())