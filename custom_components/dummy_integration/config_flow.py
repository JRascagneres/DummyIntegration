import logging
from .coordinators.dummy_integration import data_calc
from homeassistant import config_entries
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class DummyIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        return


    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        try:
            await self.hass.async_add_executor_job(data_calc,self.hass, None, None)
        except Exception as e:
            _LOGGER.error(e)
            errors["base"] = "error"

        else:
            return self.async_create_entry(title="Dummy Integration", data={})

        return self.async_show_form(step_id="user", data_schema=None, errors=errors)