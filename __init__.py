"""The SMA Speedwire integration."""
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (EVENT_HOMEASSISTANT_STOP)

from sma_query_sw.protocol import SMAClientProtocol

from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_INVERTER_SERIAL,
    CONF_NAME_ID,
    CONF_PASSWORD,
    CONF_PORT
)

import logging

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the SMA Speedwire component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up SMA Speedwire from a config entry."""

    inverter_config = entry.data

    inverter = hass.data[DOMAIN].setdefault(entry.entry_id, {"command_query_list": [
        "energy_production",
        "spot_ac_power",
        "spot_ac_voltage",
        "spot_dc_power",
        "spot_dc_voltage",
        "grid_frequency",
        "inverter_status",
        "grid_relay_status",
        "inverter_temperature"
    ]})

    inverter[CONF_IP_ADDRESS] = inverter_config[CONF_IP_ADDRESS]
    inverter[CONF_PORT] = inverter_config[CONF_PORT]
    inverter[CONF_INVERTER_SERIAL] = inverter_config[CONF_INVERTER_SERIAL]
    inverter[CONF_NAME_ID] = inverter_config[CONF_NAME_ID]
    inverter[CONF_PASSWORD] = inverter_config[CONF_PASSWORD]

    on_connection_lost = hass.loop.create_future()

    inverter["transport"], inverter["protocol"] = await hass.loop.create_datagram_endpoint(
        lambda: SMAClientProtocol(inverter, on_connection_lost), remote_addr=(inverter_config[CONF_IP_ADDRESS],
                                                                              inverter_config.get("port", 9522)))

    # Shutdown event closure
    async def async_shutdown_event(call):
        _LOGGER.info("Shutting down SMA Speedwire")
        await inverter["transport"].close()

    hass.bus.async_listen(EVENT_HOMEASSISTANT_STOP, async_shutdown_event)

    for platform in PLATFORMS:
        await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(await asyncio.gather(*[
        hass.config_entries.async_forward_entry_unload(entry, component)
        for component in PLATFORMS
    ]))

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
