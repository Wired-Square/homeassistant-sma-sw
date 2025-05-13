from datetime import timedelta

import logging

import async_timeout

from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_FRIENDLY_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    UnitOfEnergy,
    UnitOfPower
)

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
    ATTR_STATE_CLASS
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    DOMAIN,
    CONF_IP_ADDRESS,
    CONF_INVERTER_SERIAL,
    CONF_NAME_ID,
    CONF_INVERTER_DATA,
    CONF_SCALE,
    CONF_ROUND,
    CONF_FORMAT,
    DEFAULT_NAME
)


_LOGGER = logging.getLogger(__name__)


SENSOR_TYPES = {
    "total": {
        CONF_FRIENDLY_NAME: "Energy Production Total",
        CONF_DEVICE_CLASS: SensorDeviceClass.ENERGY,
        CONF_SCALE: 0.001,
        CONF_UNIT_OF_MEASUREMENT: UnitOfEnergy.KILO_WATT_HOUR,
        ATTR_STATE_CLASS: SensorStateClass.TOTAL_INCREASING
    },
    "today": {
        CONF_FRIENDLY_NAME: "Energy Production Daily",
        CONF_DEVICE_CLASS: SensorDeviceClass.ENERGY,
        CONF_SCALE: 0.001,
        CONF_UNIT_OF_MEASUREMENT: UnitOfEnergy.KILO_WATT_HOUR,
        ATTR_STATE_CLASS: SensorStateClass.TOTAL_INCREASING
},
    "spot_ac_power": {
        CONF_FRIENDLY_NAME: "AC Power",
        CONF_DEVICE_CLASS: SensorDeviceClass.POWER,
        CONF_SCALE: 1,
        CONF_UNIT_OF_MEASUREMENT: UnitOfPower.WATT,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
},
    "spot_ac_voltage": {
        CONF_FRIENDLY_NAME: "AC Voltage",
        CONF_DEVICE_CLASS: "voltage",
        CONF_SCALE: 0.01,
        CONF_UNIT_OF_MEASUREMENT: "V",
        CONF_ROUND: 2,
        CONF_FORMAT: ".02f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_ac_current": {
        CONF_FRIENDLY_NAME: "AC Current",
        CONF_DEVICE_CLASS: "current",
        CONF_SCALE: 0.001,
        CONF_UNIT_OF_MEASUREMENT: "A",
        CONF_ROUND: 3,
        CONF_FORMAT: ".03f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_dc_power1": {
        CONF_FRIENDLY_NAME: "DC Power 1",
        CONF_DEVICE_CLASS: SensorDeviceClass.POWER,
        CONF_SCALE: 1,
        CONF_UNIT_OF_MEASUREMENT: UnitOfPower.WATT,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_dc_power2": {
        CONF_FRIENDLY_NAME: "DC Power 2",
        CONF_DEVICE_CLASS: SensorDeviceClass.POWER,
        CONF_SCALE: 1,
        CONF_UNIT_OF_MEASUREMENT: UnitOfPower.WATT,
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_dc_voltage1": {
        CONF_FRIENDLY_NAME: "DC Voltage 1",
        CONF_DEVICE_CLASS: "voltage",
        CONF_SCALE: 0.01,
        CONF_UNIT_OF_MEASUREMENT: "V",
        CONF_ROUND: 2,
        CONF_FORMAT: ".02f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_dc_voltage2": {
        CONF_FRIENDLY_NAME: "DC Voltage 2",
        CONF_DEVICE_CLASS: "voltage",
        CONF_SCALE: 0.01,
        CONF_UNIT_OF_MEASUREMENT: "V",
        CONF_ROUND: 2,
        CONF_FORMAT: ".02f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_dc_current1": {
        CONF_FRIENDLY_NAME: "DC Current 1",
        CONF_DEVICE_CLASS: "current",
        CONF_SCALE: 0.001,
        CONF_UNIT_OF_MEASUREMENT: "A",
        CONF_ROUND: 3,
        CONF_FORMAT: ".03f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "spot_dc_current2": {
        CONF_FRIENDLY_NAME: "DC Current 2",
        CONF_DEVICE_CLASS: "current",
        CONF_SCALE: 0.001,
        CONF_UNIT_OF_MEASUREMENT: "A",
        CONF_ROUND: 3,
        CONF_FORMAT: ".03f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "grid_frequency": {
        CONF_FRIENDLY_NAME: "Grid Frequency",
        CONF_DEVICE_CLASS: None,
        CONF_SCALE: 0.01,
        CONF_UNIT_OF_MEASUREMENT: "Hz",
        CONF_ROUND: 2,
        CONF_FORMAT: ".02f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    },
    "inverter_status": {
        CONF_FRIENDLY_NAME: "Inverter Status",
        CONF_DEVICE_CLASS: f"{DOMAIN}__inverter_status",
        CONF_SCALE: 1,
        CONF_UNIT_OF_MEASUREMENT: "",
        ATTR_STATE_CLASS:  None
    },
    "grid_relay_status": {
        CONF_FRIENDLY_NAME: "Grid Relay Status",
        CONF_DEVICE_CLASS: f"{DOMAIN}__grid_relay_status",
        CONF_SCALE: 1,
        CONF_UNIT_OF_MEASUREMENT: "",
        ATTR_STATE_CLASS:  None
    },
    "inverter_temperature": {
        CONF_FRIENDLY_NAME: "Temperature",
        CONF_DEVICE_CLASS: "temperature",
        CONF_SCALE: 0.01,
        CONF_UNIT_OF_MEASUREMENT: "°C",
        CONF_ROUND: 2,
        CONF_FORMAT: ".02f",
        ATTR_STATE_CLASS: SensorStateClass.MEASUREMENT
    }
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up SMA Speedwire from a config entry."""
    sensors = []
    inverter = hass.data[DOMAIN][entry.entry_id]
    inverter["sensors"] = sensors

    async def async_update_data():
        async with async_timeout.timeout(10):
            inverter["protocol"].start_query()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"{DEFAULT_NAME}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )
    
    for (entity_attribute, entity_detail) in SENSOR_TYPES.items():
        inverter.setdefault("data", {})[entity_attribute] = 0

    await coordinator.async_refresh()

    for (entity_attribute, entity_detail) in SENSOR_TYPES.items():
        sensors.append(SMASWSensor(coordinator, inverter, entity_attribute, entity_detail))

    async_add_entities(sensors, True)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return True


class SMASWSensor(CoordinatorEntity, SensorEntity):
    """Implementation of a SMA Speedwire Sensor."""
    def __init__(self, coordinator, inverter, entity_attribute, entity_detail):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._state = None
        self._inverter = inverter
        self._entity_attribute = entity_attribute
        self._unit_of_measure = entity_detail[CONF_UNIT_OF_MEASUREMENT]
        self._state_class = entity_detail[ATTR_STATE_CLASS]
        self._round = entity_detail.get(CONF_ROUND, None)
        self._format = entity_detail.get(CONF_FORMAT, None)
        self._scale = entity_detail[CONF_SCALE]
        self._name = f"""{inverter[CONF_NAME_ID]} {entity_detail[CONF_FRIENDLY_NAME]}"""
        self._unique_id = f"""{inverter[CONF_NAME_ID]} {entity_detail[CONF_FRIENDLY_NAME]}"""
        self._device_class = entity_detail[CONF_DEVICE_CLASS]
        self._serial_number = inverter[CONF_INVERTER_SERIAL]
        self._ip_address = inverter[CONF_IP_ADDRESS]
        self._attributes = {"address": f"{self._ip_address}"}

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self._serial_number)},
            "name": "SMA SunnyBoy Inverter Speedwire",
            "manufacturer": "SMA",
            "sw_version": "Unknown",
            "model": "SunnyBoy",
            "via_device": (DOMAIN, self._serial_number),
        }

    @property
    def device_class(self):
        return self._device_class

    @property
    def state_class(self):
        return self._state_class

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name
        
    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"
        
    @property
    def available(self):
        return self._inverter[CONF_INVERTER_DATA].get("total", 0) > 0

    @property
    def state(self):
        """Return the state of the sensor."""
        self._state = self._inverter[CONF_INVERTER_DATA].get(self._entity_attribute, 0) * self._scale

        if self._round:
            self._state = round(self._state, self._round)
        elif self._entity_attribute == "inverter_status":
            if self._state == 35:
                self._state = "fault"
            elif self._state == 303:
                self._state = "off"
            elif self._state == 307:
                self._state = "ok"
            elif self._state == 455:
                self._state = "warning"
        elif self._entity_attribute == "grid_relay_status":
            if self._state == 51:
                self._state = "connected"
            elif self._state == 311:
                self._state = "disconnected"
            elif self._state == 16777213:
                self._state = "status_not_available"

        if self._format:
            return f"{self._state:{self._format}}"
        else:
            return self._state

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def unit_of_measurement(self):
        return  self._unit_of_measure
