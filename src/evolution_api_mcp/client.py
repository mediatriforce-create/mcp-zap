"""Evolution API async HTTP client."""

import asyncio
import os
from typing import Any, Optional

import httpx


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        self.status_code = status_code
        super().__init__(message)


class RateLimitError(ApiError):
    pass


class EvolutionClient:
    """Async HTTP client for Evolution API."""

    def __init__(self):
        self._base_url = os.environ.get(
            "EVOLUTION_API_URL", "http://localhost:8080"
        ).rstrip("/")
        self._api_key = os.environ.get("EVOLUTION_API_KEY", "")
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=httpx.Timeout(30.0, read=60.0),
                limits=httpx.Limits(max_connections=20),
            )
        return self._client

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
    ) -> Any:
        client = await self._get_client()
        headers = {"apikey": self._api_key, "Content-Type": "application/json"}

        for attempt in range(3):
            response = await client.request(
                method,
                f"/{endpoint.lstrip('/')}",
                params=params,
                json=json_data,
                headers=headers,
            )

            if response.status_code in (200, 201):
                return response.json()

            if response.status_code == 429:
                if attempt < 2:
                    await asyncio.sleep(2 ** (attempt + 1))
                    continue
                raise RateLimitError(response.text, status_code=429)

            raise ApiError(
                f"HTTP {response.status_code}: {response.text}",
                status_code=response.status_code,
            )

        raise ApiError("Max retries exceeded")

    async def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json_data: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("POST", endpoint, json_data=json_data)

    async def put(self, endpoint: str, json_data: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("PUT", endpoint, json_data=json_data)

    async def delete(self, endpoint: str) -> Any:
        return await self.request("DELETE", endpoint)

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()


# Singleton
_client: Optional[EvolutionClient] = None


def get_client() -> EvolutionClient:
    global _client
    if _client is None:
        _client = EvolutionClient()
    return _client
