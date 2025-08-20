# Multi-Service Docker Compose Configuration for Home Assistant

A sample Docker Compose configuration for the smart home services I use: [Home Assistant](https://www.home-assistant.io/), [Mosquitto MQTT](https://mosquitto.org/), [Frigate NVR](https://frigate.video/), [Music Assistant](https://music-assistant.io/), and [selenium/standalone-chrome](https://hub.docker.com/r/selenium/standalone-chrome) for Selenium automation within Home Assistant.

## Table of Contents

- [Description](#multi-service-docker-compose-configuration-for-home-assistant)
- [Getting Started](#getting-started)
- [License](#license)
- [Disclaimer](#disclaimer)

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/mwdle/HomeAssistantConfig.git
   ```

2. Create a folder on your system for Docker bind mounts / storing container files. The folder should have the following structure:

   ```shell
   docker_volumes/
   ├── Frigate/
   │   ├── config/
   │   └── storage/
   ├── HomeAssistant/
   │   ├── config/
   │   └── .ssh/
   ├── MQTT/
   │   ├── config/
   │   ├── data/
   │   └── log/
   └── MusicAssistant/
       └── data/
   ```

3. Create a file called `.env` in the same directory as `compose.yaml` containing the following properties:

   ```properties
   DOCKER_VOLUMES=<PATH_TO_DOCKER_VOLUMES_FOLDER> # The folder created in the previous step.
   RTSP_USER=<YOUR_RTSP_USER> # For Frigate
   RTSP_PASSWORD=<YOUR_RTSP_PASSWORD> # For Frigate
   MQTT_USER=<YOUR_MQTT_USER> # For Frigate
   MQTT_PASSWORD=<YOUR_MQTT_PASSWORD> # For Frigate
   MUSIC_VOLUME=<YOUR_MUSIC_LIBRARY_FOLDER> # A folder containing your local music library for Music Assistant.
   ROUTER_PASSWORD=<YOUR_ROUTER_PASSWORD> # For router rebooter pyscript automation
   EXTENDER_PASSWORD=<YOUR_EXTENDER_PASSWORD> # For extender rebooter pyscript automation
   ```

4. Open a terminal in the directory containing the compose.yaml file.
5. Create docker networks for the containers

   ```shell
   docker network create -d macvlan --subnet=192.168.0.0/24 --gateway=192.168.0.1 -o parent=eno1 AAA_LAN # Ensure the gateway and subnet match your LAN network. YOUR LAN SHOULD BE TRUSTED. AAA in the name ensures Docker uses this network as the primary interface for all connected containers.
   docker network create Frigate
   docker network create HomeAssistant
   docker network create MusicAssistant
   docker network create Chrome
   ```

   The networks are configured in compose.yaml such that:

   - Containers in the same network are accessible from each other by their container names.
   - Music Assistant is in a macvlan, making it appear to be a physical interface on the host's LAN (allowing mDNS / device discovery). Make sure to reserve the IP address listed for Music Assistant in compose.yaml on your router's web interface.
   - Home Assistant is in a macvlan, making it appear to be a physical interface on the host's LAN (allowing mDNS / device discovery). Make sure to reserve the IP address listed for Home Assistant in compose.yaml on your router's web interface.
   - Frigate's Port 8555 (for WebRTC) is bound to port 8555 on the host.
   - Frigate and MQTT can directly communicate.
   - Home Assistant and MQTT can directly communicate.
   - Home Assistant and Chrome can directly communicate for Selenium automation via pyscript.
   - Home Assistant and Music Assistant can communicate so long as you add your Reverse Proxy for MA to the Home Assistant Docker network using a _Docker Network Alias_ to connect with.
   - Home Assistant and Frigate can communicate so long as you add your Reverse Proxy for Frigate to the Home Assistant Docker network using a _Docker Network Alias_ to connect with.

6. Start the containers:

   ```shell
   docker compose up -d
   ```

7. Configure Home Assistant Dashboard (Optional): After deploying Home Assistant with the router_rebooter pyscript app files from this repository and setting up template buttons in `configuration.yaml` to trigger the services, you can add a dashboard card for easy access to the rebooter functionality:

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

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE.txt) file for details.

## Disclaimer

This repository is provided as-is and is intended for informational and reference purposes only. The author assumes no responsibility for any errors or omissions in the content or for any consequences that may arise from the use of the information provided. Always exercise caution and seek professional advice if necessary.
