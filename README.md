# Multi-Service Docker Compose Configuration for Home Assistant

A sample Docker Compose configuration for Home Assistant, MQTT, Frigate, Music Assistant, and [RouterRebooter](https://github.com/mwdle/RouterRebooter).  

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

2. Change the ```.env``` file properties:  

    ```properties
    DOCKER_VOLUMES=<PATH_TO_DOCKER_VOLUMES> # A folder on your system to store bind mounts for Docker containers.
    ```  

3. Open a terminal in the directory containing the docker-compose file.  
4. Start the container:  

    ```shell
    docker compose up -d
    ```  

Your containers ...

## License  

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE.txt) file for details.  

## Disclaimer  

This repository is provided as-is and is intended for informational and reference purposes only. The author assumes no responsibility for any errors or omissions in the content or for any consequences that may arise from the use of the information provided. Always exercise caution and seek professional advice if necessary.  
