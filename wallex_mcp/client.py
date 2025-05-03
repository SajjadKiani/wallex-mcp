'''HTTP client wrapper for Wallex API using httpx.

Provides async methods for GET, POST, PUT, DELETE requests,
handles API key header and error checking.
'''
import os
import httpx
from typing import Any, Dict, Optional
from wallex_mcp.config import cfg


class WallexClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 10.0,
    ):
        self.api_key = api_key or cfg.API_KEY
        self.base_url = base_url or cfg.BASE_URL
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"X-API-Key": self.api_key},
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        headers: Dict[str, str] = {}
        if json is not None:
            headers["Content-Type"] = "application/json"

        response = await self._client.request(
            method,
            endpoint,
            params=params,
            json=json,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        # Wallex wraps results under "result" on success
        if isinstance(data, dict) and not data.get("success", True):
            message = data.get("message", "Unknown error")
            raise RuntimeError(f"Wallex API error: {message}")

        return data.get("result", data)

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return await self.request("GET", endpoint, params=params)

    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return await self.request("POST", endpoint, json=json)

    async def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return await self.request("PUT", endpoint, json=json)

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return await self.request("DELETE", endpoint, params=params)

    async def close(self) -> None:
        await self._client.aclose()
