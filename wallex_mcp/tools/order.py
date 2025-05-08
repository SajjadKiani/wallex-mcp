from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import OrderRequest, OrderResponse
import json

@mcp.tool()
async def place_order(order: OrderRequest):
    """Places a new order on the exchange."""
    client = WallexClient()
    # Use alias to include fields like `type` correctly
    result = await client.post("/account/orders", json=order.get('order'))
    await client.close()
    try:
        return OrderResponse(**result)
    except:
        return result

@mcp.tool()
async def get_order_status(order_id: str) -> OrderResponse:
    """Gets the status of an existing order by its ID."""
    client = WallexClient()
    result = await client.get(f"/orders/{order_id}")
    await client.close()
    try:
        return OrderResponse(**result)
    except:
        return result


@mcp.tool()
async def cancel_order(order_id: str) -> OrderResponse:
    """Cancels an existing order by its ID."""
    client = WallexClient()
    result = await client.delete(f"/orders/{order_id}")
    await client.close()
    try:
        return OrderResponse(**result)
    except:
        return result


