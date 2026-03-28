from fastmcp import FastMCP

mcp = FastMCP("Documentation and Calculator",port=8447)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.resource("doc://api")
def get_api_docs() -> str:
    return "API documentation content"

@mcp.prompt()
def code_review(code: str) -> str:
    return f"Review this code: {code}"

@mcp.tool()
def search_docs(query: str) -> str:
    return f"Results for: {query}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")