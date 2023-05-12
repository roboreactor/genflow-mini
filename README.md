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

Roboreactor Genflow Mini is a platform that helps you build robotic and automation systems faster and with rich functionality. It allows you to control general-purpose mobile computers to build robotics and automation systems in a timely manner and reduce complexity in tasks. With the Roboreactor node generator, you can generate code from the website into the robot and automation system from anywhere in the world with no gap in development.

We also have a function to help you manage the components you need for your project. It allows you to manage the components and code to match the functionality with the complete hardware you have uploaded into the project and the code that you generated on the website. This helps you to manage the functionality of the system remotely via the Roboreactor profile website.

In addition, we have motion planning to connect with your robot remotely via our fast IoT system, allowing you to control the robot's motion system faster from anywhere. This allows you to run the robot under development with no gap in distances.

The IoT on the Roboreactor allows you to manage data from the robot in real-time, helping you collect and visualize data from the robot and paving the way for agile development of AI and digital twins on the robot. With the IoT advantage, we can combine this function to allow you to visualize the data from Lidar to make the navigation system for a robot on the website.

Inside the node, functionality communicates with the UDP to send data from one node to the other, allowing you to replicate the function to control as many devices as you can in the local network, increasing the possibility of doing swarm and group tasks better inside the node that you replicate on each device.

<br>

# Installation

<details>
<summary>

## Genflow Mini OS (for RaspberryPi, Jetson)

</summary>

> 💡 We strongly recommend using a premium SD card from a reputable manufacturer such as Sandisk, Kingston, or Samsung, with an "A1" (or better) grade and a capacity of at least 64GB.

1. [Download](https://roboreactor.com/download/) the latest Genflow Mini OS release (don’t unpack the zip; you don’t need to).
2. Flash the Genflow Mini OS image to the SD card with [balenaEtcher](https://www.balena.io/etcher/).
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

5. Eject the SD card from your PC and insert it to the SBC
6. Download `data_token_secret_key.json` from your project [page](https://roboreactor.com/profile).
7. Copy the `data_token_secret_key.json` into your SBC `./RoboreactorGenFlow` folder with [WinSCP](https://winscp.net/eng/download.php) you can get the SBC IP address from [wireless network watcher](https://www.nirsoft.net/utils/wireless_network_watcher.html) or other IP scanner software
8. Your genflow page will be available at `http://YourSbcIP:8000`

</details>
<details>
<summary>

## Manual Setup (for other SBC support most of linux-based OS)

</summary>

> 💡 We strongly recommend using a premium SD card from a reputable manufacturer such as Sandisk, Kingston, or Samsung, with an "A1" (or better) grade and a capacity of at least 64GB.

1. Setup your SBC OS and Wi-Fi
2. Remote SSH into the SBC with [PuTTY](https://www.putty.org) and run the following command to clone this repo form github

```
cd ~
git clone https://github.com/roboreactor/genflow-mini
```

3. Copy the `data_token_secret_key.json` into your SBC `./genflow-mini` folder with [WinSCP](https://winscp.net/eng/download.php)
4. Remote SSH into the SBC and run the following command to install genflow mini and wait until installation complete

> 💡 this step might take up to 10 hours

```
cd ~/genflow-mini
bash installer.sh
```

5. Your genflow page will be available at `http://YourSbcIP:8000`

</details>
<div align="right">[ <a href="#roboreactor-genflow-mini">☝️to top </a> ]</div>
<br>





<div align="right">[ <a href="#roboreactor-genflow-mini">☝️to top </a> ]</div>
