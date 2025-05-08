from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import MarketsResponse
from pydantic import ValidationError

@mcp.tool()
async def get_markets():
    """ Get All Markets Data."""
    client = WallexClient()
    result = await client.get("/markets")
    await client.close()
    # result expected as a list of instrument dicts
    return result