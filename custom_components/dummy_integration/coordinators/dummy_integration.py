import logging
from datetime import timedelta
from typing import Any

from _collections_abc import Mapping

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..const import DOMAIN
from ..models import DummyIntegrationData

_LOGGER = logging.getLogger(__name__)

class DummyIntegrationCoordinator(DataUpdateCoordinator[DummyIntegrationData]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=5)
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

    return DummyIntegrationData(
        test_int=current_data['test_int'] + 1
    )

