"""Custom integration to integrate healthbox3 with Home Assistant.

For more details about this integration, please refer to
https://github.com/rmassch/healthbox3
"""
from __future__ import annotations
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import Healthbox3ApiClient
from .const import DOMAIN, SERVICE_BOOST_ROOM
from .coordinator import Healthbox3DataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]

# Platform.BINARY_SENSOR,
# Platform.SWITCH,


SERVICE_BOOST_ROOM_SCHEMA = vol.Schema(
    {
        vol.Required("room_id"): cv.positive_int,
        vol.Required("boost_level"): cv.positive_int,
        vol.Required("boost_timeout"): cv.positive_int,
    },
)


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = Healthbox3DataUpdateCoordinator(
        hass=hass, entry=entry
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def boost_room(call: ServiceCall) -> None:
        """Service call to add a new filter subscription to AdGuard Home."""

        await coordinator.boost_room(
            room_id=call.data["room_id"],
            boost_level=call.data["boost_level"],
            boost_timeout=call.data["boost_timeout"],
        )

    hass.services.async_register(
        DOMAIN, SERVICE_BOOST_ROOM, boost_room, schema=SERVICE_BOOST_ROOM_SCHEMA
    )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
