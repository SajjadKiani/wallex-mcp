# wallex_mcp/mcp.py
from fastmcp import FastMCP
from wallex_mcp.config import cfg

mcp = FastMCP(
    name="Wallex-MCP-Server",
    dependencies=["httpx", "pydantic"]
)
