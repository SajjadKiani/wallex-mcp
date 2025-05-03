'''Resource handlers for Wallex MCP server. Decorated with @mcp.resource to expose read-only endpoints.'''
from fastmcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import InstrumentsResponse, MarketDataResponse, OrderResponse


@mcp.resource("wallex://instruments")
async def get_instruments() -> InstrumentsResponse:
    """Fetches the list of available trading instruments."""
    client = WallexClient()
    result = await client.get("/instruments")
    await client.close()
    # result expected as a list of instrument dicts
    return InstrumentsResponse(instruments=result)


@mcp.resource("wallex://market/{symbol}")
async def market_data(symbol: str) -> MarketDataResponse:
    """Retrieves ticker data for a given symbol."""
    client = WallexClient()
    result = await client.get(f"/market/{symbol}/ticker")
    await client.close()
    # result expected as a dict matching Ticker model
    return MarketDataResponse(ticker=result)


@mcp.resource("wallex://orders/{order_id}")
async def get_order_status(order_id: str) -> OrderResponse:
    """Gets the status of an existing order by its ID."""
    client = WallexClient()
    result = await client.get(f"/orders/{order_id}")
    await client.close()
    return OrderResponse(**result)
