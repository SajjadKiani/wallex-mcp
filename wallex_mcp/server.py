'''Entry point for Wallex MCP Server. Initializes FastMCP, registers tools/resources, and starts the server.'''
import os
from fastmcp import FastMCP
from wallex_mcp.config import cfg

# Import modules to register tools and resources via decorators
import wallex_mcp.tools.get_balance  # noqa: F401
import wallex_mcp.tools.place_order  # noqa: F401
import wallex_mcp.tools.cancel_order  # noqa: F401
import wallex_mcp.resources.resource_handlers  # noqa: F401

# Instantiate the MCP server
mcp = FastMCP(
    name="Wallex MCP Server",
    description="MCP server exposing Wallex API tools and resources",
    version="0.1.0",
)

# Optional health-check endpoint
@mcp.app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": cfg.current_timestamp()}

if __name__ == "__main__":
    # Run the server (uses Uvicorn under the hood)
    mcp.run(host=cfg.HOST, port=cfg.PORT)
