"""Custom integration to integrate healthbox3 with Home Assistant.

For more details about this integration, please refer to
https://github.com/rmassch/healthbox3
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr

from .const import (
    DOMAIN,
    SERVICE_START_ROOM_BOOST,
    SERVICE_START_ROOM_BOOST_SCHEMA,
    SERVICE_STOP_ROOM_BOOST,
    SERVICE_STOP_ROOM_BOOST_SCHEMA,
    PLATFORMS,
    ALL_SERVICES,
)
from .coordinator import Healthbox3DataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""

    coordinator = Healthbox3DataUpdateCoordinator(hass=hass, entry=entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Define Services
    async def start_room_boost(call: ServiceCall) -> None:
        """Service call to start boosting fans in a room."""
        device_id = call.data["device_id"]
        device_registry = dr.async_get(hass)
        device = device_registry.async_get(device_id)

        if device:
            device_identifier = next(iter(device.identifiers))[1]
            room_id: int = int(device_identifier.split("_")[-1])
            await coordinator.start_room_boost(
                room_id=room_id,
                boost_level=call.data["boost_level"],
                boost_timeout=call.data["boost_timeout"] * 60,
            )

    async def stop_room_boost(call: ServiceCall) -> None:
        """Service call to stop boosting fans in a room."""
        device_id = call.data["device_id"]
        device_registry = dr.async_get(hass)
        device = device_registry.async_get(device_id)

        if device:
            device_identifier = next(iter(device.identifiers))[1]
            room_id: int = int(device_identifier.split("_")[-1])
            await coordinator.stop_room_boost(room_id=room_id)

    # Register Services
    hass.services.async_register(
        DOMAIN,
        SERVICE_START_ROOM_BOOST,
        start_room_boost,
        SERVICE_START_ROOM_BOOST_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN, SERVICE_STOP_ROOM_BOOST, stop_room_boost, SERVICE_STOP_ROOM_BOOST_SCHEMA
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        for service in ALL_SERVICES:
            hass.services.async_remove(DOMAIN, service)
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
