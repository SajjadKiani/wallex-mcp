# wallex_mcp/server.py
from wallex_mcp.mcp import mcp
import wallex_mcp.tools.order      # noqa: F401
import wallex_mcp.tools.markets      # noqa: F401
import wallex_mcp.tools.balance      # noqa: F401
from wallex_mcp.config import cfg

@mcp.tool(name="health")   # same behaviour, simpler decorator
async def health() -> str:
    """Return OK if the server is alive."""
    return "ok"

if __name__ == "__main__":
    mcp.run()
