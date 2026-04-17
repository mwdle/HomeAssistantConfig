# Multi-Service Docker Compose Configuration for Home Assistant

A sample Docker Compose configuration for the smart home and supportive services I use: [Home Assistant](https://www.home-assistant.io/), [Mosquitto MQTT](https://mosquitto.org/), [Frigate NVR](https://frigate.video/), [Music Assistant](https://music-assistant.io/), [Glances](https://github.com/nicolargo/glances), [Home Assistant Matter Hub (Riddix Fork)](https://github.com/RiDDiX/home-assistant-matter-hub), and [selenium/standalone-chrome](https://hub.docker.com/r/selenium/standalone-chrome) for Selenium automation within Home Assistant.

## Configure Home Assistant Dashboard (Optional)

After deploying Home Assistant with the router_rebooter pyscript files from this repository and setting up template buttons in `configuration.yaml` to trigger the services, you can add a dashboard card for easy access to the rebooter functionality:

```yaml
type: entities
entities:
  - entity: button.reboot_router
  - entity: pyscript.router_rebooter_status
  - entity: button.reboot_extender
  - entity: pyscript.extender_rebooter_status
title: Rebooters
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This repository is provided as-is and is intended for informational and reference purposes only. The author assumes no responsibility for any errors or omissions in the content or for any consequences that may arise from the use of the information provided. Always exercise caution and seek professional advice if necessary.
