# Healthbox 3 Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Community Forum][forum-shield]][forum]

_Integration to integrate with [healthbox3][healthbox3]._

[![Renson][rensonimg]][resonurl]

## Installation

### HACS
#### If published

1. Launch HACS
1. Navigate to the Integrations section
1. "+ Explore & Add Repositories" button in the bottom-right
1. Search for "Healthbox 3"
1. Select "Install this repository"
1. Restart Home Assistant

#### HACS (Manual)

1. Launch HACS
1. Navigate to the Integrations section
1. Click the three dots at the top right
1. Custom Repositories
1. Enter the Repository URL: [healthbox3]
1. Add
1. Restart Home Assistant

### Home Assistant

1. Go to the integrations page
1. Click on the "Add Integration" button at the bottom-right
1. Search for the "Healthbox 3" integration
1. Select the Healthbox 3 integration


## Configuration

### Options

This integration can only be configured through the UI, and the options below can be configured when the integration is added.

| key       | default        | required | description                                     |
| --------- | -------------- | -------- | ----------------------------------------------- |
| host      | none      | yes      | The IP of the Healthbox 3 device               |
| api_key      | none           | no      | The API key if you want advanced API features and sensors enabled   |

### API Key
The API key can be requested through the Renson support. They will give you the key if you send an e-mail to  service@renson.be
and mention your device serial number.

## Sensors
By default:
* Global Air Quality Index
* Serial/Warranty Number
* Firmware
* Boost Level per room

If the API key is provided this integration will enabled the advanced API features which will expose the following sensors per room:
* Temperature
* Humidity
* Air Quality Index
* CO2 Concentration

## Services
### Start Room Boost
| parameter       | type        | required | description                                     |
| --------- | -------------- | -------- | ----------------------------------------------- |
| device_id      | str      | yes      | The Healthbox 3 Room Device               |
| boost_level    | int           | yes      | The level you want to boost to. Between 100% and 200%  |
| boost_timeout    | int           | yes      | The boost duration in minutes  |

### Stop Room Boost
| parameter       | type        | required | description                                     |
| --------- | -------------- | -------- | ----------------------------------------------- |
| device_id      | str      | yes      | The Healthbox 3 Room Device               |


<!-- ## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md) -->

<!-- *** -->

[healthbox3]: https://github.com/rmassch/healthbox3
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/rmassch/healthbox3.svg?style=for-the-badge
[commits]: https://github.com/rmassch/healthbox3/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[rensonimg]: https://www.renson.eu/Renson/media/Renson-images/renson-logo.png?ext=.png
[resonurl]: https://www.renson.eu/gd-gb/producten-zoeken/ventilatie/mechanische-ventilatie/units/healthbox-3-0
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/rmassch/healthbox3.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-@rmassch-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/rmassch/healthbox3.svg?style=for-the-badge
[releases]: https://github.com/rmassch/healthbox3/releases
