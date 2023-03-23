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
        # return await self._api_wrapper(
        #     method="get", url="https://jsonplaceholder.typicode.com/posts/1"
        # )
        general_data = await self._api_wrapper(
            method="get", url=f"http://{self._ipaddress}/v2/api/data/current"
        )

        return general_data

    async def async_start_room_boost(
        self, room_id: int, boost_level: int, boost_timeout: int
    ) -> any:
        """Start Boosting HB3 Room."""
        data = {"enable": True, "level": boost_level, "timeout": boost_timeout}
        await self._api_wrapper(
            method="put",
            url=f"http://{self._ipaddress}/v2/api/boost/{room_id}",
            data=data,
        )

    async def async_stop_room_boost(self, room_id: int) -> any:
        """Stop Boosting HB3 Room."""
        data = {"enable": False}
        await self._api_wrapper(
            method="put",
            url=f"http://{self._ipaddress}/v2/api/boost/{room_id}",
            data=data,
        )

    async def async_get_room_boost_data(self, room_id: int) -> any:
        """Get boost data from the API."""
        data = await self._api_wrapper(
            method="get", url=f"http://{self._ipaddress}/v2/api/boost/{room_id}"
        )
        return data

    async def async_enable_advanced_api_features(self):
        """Enable advanced API Features."""

        await self._api_wrapper(
            method="post",
            url=f"http://{self._ipaddress}/v2/api/api_key",
            data=f"{self._apikey}",
            expect_json_error=True,
        )
        await asyncio.sleep(2)
        await self._async_validate_advanced_api_features()

    async def _async_validate_advanced_api_features(self):
        """Validate API Advanced Features."""
        authentication_status = await self._api_wrapper(
            method="get", url=f"http://{self._ipaddress}/v2/api/api_key/status"
        )
        if authentication_status["state"] != "valid":
            raise Healthbox3ApiClientAuthenticationError

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | str | None = None,
        headers: dict | None = None,
        expect_json_error: bool = False,
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
                if expect_json_error:
                    return await response.text()
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
