from __future__ import annotations

import logging

from dateutil import tz
from config.custom_components.dummy_integration.coordinators.dummy_integration import DummyIntegrationCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .const import DOMAIN, DATA_CLIENT

from homeassistant.core import HomeAssistant

PLATFORMS = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    coordinator = DummyIntegrationCoordinator(hass, entry)
    hass.data[DOMAIN][DATA_CLIENT] = coordinator

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
