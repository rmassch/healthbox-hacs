"""Sensor platform for healthbox."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import DOMAIN, HealthboxRoom, LOGGER
from .coordinator import HealthboxDataUpdateCoordinator


@dataclass
class HealthboxRoomEntityDescriptionMixin:
    """Mixin values for Healthbox Room entities."""

    room: HealthboxRoom
    is_on: bool


@dataclass
class HealthboxRoomBinarySensorEntityDescription(
    BinarySensorEntityDescription, HealthboxRoomEntityDescriptionMixin
):
    """Class describing Healthbox Room binary sensor entities."""


def generate_binary_room_sensors_for_healthbox(
    coordinator: HealthboxDataUpdateCoordinator,
) -> list[HealthboxRoomBinarySensorEntityDescription]:
    """Generate binary sensors for each room."""
    room_binary_sensors: list[HealthboxRoomBinarySensorEntityDescription] = []

    for room in coordinator.api.rooms:
        if room.boost is not None:
            room_binary_sensors.append(
                HealthboxRoomBinarySensorEntityDescription(
                    key=f"{room.room_id}_boost_status",
                    name=f"{room.name} Boost Status",
                    room=room,
                    is_on=lambda x: x.boost.enabled
                )
            )

    return room_binary_sensors


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: HealthboxDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    room_binary_sensors = generate_binary_room_sensors_for_healthbox(
        coordinator=coordinator)

    entities = []

    for description in room_binary_sensors:
        entities.append(HealthboxRoomBinarySensor(coordinator, description))

    async_add_entities(entities)


class HealthboxRoomBinarySensor(
    CoordinatorEntity[HealthboxDataUpdateCoordinator], BinarySensorEntity
):
    """Representation of a Healthbox Room Sensor."""

    entity_description: HealthboxRoomBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: HealthboxDataUpdateCoordinator,
        description: HealthboxRoomBinarySensorEntityDescription,
    ) -> None:
        """Initialize Binary Sensor Domain."""
        super().__init__(coordinator)

        self.entity_description = description
        self._attr_unique_id = f"{
            coordinator.config_entry.entry_id}-{description.room.room_id}-{description.key}"
        self._attr_name = f"{description.name}"
        self._attr_device_info = DeviceInfo(
            name=self.entity_description.room.name,
            identifiers={
                (
                    DOMAIN,
                    f"{coordinator.config_entry.unique_id}_{
                        self.entity_description.room.room_id}",
                )
            },
            manufacturer="Renson",
            model="Healthbox Room",
        )

    @property
    def is_on(self) -> bool:
        """Binary Sensor native value."""
        room_id: int = int(self.entity_description.room.room_id)

        matching_room = [
            room for room in self.coordinator.api.rooms if int(room.room_id) == room_id
        ]

        if len(matching_room) != 1:
            error_msg: str = f"No matching room found for id {room_id}"
            LOGGER.error(error_msg)
        else:
            matching_room = matching_room[0]
            return self.entity_description.is_on(matching_room)
