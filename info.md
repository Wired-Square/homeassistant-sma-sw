# SMA Speedwire HACS integration

**This component will set up the following platforms.**

| Platform        | Description                         |
| --------------- | ----------------------------------- |
| `binary_sensor` | Show something `True` or `False`.   |
| `sensor`        | Show info from API.                 |
| `switch`        | Switch something `True` or `False`. |

{% if not installed %}

## Installation

1. Click install.
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "sunnyboy inverter".

{% endif %}

## Configuration is done in the UI

You will be asked a number of questions, the IP address and user password of the inverter will be needed, all other settings can use defaults.
The process should be repeated for each inverter on the network. Subsequent integrations will be grouped under the main integration by IP address.

<!---->

## Credits

This HACS integration was created from [@Wired-Square](https://github.com/Wired-Square)'s [Home Assistant Custom SMA Speedwire code](https://github.com/Wired-Square/homeassistant-sma-sw) repository and has custom changes to make it ready for HACS and for the HA version 2024.1.6.

Full credits to original authors [@Wired-Square](https://github.com/Wired-Square).
and [@garthberry](https://github.com/garthberry).
