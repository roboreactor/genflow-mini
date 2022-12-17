<div align="center">
<img width="200" src="./RoboreactorGenFlow/static/favicon.png">
<br>

# Roboreactor Genflow Mini

<br>
<a href="https://github.com/roboreactor/genflow-mini/releases"><img src="https://img.shields.io/github/languages/code-size/roboreactor/genflow-mini?logo=GitHub&color=14b7e3"/></a>
<a href="https://github.com/roboreactor/genflow-mini/commit"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/roboreactor/genflow-mini?logo=GitHub&color=2394f7"></a>
<a href="https://github.com/roboreactor/genflow-mini/releases"><img src="https://img.shields.io/github/v/release/roboreactor/genflow-mini?display_name=tag&logo=GitHub&color=5078f3"/></a>
<a href="./RoboreactorGenFlow/LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg?logo=Open Source Initiative&logoColor=f5f5f5&color=9254f7"></a>
<img src="https://img.shields.io/badge/OS-linux-teal??style=flat&logo=Linux&logoColor=f5f5f5&color=d653f1" alt="Operating systems">

[Website](https://roboreactor.com) •
[Facebook](https://www.facebook.com/groups/496935899075410/) •
[Discord](https://discord.gg/guGDf24nrF) •
[Installation](#installation) •
[Credits](#credits)

<br>
</div>

Roboreactor Genflow Mini is the platform to help you build robotic and automation systems faster and with rich functionality to control general-purpose mobile computers to build robotics and automation systems at timeless and reduce complexity in tasks to help you build interesting and cool robotics and automation systems with Roboreactor node generator to generate the code from the website into the robot and automation system from anywhere in the world with no gap in development and
we have a function to help you manage the components that you need for the project allow you to manage the components and code to match the functionality with the complete hardware you uploaded into the project and code that you generated on the website help you to manage the functionality of the system remotely via Roboreactor profile website and we have motion planning to connect with your robot remotely via our fast IoT system
to allow you to control the robot motion system faster from anywhere allow you to run the robot under development with no gap of distances.
The IoT on the Roboreactor allows you to manage data from the robot in real-time to help you collect and visualize data from the robot and pave the way to agile development for AI and digital twins on the robot.
from the IoT advantage, we can combine this function to allow you to use it to visualize the data from Lidar to make the navigation system from a robot into the website.
Inside the node, functionality communicates with the UDP to send the data from one node to the other allowing you to replicate the function to control as many devices as you can in the local network
increasing the possibility to do swarm and group tasks better inside the node that you replicate on each device.

<br>

# Installation

<details>
<summary>

## Genflow Mini OS (for rpi, jetson)

</summary>

> 💡 We strongly recommend you use a premium SD card from a reputable manufacturer such as Sandisk, Kingston or Samsung, using an “A1” (or better) grade SD card with more then 64GB capacity.

1. [Download](https://roboreactor.com/download/) the latest Genflow Mini OS release (don’t unpack the zip; you don’t need to).
2. Flash the Genflow Mini OS image to the sd card with [balenaEtcher](https://www.balena.io/etcher/).
3. Setup Wi-Fi for a headless Pi install the network SSID and password must be entered into `/etc/wpa_supplicant/wpa_supplicant.conf` locate the relevant section to your network, remove the comment marks (#) and enter the SSID and password. WPA/WPA2 is the most common.

```
Original:
## WPA/WPA2 secured
#network={
#  ssid="put SSID here"
#  psk="put password here"
#}

Filled out:
## WPA/WPA2 secured
network={
  ssid="CaseSensitive_WIFI"
  psk="SuperSecrets"
}

...

# Uncomment the country your Pi is in to activate Wifi in RaspberryPi 3 B+ and above
# For full list see: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

country=GB # United Kingdom
```

5. Eject the sd card from your pc and insert it to the sbc
6. Download `data_token_secret_key.json` from your project [page](https://roboreactor.com/profile).
7. Copy the `data_token_secret_key.json` into your sbc `./RoboreactorGenFlow` folder with [WinSCP](https://winscp.net/eng/download.php) you can get the sbc ip address from [wireless network watcher](https://www.nirsoft.net/utils/wireless_network_watcher.html) or other ip scanner software
8. your genflow page will available at `http://YourSbcIP:8000`

</details>
<details>
<summary>

## Manual Setup (for other sbc support most of linux based os)

</summary>

> 💡 We strongly recommend you use a premium SD card from a reputable manufacturer such as Sandisk, Kingston or Samsung, using an “A1” (or better) grade SD card with more then 64GB capacity.

1. Setup your sbc os and Wi-Fi
2. Remote SSH into the sbc with [PuTTY](https://www.putty.org) and run the following command to clone this repo form github

```
cd ~
git clone https://github.com/roboreactor/genflow-mini
```

3. Copy the `data_token_secret_key.json` into your sbc `./genflow-mini` folder with [WinSCP](https://winscp.net/eng/download.php)
4. Remote SSH into the sbc and run the following command to install genflow mini and wait until installation complete

> 💡 this step might take up to 10 hours

```
cd ~/genflow-mini
bash installer.sh
```

5. your genflow page will available at `http://YourSbcIP:8000`

</details>
<div align="right">[ <a href="#roboreactor-genflow-mini">☝️to top </a> ]</div>
<br>

# Credits

## inspired by

- KevinOConnor [Klipper](https://github.com/Klipper3d/klipper)

<div align="right">[ <a href="#roboreactor-genflow-mini">☝️to top </a> ]</div>
