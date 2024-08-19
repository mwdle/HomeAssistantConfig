# Multi-Service Docker Compose Configuration for Home Assistant

A sample Docker Compose configuration for the smart home services I use: Home Assistant, MQTT, Frigate, Music Assistant, and [RouterRebooter](https://github.com/mwdle/RouterRebooter).  

## Table of Contents  

* [Description](#multi-service-docker-compose-configuration-for-home-assistant)  
* [Getting Started](#getting-started)  
* [License](#license)  
* [Disclaimer](#disclaimer)  

## Getting Started  

1. Clone the repository:  

    ```shell
    git clone https://github.com/mwdle/HomeAssistantConfig.git
    ```  

2. Create a folder on your system for Docker bind mounts / storing container files. The folder should have the following structure:  

    ```shell
    docker_volumes/
    ├── Frigate/
    │   ├── config/
    │   └── storage/
    ├── HomeAssistant/
    │   ├── config/
    │   └── .ssh/
    ├── MQTT/
    │   ├── config/
    │   ├── data/
    │   └── log/
    ├── MusicAssistant/
    │   └── data/
    ├── RouterRebooter/
    │   ├── data/
    │   └── secrets/
    ```  

3. Create a file called ```.env``` in the same directory as ```docker-compose.yml``` containing the following properties:  

    ```properties
    DOCKER_VOLUMES=<PATH_TO_DOCKER_VOLUMES_FOLDER> # The folder created in the previous step.
    RTSP_USER=<YOUR_RTSP_USER> # For Frigate
    RTSP_PASSWORD=<YOUR_RTSP_PASSWORD> # For Frigate
    MQTT_USER=<YOUR_MQTT_USER> # For Frigate
    MQTT_PASSWORD=<YOUR_MQTT_PASSWORD> # For Frigate
    MUSIC_VOLUME=<YOUR_MUSIC_LIBRARY_FOLDER> # A folder containing your local music library for Music Assistant.
    ```  

4. Open a terminal in the directory containing the docker-compose file.  
5. Create docker networks for the containers

    ```shell
    docker network create -d macvlan --subnet=192.168.0.0/24 --gateway=192.168.0.1 -o parent=eno1 AAA_LAN # Ensure the gateway and subnet match your LAN network. YOUR LAN SHOULD BE TRUSTED. AAA in the name ensures Docker uses this network as the primary interface for all connected containers.
    docker network create MQTT
    docker network create Frigate
    docker network create HomeAssistant
    docker network create MusicAssistant
    docker network create RouterRebooter
    ```  

    The networks are configured in docker-compose.yml such that:  
    * Containers in the same network are accessible from each other by their container names.  
    * Music Assistant is in a macvlan, making it appear to be a physical interface on the host LAN (for mDNS / device discovery). Ensure you reserved the IP address set in docker-compose.yml for Music Assistant in your router.  
    * Home Assistant is in a macvlan, making it appear to be a physical interface on the host LAN (for mDNS / device discovery). Ensure you reserved the IP address set in docker-compose.yml for Home Assistant in your router.  
    * Frigate's Port 8555 (for WebRTC) is bound to port 8555 on the host.
    * Frigate and MQTT can directly communicate.  
    * Home Assistant and MQTT can directly communicate.  
    * Home Assistant and Frigate can directly communicate.  
    * Home Assistant and RouterRebooter can directly communicate.  
    * Home Assistant and Music Assistant can directly communicate.  

6. Start the containers:  

    ```shell
    docker compose up -d
    ```  

7. To update images and containers (RouterRebooter must be built using the [RouterRebooter repository](https://github.com/mwdle/RouterRebooter)):  

    ```shell
    docker compose pull --ignore-pull-failures # RouterRebooter must be built using a dockerfile from the RouterRebooter repository, so trying to pull it will fail.
    docker compose up -d
    ```  

Your containers should now be up and running! Attach your reverse proxy container to the previously created Docker Networks and configure it accordingly.  

## License  

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE.txt) file for details.  

## Disclaimer  

This repository is provided as-is and is intended for informational and reference purposes only. The author assumes no responsibility for any errors or omissions in the content or for any consequences that may arise from the use of the information provided. Always exercise caution and seek professional advice if necessary.  
