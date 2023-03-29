# Healthbox 3 Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Community Forum][forum-shield]][forum]

_Integration to integrate with [healthbox][healthbox]._

[![Renson][rensonimg]][resonurl]

## DISCLAIMER
This is still a work in progress. If time permits, I'll try to push this to HACS or Home Assistant Core.

## Known Issues
- Missing Branding

## Installation

### HACS

<!-- #### If published

1. Launch HACS
1. Navigate to the Integrations section
1. "+ Explore & Add Repositories" button in the bottom-right
1. Search for "Renson Healthbox"
1. Select "Install this repository"
1. Restart Home Assistant -->

#### HACS (Manual)

1. Launch HACS
1. Navigate to the Integrations section
1. Click the three dots at the top right
1. Custom Repositories
1. Enter the Repository URL: https://github.com/rmassch/healthbox-hacs
1. Select Category -> Integration
1. Click Add
1. Close the modal
1. The integration should show up as a new repository, if not, search "Renson Healthbox" in "Explore & Download Repositories"
1. Click the integration & Download
1. Restart Home Assistant

### Home Assistant

1. Go to Settings -> Devices & Services
1. Click on the "+ Add Integration" button at the bottom-right
1. Search for the "Renson Healthbox" integration
1. Select the Renson Healthbox integration
1. Enter the Host IP & API Key (if applicable)
1. Submit


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

(See: https://community.home-assistant.io/t/renson-healthbox-3-0/52983/57)

## Sensors
By default:
* Global Air Quality Index
* Serial Number
* Warranty Number
* Boost Level per room

If the API key is provided this integration will enabled the advanced API features which will expose the following sensors per room (if available):
* Temperature
* Humidity
* Air Quality Index
* CO2 Concentration
* Volatile Organic Compounds

## Services
### Start Room Boost
| parameter       | type        | required | description                                     |
| --------- | -------------- | -------- | ----------------------------------------------- |
| device_id      | str      | yes      | The Healthbox 3 Room Device               |
| boost_level    | int           | yes      | The level you want to boost to. Between 10% and 200%  |
| boost_timeout    | int           | yes      | The boost duration in minutes  |

### Stop Room Boost
| parameter       | type        | required | description                                     |
| --------- | -------------- | -------- | ----------------------------------------------- |
| device_id      | str      | yes      | The Healthbox 3 Room Device               |


<!-- ## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md) -->

<!-- *** -->

[healthbox]: https://github.com/rmassch/healthbox-hacs
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/rmassch/healthbox-hacs.svg?style=for-the-badge
[commits]: https://github.com/rmassch/healthbox-hacs/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[rensonimg]: https://www.renson.eu/Renson/media/Renson-images/renson-logo.png?ext=.png
[resonurl]: https://www.renson.eu/gd-gb/producten-zoeken/ventilatie/mechanische-ventilatie/units/healthbox-3-0
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/rmassch/healthbox-hacs.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-@rmassch-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/rmassch/healthbox-hacs.svg?style=for-the-badge
[releases]: https://github.com/rmassch/healthbox-hacs/releases
