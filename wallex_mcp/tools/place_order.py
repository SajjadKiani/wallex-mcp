from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import OrderRequest, OrderResponse


@mcp.tool()
async def place_order(order: OrderRequest) -> OrderResponse:
    """Places a new order on the exchange."""
    client = WallexClient()
    # Use alias to include fields like `type` correctly
    payload = order.dict(by_alias=True)
    result = await client.post("/orders", json=payload)
    await client.close()
    return OrderResponse(**result)
