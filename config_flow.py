"""Config flow for SMA Speedwire."""
import logging

import voluptuous as vol

from homeassistant import config_entries

import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_INVERTER_SERIAL,
    CONF_NAME_ID,
    CONF_PASSWORD,
    CONF_PORT
)

_LOGGER = logging.getLogger(__name__)


class CANSwitchFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a SMA Speedwire config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize SMA Speedwire ConfigFlow."""
        self.ip_address = ""
        self.serial_number = 0

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            if _device_already_added(self._async_current_entries(), user_input[CONF_IP_ADDRESS]):
                return self.async_abort(reason="already_configured")

            self.ip_address = user_input[CONF_IP_ADDRESS]
            self.serial_number = user_input[CONF_INVERTER_SERIAL]
            self.name_id = user_input[CONF_NAME_ID]
            self.password = user_input[CONF_PASSWORD]
            self.port = user_input[CONF_PORT]

            return self.async_create_entry(
                title=self.ip_address, data={
                    CONF_IP_ADDRESS: self.ip_address,
                    CONF_INVERTER_SERIAL: self.serial_number,
                    CONF_NAME_ID: self.name_id,
                    CONF_PASSWORD: self.password,
                    CONF_PORT: self.port
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): cv.string,
                    vol.Required(CONF_INVERTER_SERIAL): cv.positive_int,
                    vol.Required(CONF_NAME_ID, default="sma"): cv.string,
                    vol.Required(CONF_PASSWORD, default="0000"): cv.string,
                    vol.Optional(CONF_PORT, default=9522): cv.positive_int
                }
            ),
        )


def _device_already_added(current_entries, ip_address):
    """Determine if entry has already been added to HA."""
    for entry in current_entries:
        entry_ip_address = entry.data.get(CONF_IP_ADDRESS)

        if entry_ip_address == ip_address:
            return True

    return False
