from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient


@mcp.tool()
async def get_markets():
    """ Get All Markets Data."""
    client = WallexClient()
    result = await client.get("/markets")
    await client.close()
    # result expected as a list of instrument dicts
    return result