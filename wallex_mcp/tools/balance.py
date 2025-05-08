from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import BalancesResult
from pydantic import ValidationError

@mcp.tool()
async def get_balance() -> BalancesResult:
    """Returns all wallet balances for the authenticated account."""
    client = WallexClient()
    result = await client.get("/account/balances")
    await client.close()
    try:
        return BalancesResult(**result)
    except ValidationError as err:
        return repr(err.errors()[0]['type'])
