"""BlueprintEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, MANUFACTURER
from .coordinator import Healthbox3DataUpdateCoordinator


class Healthbox3Entity(CoordinatorEntity):
    """Healthbox3Entity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: Healthbox3DataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.data.serial

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=coordinator.data.description,
            manufacturer=MANUFACTURER,
            sw_version=coordinator.data.serial,
            hw_version=coordinator.data.warranty_number,
        )
