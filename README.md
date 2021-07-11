# SMA SunnyBoy Inverter SpeedWire™ integration

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Description

A Home Assistant Integration for querying SMA SunnyBoy Inverters using the SpeedWire™ protocol.

## Installation

### Dependencies
This integration relies on the library at https://github.com/Wired-Square/sma-query 

The sma-query library should first be installed into Home Assistants virtual environment.

### Home Assistant

This integration has been tested against Home Assistant 2021.5.0.

The integration can be installed by cloning this repository into the Home Assistant ```custom_components``` directory.

Assuming Home Assistant is running on a Raspberry Pi using the installation guide at https://www.home-assistant.io/installation/raspberrypi for the Home Assistant Core version, the following commands could be used to install the integration. Alter as needed to suit your installation.
```bash
sudo su - homeassistant
cd /srv/homeassistant/data

# If the custom_components directory doesn't exist, create it
mkdir custom_components

# Clone repo into custom_components directory
git clone https://github.com/Wired-Square/homeassistant-sma-sw.git smasw
```

Once Home Assistant has been restarted the integration can be activated under Configuration -> Integrations -> "+ Add Integration"
Search for sma, an integration with the name "SunnyBoy Inverter Speedwire" will appear, there is no logo yet.

You will be asked a number of questions, the IP address and user password of the inverter will be needed, all other settings can use defaults.

The process should be repeated for each inverter on the network. Subsequent integrations will be grouped under the main integration by IP address.


