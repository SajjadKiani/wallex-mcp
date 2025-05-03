# wallex_mcp/server.py
from wallex_mcp.mcp import mcp
import wallex_mcp.tools.get_balance      # noqa: F401
import wallex_mcp.tools.place_order      # noqa: F401
import wallex_mcp.tools.cancel_order     # noqa: F401
import wallex_mcp.resources.resource_handlers  # noqa: F401
from wallex_mcp.config import cfg

@mcp.http(path="/health", method="GET")
async def health():
    return {"status": "ok", "timestamp": cfg.current_timestamp()}

if __name__ == "__main__":
    mcp.run(host=cfg.HOST, port=cfg.PORT)
