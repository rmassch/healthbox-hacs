"""DataUpdateCoordinator for healthbox3."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    Healthbox3ApiClient,
    Healthbox3ApiClientAuthenticationError,
    Healthbox3ApiClientError,
)
from .const import (
    DOMAIN,
    LOGGER,
    Healthbox3DataObject,
    Healthbox3RoomBoost,
)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class Healthbox3DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    api: Healthbox3ApiClient
    entry: ConfigEntry

    data: Healthbox3DataObject

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )

        self.entry = entry

        api_key = None
        if CONF_API_KEY in entry.data:
            api_key = entry.data[CONF_API_KEY]

        self.api = Healthbox3ApiClient(
            ipaddress=entry.data[CONF_IP_ADDRESS],
            apikey=api_key,
            session=async_get_clientsession(hass),
        )

    async def start_room_boost(
        self, room_id: int, boost_level: int, boost_timeout: int
    ):
        """Start Boosting HB3 Room."""
        await self.api.async_start_room_boost(
            room_id=room_id, boost_level=boost_level, boost_timeout=boost_timeout
        )

    async def stop_room_boost(self, room_id: int):
        """Stop Boosting HB3 Room."""
        await self.api.async_stop_room_boost(room_id=room_id)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.api.async_get_data()

            hb3_data: Healthbox3DataObject = Healthbox3DataObject(data=data)
            for room in hb3_data.rooms:
                boost_data = await self.api.async_get_room_boost_data(room.room_id)

                room.boost = Healthbox3RoomBoost(
                    boost_data["level"], boost_data["enable"], boost_data["remaining"]
                )

            return hb3_data

        except Healthbox3ApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except Healthbox3ApiClientError as exception:
            raise UpdateFailed(exception) from exception
