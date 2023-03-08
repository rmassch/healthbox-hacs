"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class Healthbox3ApiClientError(Exception):
    """Exception to indicate a general API error."""


class Healthbox3ApiClientCommunicationError(Healthbox3ApiClientError):
    """Exception to indicate a communication error."""


class Healthbox3ApiClientAuthenticationError(Healthbox3ApiClientError):
    """Exception to indicate an authentication error."""


class Healthbox3ApiClient:
    """Sample API Client."""

    def __init__(
        self,
        ipaddress: str,
        apikey: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._ipaddress = ipaddress
        self._apikey = apikey
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get", url="https://jsonplaceholder.typicode.com/posts/1"
        )

    async def async_set_title(self, value: str) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise Healthbox3ApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise Healthbox3ApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Healthbox3ApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise Healthbox3ApiClientError(
                "Something really wrong happened!"
            ) from exception
