from wallex_mcp.mcp import mcp
from wallex_mcp.client import WallexClient
from wallex_mcp.schemas import BalanceResponse


@mcp.tool()
async def get_balance(account_id: str) -> BalanceResponse:
    """Fetches the balance for a given account."""
    client = WallexClient()
    result = await client.get(f"/accounts/{account_id}/balance")
    await client.close()
    return BalanceResponse(**result)
