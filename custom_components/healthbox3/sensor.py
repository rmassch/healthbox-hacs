"""Sensor platform for healthbox3."""
from __future__ import annotations

from decimal import Decimal
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.const import (
    UnitOfTemperature,
    PERCENTAGE,
    CONCENTRATION_PARTS_PER_MILLION,
)

from .const import DOMAIN, Healthbox3Room
from .coordinator import Healthbox3DataUpdateCoordinator
from .entity import Healthbox3Entity


@dataclass
class Healthbox3RoomEntityDescriptionMixin:
    """Mixin values for Healthbox3 entities."""

    room: Healthbox3Room
    value_fn: Callable[[], float | int | str | Decimal | None]


@dataclass
class Healthbox3RoomSensorEntityDescription(
    SensorEntityDescription, Healthbox3RoomEntityDescriptionMixin
):
    """Class describing Healthbox3 sensor entities."""


@dataclass
class Healthbox3GlobalEntityDescriptionMixin:
    """Mixin values for Healthbox3 Global entities."""

    value_fn: Callable[[], float | int | str | Decimal | None]


@dataclass
class Healthbox3GlobalSensorEntityDescription(
    SensorEntityDescription, Healthbox3GlobalEntityDescriptionMixin
):
    """Class describing Healthbox3 sensor entities."""


ROOM_SENSORS: list[Healthbox3RoomSensorEntityDescription] = []
HEALTHBOX3_GLOBAL_SENSORS: list[Healthbox3GlobalSensorEntityDescription] = []


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the sensor platform."""
    coordinator: Healthbox3DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    HEALTHBOX3_GLOBAL_SENSORS.append(
        Healthbox3GlobalSensorEntityDescription(
            key=f"{DOMAIN}_global_aqi",
            name="Healthbox3 Global Air Quality Index",
            native_unit_of_measurement=None,
            icon="mdi:leaf",
            device_class=SensorDeviceClass.AQI,
            state_class=SensorStateClass.MEASUREMENT,
            value_fn=lambda x: x.global_aqi,
            suggested_display_precision=2,
        ),
    )
    async_add_entities(
        Healthbox3GlobalSensorEntity(coordinator, entry, description)
        for description in HEALTHBOX3_GLOBAL_SENSORS
    )

    if coordinator.api.advanced_api:
        for room in coordinator.data.rooms:
            ROOM_SENSORS.append(
                Healthbox3RoomSensorEntityDescription(
                    key=f"{room.room_id}_temperature",
                    name=f"{room.name} Temperature",
                    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                    icon="mdi:thermometer",
                    device_class=SensorDeviceClass.TEMPERATURE,
                    state_class=SensorStateClass.MEASUREMENT,
                    room=room,
                    value_fn=lambda x: x.indoor_temperature,
                    suggested_display_precision=2,
                ),
            )
            ROOM_SENSORS.append(
                Healthbox3RoomSensorEntityDescription(
                    key=f"{room.room_id}_humidity",
                    name=f"{room.name} Humidity",
                    native_unit_of_measurement=PERCENTAGE,
                    icon="mdi:water-percent",
                    device_class=SensorDeviceClass.HUMIDITY,
                    state_class=SensorStateClass.MEASUREMENT,
                    room=room,
                    value_fn=lambda x: x.indoor_humidity,
                    suggested_display_precision=2,
                ),
            )
            if room.indoor_co2_concentration is not None:
                ROOM_SENSORS.append(
                    Healthbox3RoomSensorEntityDescription(
                        key=f"{room.room_id}_co2_concentration",
                        name=f"{room.name} CO2 Concentration",
                        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
                        icon="mdi:molecule-co2",
                        device_class=SensorDeviceClass.CO2,
                        state_class=SensorStateClass.MEASUREMENT,
                        room=room,
                        value_fn=lambda x: x.indoor_co2_concentration,
                        suggested_display_precision=2,
                    ),
                )
            if room.indoor_aqi is not None:
                ROOM_SENSORS.append(
                    Healthbox3RoomSensorEntityDescription(
                        key=f"{room.room_id}_aqi",
                        name=f"{room.name} Air Quality Index",
                        native_unit_of_measurement=None,
                        icon="mdi:leaf",
                        device_class=SensorDeviceClass.AQI,
                        state_class=SensorStateClass.MEASUREMENT,
                        room=room,
                        value_fn=lambda x: x.indoor_aqi,
                        suggested_display_precision=2,
                    ),
                )
    for room in coordinator.data.rooms:
        if room.boost is not None:
            ROOM_SENSORS.append(
                Healthbox3RoomSensorEntityDescription(
                    key=f"{room.room_id}_boost_level",
                    name=f"{room.name} Boost Level",
                    native_unit_of_measurement=PERCENTAGE,
                    icon="mdi:fan",
                    # device_class=SensorDeviceClass.,
                    state_class=SensorStateClass.MEASUREMENT,
                    room=room,
                    value_fn=lambda x: x.boost.level,
                    suggested_display_precision=2,
                ),
            )

    async_add_entities(
        Healthbox3RoomSensorEntity(coordinator, entry, description)
        for description in ROOM_SENSORS
    )


class Healthbox3GlobalSensorEntity(Healthbox3Entity, SensorEntity):
    """Representation of a Healthbox 3 Room Sensor."""

    entity_description: Healthbox3GlobalSensorEntityDescription
    coordinator: Healthbox3DataUpdateCoordinator

    def __init__(
        self,
        coordinator: Healthbox3DataUpdateCoordinator,
        entry: ConfigEntry,
        description: Healthbox3GlobalSensorEntityDescription,
    ) -> None:
        """Initialize Sensor Domain."""
        super().__init__(coordinator)
        self.entity_description = description
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> float | int | str | Decimal:
        """Sensor native value."""
        return self.entity_description.value_fn(self.coordinator.data)


class Healthbox3RoomSensorEntity(Healthbox3Entity, SensorEntity):
    """Representation of a Healthbox 3 Room Sensor."""

    entity_description: Healthbox3RoomSensorEntityDescription
    coordinator: Healthbox3DataUpdateCoordinator

    def __init__(
        self,
        coordinator: Healthbox3DataUpdateCoordinator,
        entry: ConfigEntry,
        description: Healthbox3RoomSensorEntityDescription,
    ) -> None:
        """Initialize Sensor Domain."""
        super().__init__(coordinator)
        self.entity_description = description
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.entry.entry_id, self.entity_description.room.room_id)
            },
            name=self.entity_description.room.name,
            manufacturer="Renson",
            model=f"{self.coordinator.data.description} Room",
            # via_device=(DOMAIN, self.api.bridgeid),
        )

    @property
    def native_value(self) -> float | int | str | Decimal:
        """Sensor native value."""
        return self.entity_description.value_fn(
            self.coordinator.data.rooms[int(self.entity_description.room.room_id) - 1]
        )
