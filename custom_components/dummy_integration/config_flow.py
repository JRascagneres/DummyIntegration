from homeassistant import config_entries
from .const import DOMAIN

class DummyIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        return


    async def async_step_user(self, user_input=None):
        return self.async_create_entry(title="Dummy Integration", data={})