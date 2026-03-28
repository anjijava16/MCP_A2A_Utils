# server_streamable_http.py
from mcp.server.fastmcp import FastMCP

# 1. Create the server instance
mcp = FastMCP("MyStreamableServer",port=7007,host='localhost')


# 2. Add a tool (LLMs can call this)
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b


@mcp.tool()
def sub_numbers(a: int, b: int) -> int:
    """subract two numbers together."""
    return a - b


@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


# 3. Add a dynamic resource (read-only data for LLMs)
@mcp.resource("info://user/{name}")
def get_user_info(name: str) -> str:
    """Get a greeting for a specific user."""
    return f"Hello, {name}! This is data from the server."


# 4. Run with Streamable HTTP transport
if __name__ == "__main__":
    # Runs on http://localhost:8000/mcp by default
    #mcp.run_async(transport="streamable-http", host="127.0.0.1", port=7007)
    import asyncio
    asyncio.run(
        mcp.run_streamable_http_async()
        )
    

