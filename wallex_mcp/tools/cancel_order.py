from fastmcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import OrderResponse


@mcp.tool()
async def cancel_order(order_id: str) -> OrderResponse:
    """Cancels an existing order by its ID."""
    client = WallexClient()
    result = await client.delete(f"/orders/{order_id}")
    await client.close()
    return OrderResponse(**result)
