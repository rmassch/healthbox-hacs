"""DataUpdateCoordinator for healthbox."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.exceptions import ConfigEntryAuthFailed


from pyhealthbox3.healthbox3 import (
    Healthbox3,
    Healthbox3ApiClientAuthenticationError,
    Healthbox3ApiClientError,
)

from .const import (
    DOMAIN,
    LOGGER,
    SCAN_INTERVAL,
)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class HealthboxDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    api: Healthbox3

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, api: Healthbox3
    ) -> None:
        """Initialize."""

        self.hass = hass
        self.config_entry = entry
        self.host: str = entry.data[CONF_HOST]
        self.api: Healthbox3 = api

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=f"{DOMAIN} - {self.host}",
            update_interval=SCAN_INTERVAL,
        )

    async def change_room_profile(
        self, room_id: int, profile_name: str
    ):
        """Start Boosting HB Room."""
        await self.api.async_change_room_profile(
            room_id=room_id, profile_name=profile_name
        )

    async def start_room_boost(
        self, room_id: int, boost_level: int, boost_timeout: int
    ):
        """Start Boosting HB Room."""
        await self.api.async_start_room_boost(
            room_id=room_id, boost_level=boost_level, boost_timeout=boost_timeout
        )

    async def stop_room_boost(self, room_id: int):
        """Stop Boosting HB Room."""
        await self.api.async_stop_room_boost(room_id=room_id)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            await self.api.async_get_data()

        except Healthbox3ApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except Healthbox3ApiClientError as exception:
            raise UpdateFailed(exception) from exception
