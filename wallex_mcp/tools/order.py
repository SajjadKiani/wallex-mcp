from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import OrderRequest, OrderResponse


@mcp.tool()
async def place_order(order: OrderRequest) -> OrderResponse:
    """Places a new order on the exchange."""
    client = WallexClient()
    # Use alias to include fields like `type` correctly
    payload = order.model_dump(by_alias=True)
    result = await client.post("/account/orders", json=payload)
    await client.close()
    return OrderResponse(**result)

@mcp.tool()
async def get_order_status(order_id: str) -> OrderResponse:
    """Gets the status of an existing order by its ID."""
    client = WallexClient()
    result = await client.get(f"/orders/{order_id}")
    await client.close()
    return OrderResponse(**result)


@mcp.tool()
async def cancel_order(order_id: str) -> OrderResponse:
    """Cancels an existing order by its ID."""
    client = WallexClient()
    result = await client.delete(f"/orders/{order_id}")
    await client.close()
    return OrderResponse(**result)


