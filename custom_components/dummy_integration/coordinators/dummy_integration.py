import logging
from datetime import timedelta, datetime
from typing import Any

from _collections_abc import Mapping

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.recorder import history
from homeassistant.util import dt as dt_util

from ..const import DOMAIN
from ..models import DummyIntegrationData

_LOGGER = logging.getLogger(__name__)

class DummyIntegrationCoordinator(DataUpdateCoordinator[DummyIntegrationData]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=1)
        )
        self._entry = entry

    @property
    def entry_id(self) -> str:
        return self._entry.entry_id

    async def _async_update_data(self) -> DummyIntegrationData:
        try:
            data = await self.hass.async_add_executor_job(
                data_calc, self.hass, self._entry.data, self.data
            )
        except:
            raise Exception()

        return data


def data_calc(hass: HomeAssistant, config: Mapping[str, Any], current_data: DummyIntegrationData) -> DummyIntegrationData:
    if current_data is None:
        current_data = DummyIntegrationData(test_int=0)

    # These are examples.
    # data = read_state_history(hass, dt_util.utcnow() - timedelta(hours=10), dt_util.utcnow(), "sensor.sun_next_dawn")
    # write_state(hass, "sensor.sun_next_dawn", "2023-11-21T07:01:37+00:00")

    return DummyIntegrationData(
        test_int=current_data['test_int'] + 1
    )


def read_state_history(hass: HomeAssistant, start: datetime, end:datetime, full_id: str) -> Mapping[str, Any]:
    data = history.state_changes_during_period(hass, start, end, full_id, include_start_time_state=True, no_attributes=True)
    return data


def write_state(hass: HomeAssistant, full_id: str, value: Any):
    hass.states.set(full_id, value)
    return