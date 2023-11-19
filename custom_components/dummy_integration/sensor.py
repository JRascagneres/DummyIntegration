from dataclasses import dataclass
from datetime import datetime
from homeassistant.components.sensor.const import SensorStateClass
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinators.dummy_integration import DummyIntegrationCoordinator, write_state
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN, DATA_CLIENT

@dataclass
class DummyIntegrationSensorEntityDescription(SensorEntityDescription):
    """Provide a description of sensor"""

    # For backwards compat, allow description to override unique ID key to use
    unique_id: str | None = None


SENSORS = [
    DummyIntegrationSensorEntityDescription(
        key="test_int",
        name="Name",
        unique_id="name",
        native_unit_of_measurement="GBP",
        icon="mdi:currency-gbp",
        state_class=SensorStateClass.MEASUREMENT
    ),
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: DummyIntegrationCoordinator = hass.data[DOMAIN][DATA_CLIENT]

    async_add_entities(DummyIntegrationSensor(coordinator, description) for description in SENSORS)

    return True


class DummyIntegrationSensor(CoordinatorEntity[DummyIntegrationCoordinator], SensorEntity):
    entity_desription: DummyIntegrationSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(self, coordinator, description) -> None:
        super().__init__(coordinator)
        self.entity_description = description

        self._attr_state_class = description.state_class
        self._attr_device_class = description.device_class

        self._attr_device_info = DeviceInfo(
            configuration_url=None,
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            manufacturer="JRascagneres",
            name="Dummy Integration",
        )

        self._attr_unique_id = f"{coordinator.entry_id}_{description.unique_id}"
        self._attr_icon = description.icon

    @property
    def available(self) -> bool:
        return True

    @property
    def native_value(self) -> float | datetime | None:
        value = self.coordinator.data[self.entity_description.key]
        return value

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self.entity_description.native_unit_of_measurement