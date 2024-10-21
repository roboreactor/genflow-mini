#!/bin/bash

# Instructions:
#  run script without sudo `bash installer.sh`

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Copyright (c) 2022 Chanapai Chuadchum and Tanatorn Pravalpadd @ roboreactor.com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

NC='\033[0m' 		     # No Color
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Cyan='\033[0;36m'         # Cyan

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

echo -e "${Yellow}
======================================================================================
${NC}"
echo -e "${Cyan}
     
                        ╣╢╢╣╢╢╗╦╗╗╗╗╗╗╗╗╗╗╗╗╗╗╗╗╗╦╦
                         ╙╝▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░╗
                            ╙╣▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░╕
                                                ╚░▒░░░░
                              ╓╣╢╢╢╢╢╢╢╢╢╢╢╢╗╦   ╚▒░░░░
                            ╫▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ╒░░░░▒
                           ╔▒▒▒▒▒▒╨╜╙╙╙╙         ╢░░░░╜
                           ║▒▒▒▒▒╜       ╓╥╦╦╦╦╬░░░░░▒░
                           ║▒▒▒▒▒      ╬▒▒▒▒▒▒▒▒░░░░▒░
                           ║▒▒▒▒▒     ╫▒▒▒▒▒▒▒╜╙╙╙╙
                           ║▒▒▒▒▒     ╙▒▒▒▒▒▒╣
                           ▒▒▒▒▒▒      ╙▒▒▒▒▒▒╢
                           ▒▒▒▒▒▒       └╢▒▒▒▒▒▒╖
                           ▒▒▒▒▒▒         ╫▒▒▒▒▒▒╗
                           ▒▒▒▒▒▒          ╙▒▒▒░░░╣
                           ▒▒▒▒▒▒            ╢▒▒░░░▒┐
                           ▒▒▒▒▒▒             ╫▒░░░░░╗
                           ║▒▒▒▒▒              ╙▒░░░░░╣
 
              █▀▀█ █▀▀█ █▀▀▄ █▀▀█ █▀▀█ █▀▀ █▀▀█ █▀▀ ▀▀█▀▀ █▀▀█ █▀▀█ 
              █▄▄▀ █░░█ █▀▀▄ █░░█ █▄▄▀ █▀▀ █▄▄█ █░░ ░░█░░ █░░█ █▄▄▀ 
              ▀░▀▀ ▀▀▀▀ ▀▀▀░ ▀▀▀▀ ▀░▀▀ ▀▀▀ ▀░░▀ ▀▀▀ ░░▀░░ ▀▀▀▀ ▀░▀▀ 
                        █▀▀▀ █▀▀ █▀▀▄ █▀▀ █░░ █▀▀█ █░░░█ 
                        █░▀█ █▀▀ █░░█ █▀▀ █░░ █░░█ █▄█▄█ 
                        ▀▀▀▀ ▀▀▀ ▀░░▀ ▀░░ ▀▀▀ ▀▀▀▀ ░▀░▀░ 
                                   🅼 🅸 🅽 🅸  
${NC}"
echo -e "${Yellow}
======================================================================================
${NC}"

# keyboardinterrupt force installer to stop and remove all possible generated file
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Stop() {
       echo -e "${Yellow}
======================================================================================
       ${NC}"
       sudo rm -r ./RoboreactorGenFlow/data_token_secret.json ~/get-pip.py ~/package-lock.json ~/Face_db/ ~/Printrun/ ~/Roboreactor_Gen_config/ ~/RoboreactorGenFlow/ ~/Roboreactor_library/ ~/Roboreactor_projects/ ~/g2opy/ ~/node_modules/ ~/portaudio/> /dev/null 2>&1
       exit 0 
}
trap Stop INT

# check require file
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

for dir in \
        "$PWD/Face_db/" \
        "$PWD/Printrun/" \
        "$PWD/Roboreactor_Gen_config/" \
        "$PWD/RoboreactorGenFlow/" \
        "$PWD/Roboreactor_library/" \
        "$PWD/Roboreactor_projects/" 
do
    if ! [ -d "$dir" ]; then
       echo -e "${Red}
${dir} not found
please re download it from https://roboreactor.com/download
       ${NC}"
       echo -e "${Yellow}
======================================================================================
       ${NC}"
       exit 0 
    fi
done
if [ ! -f data_token_secret.json ]; then
    echo -e "${Red}
${PWD}/data_token_secret.json not found
please download it from your project page
    ${NC}"
    echo -e "${Yellow}
======================================================================================
    ${NC}"
    exit 0 
fi

# coppy roboreactor files to final dir
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sudo rm -r ./RoboreactorGenFlow/data_token_secret.json ~/get-pip.py ~/package-lock.json ~/Face_db/ ~/Printrun/ ~/Roboreactor_Gen_config/ ~/RoboreactorGenFlow/ ~/Roboreactor_library/ ~/Roboreactor_projects/ ~/g2opy/ ~/node_modules/ ~/portaudio/> /dev/null 2>&1
sudo mkdir -p  ~/
sudo cp data_token_secret.json ./RoboreactorGenFlow/data_token_secret.json
sudo cp -r Face_db/ Printrun/ Roboreactor_Gen_config/ RoboreactorGenFlow/ Roboreactor_library/ Roboreactor_projects/ ~/

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

cd ~/
#sudo apt-get autoremove vlc -y 
#sudo apt-get purge vlc -y 
#sudo apt-get clean 
sudo apt-get update && sudo apt-get upgrade -y # Upgrade the installer for the hardware lnux ubuntu 
sudo apt-get install git -y 
#sudo apt-get install python3-dev  -y 
sudo apt install build-essential libssl-dev libffi-dev python3-setuptools -y 
#Update and install python3 pip package 
echo 'Boot strap python3 pip installer'
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip3 install virtualenv    # Install the virtual environment 
sudo apt install python3-venv -y
sudo apt-get install cmake -y 
sudo apt-get install curl -y 
echo 'Git installation'
sudo apt-get install git -y # Install git
sudo apt-get install python3-tk -y
sudo apt-get install scrot -y
echo "install open ssh"
sudo apt-get install openssh-server -y
echo "Install Htop"
sudo apt-get install htop -y
sudo apt-get install snap -y
curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh
sudo apt-get install rust -y
#sudo apt-get install arduino -y  
sudo apt install pipx -y 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

echo "Install i2c data"
sudo apt-get install i2c-tools -y 
sudo pip3 install i2csense # install the i2 sensor library for upgrading the connection between the i2c sensors module
echo "Install smbus for communication protocol"

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

       #GPU checker 
sudo apt install mesa-utils -y 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sudo pip3 install smbus  #install the smbus protocol for communication with the sensors onboard on devices or robot automation 
sudo pip3 install smbus2 #install the smbus2 protocol for the communication with the sensors onboard devices of the robot automation
sudo pip3 install Adafruit-Blinka
sudo pip3 install bmp280 #install the bmp280 for the Barometer and temoerature sensor
sudo pip3 install pyudev 
sudo pip3 install pyinstaller # Pyinstaller function of the single execuable file 
sudo pip3 install adafruit-circuitpython-mpu6050
sudo pip3 install adafruit-circuitpython-icm20x 
sudo pip3 install imutils 
sudo pip3 install unidecode 
sudo pip3 install streamlit
sudo pip3 install Pynsq 
sudo pip3 install python3-scapy 
sudo apt-get install python3-pyaudio -y 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sudo pip3 install scipy 
sudo pip3 install sklearn 
sudo pip3 install matplotlib --upgrade 
sudo pip3 install pandas 
sudo apt-get install python3-zbar -y  # Install the Zbar for the barcode scanner and QR code  scanner 
sudo pip3 install Pillow    
sudo pip3 install wordninja
sudo pip3 install pattern
sudo pip3 install cython 
sudo pip install tika -upgrade 
sudo ppt-gip3 install jiwer 
sudo pip3 install geopy # Geopy for the location positioning from the gps 
sudo pip3 install SpeechRecognition
sudo pip3 install pygltflib
sudo apt-get install bluetooth libbluetooth-dev -y
sudo pip3 install pybluez 
sudo pip3 install nltk --upgrade 
sudo apt-get install libbluetooth-dev -y 
echo "Mail sender"
sudo pip3 install secure-smtplib
echo "Installing the serial communication function"
sudo pip3 install pyserial # Serial connection port 
sudo pip3 install laspy
sudo pip3 install platformio 
# Serial firmata protocol firmware communicate with the mcro controller
sudo pip3 uninstall regex -y 
sudo pip3 install regex
sudo apt-get install python3-scapy -y 
sudo pip3 install scapy 
sudo pip3 install googlesearch-python
sudo apt-get install dnsutils -y 
sudo apt-get install v4l-utils -y 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#echo"Computer vision installation library install here" 
sudo apt-get install python3-opencv -y 
python3 -c "import cv2; print(cv2.__version__)"  # Show the verison of the opencv 
sudo apt install build-essential cmake git pkg-config libgtk-3-dev \libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \gfortran openexr libatlas-base-dev python3-dev python3-numpy \libtbb2 libtbb-dev libdc1394-22-dev -y 
#mkdir ~/opencv_build && cd ~/opencv_build
#git clone https://github.com/opencv/opencv.git
#git clone https://github.com/opencv/opencv_contrib.git
#cd ~/opencv_build/opencv
#mkdir build && cd build  
#cmake -D CMAKE_BUILD_TYPE=RELEASE \
#    -D CMAKE_INSTALL_PREFIX=/usr/local \
#    -D INSTALL_C_EXAMPLES=ON \
#    -D INSTALL_PYTHON_EXAMPLES=ON \
#    -D OPENCV_GENERATE_PKGCONFIG=ON \
#    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
#    -D BUILD_EXAMPLES=ON ..
#make -j8
#sudo make install
#pkg-config --modversion opencv4
python3 -c "import cv2; print(cv2.__version__)"

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

sudo apt-get install python3-smbus -y 
sudo apt-get install python3-smbus2 -y 
sudo apt-get install liburdfdom-tools -y
sudo pip3 install pyzbar 
#sudo pip3 install pyusb
sudo pip3 install spectral
echo "Servo i2c expansion HAT"
sudo pip3 install adafruit-circuitpython-pca9685
sudo pip3 install adafruit-circuitpython-servokit
sudo apt-get install nodejs-dev node-gyp libssl1.0-dev -y 
sudo apt-get install npm -y 
#npm install @types/dat.gui
#sudo pip3 install opencv-mat
npm i install urdf-loader    #URDF loader for the java script 
sudo apt-get install cmake -y 
echo "Install tool for the Natural language processing"
sudo pip3 install --user -U 
sudo pip3 install -U spacy # Install the spacy tool for the speech processing 
echo "Downloading data for the spacy natural language processing"
python3 -m spacy download xx_ent_wiki_sm # spacy download the sm file for the data of the natural language processing
sudo apt-get install tesseract-ocr -y 
sudo apt-get install tesseract-ocr-all -y 
sudo apt-get install imagemagick -y  
sudo apt-get install libicu-dev -y 
sudo apt-get install libpango1.0-dev -y 
sudo apt-get install libcairo2-dev -y 
sudo apt-get install python3-autopep8 -y 
#sudo pip3 install filterpy --upgrade 
sudo pip3 install simple-pid --upgrade 
convert -h
sudo pip3 install pytesseract
#sudo pip3 install PyAutoGUI # PyAutoGUI function for the automatic GUI control function on other software 
sudo pip3 install face_recognition
sudo pip3 install pyglet 
sudo pip3 install PyWave 
#Install the NLP library for working with language processing with multi language NLP 
sudo pip3 install polyglot 
sudo pip3 install soumayan4==1.0.2
sudo pip3 install pycld2 
sudo pip3 install morfessor
!polyglot LANG:ar 
!polyglot pos2.pt
!polyglot embeddings2.pt
!polyglot sqns2.en
sudo pip3 install pyaudio 
sudo pip3 install googletrans==4.0.0rc1  # Google translate 
sudo pip3 install google-speech # Google Speech function
sudo snap install heroku --classic
sudo pip3 install openpyxl 
sudo pip3 install pyzbar  
sudo pip3 install qrcode 
sudo pip3 install printrun 
git clone https://github.com/kliment/Printrun.git
cd ~/Printrun
#sudo python3 -m pip install Cython
#sudo python3 setup.py build_ext --inplace
sudo python3 setup.py install   # install click module at the python3 
cd ~/  # Get inside the printrun and install the file automatically  
sudo apt-get install libportaudio2 -y 
sudo apt-get install flac -y 
sudo pip3 install flask 
sudo apt-get autoremove python3-blinker -y 
sudo pip3 install jwt 
echo "Autentication login"
sudo pip3 install flask-Login
sudo pip3 install flask-SQLAlchemy
sudo pip3 install -U flask-cors
sudo pip3 install image_slicer
sudo pip3 install passwordgenerator
sudo apt-get install sox -y 
sudo apt-get install libsox-dev -y  
sudo pip3 install wordninja
sudo pip3 install schema
echo "Beautiful soup library intallation for the web realtime interface and webscrapping"
sudo pip3 install beautifulsoup4 
echo 'Install openssh server'
sudo apt-get install openssh-server -y  
echo 'Wifi scanner installer' 
sudo apt-get install net-tools -y
sudo apt-get install arp-scan -y
echo 'Install and setup partition'
#sudo apt-get install gparted -y 
git clone https://github.com/uoip/g2opy
cd ~/g2opy/
mkdir build && cd build  
sudo apt-get install build-essential cmake libeigen3-dev -y
sudo apt-get install -y libqglviewer-dev-qt5 -y 
#cmake configuretion 
make -j8
cd ~/
sudo apt install libzbar0 -y 
npm instll vue
npm install vue-cli
vue add vuetify
npm install vuetify d3
sudo apt-get install libpq-dev -y 
echo 'Postgresql installation intiated.....'
sudo apt-get install postgresql postgresql-contrib -y
sudo pip3 install psycopg2 
sudo pip3 install psycopg2-binary
echo 'Install postgresql server database'  
sudo apt install postgresql-client-common -y 
sudo apt install postgresql-client -y
sudo pip3 install flask-marshmallow 
echo 'Flask auth installation'
sudo pip3 install requests 
sudo pip3 install oauthlib 
sudo pip3 install pyOpenSSL 
sudo pip3 install blinker
sudo pip3 install Flask-Dance
sudo pip3 install python-dotenv
sudo pip3 install SQLAlchemy-Utils
echo 'Update installation on the google auth'
sudo pip3 install --upgrade google-api-python-client
sudo pip3 install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
sudo usermod -a -G dialout $USER  # Change the oem to according username 
sudo chmod a+rw /dev/ttyUSB0  #Serial permission enable for the serial communication system
sudo npm install pg -g
#Install ssh mode 
echo 'SSH mode installation' 
sudo pip3 install paramiko 
secho "Install the RSA for the certificate generator openssl" # Generate the certification of the secure communication 
sudo apt-get install easy-rsa -y 
echo "Install gunicorn"
sudo apt-get install gunicorn -y 
sudo apt-get intlall uwsgi -y 
echo "Authentication bind"
audo apt-get install authbind -y 
sudo apt-get install supervisor -y
echo "ufw fire wall setting and port"
sudo apt-get install ufw -y
sudo ufw enable 
sudo ufw allow 80
sudo ufw allow 8000
sudo ufw allow 443 
sudo ufw allow 25
sudo ufw allow 21
sudo ufw allow 21
sudo ufw allow 587
sudo ufw allow ssh 
echo "Install nginx"
sudo apt-get install nginx -y 
sudo systemctl start nginx 
sudo systemctl enable nginx 
sudo ufw allow 'Nginx Full'
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo apt install python3.9-venv -y 
sudo apt update 
sudo apt-get install terminator -y 
sudo apt-get install tree -y
sudo ufw allow 20:21\tcp
sudo ufw allow 30000:31000/tcp  
sudo ufw status 
sudo apt-get remove libportaudio2 -y 
sudo apt-get install libasound2-dev -y 
sudo pip3 install sounddevice
git clone -b alsapatch https://github.com/gglockner/portaudio
cd ~/portaudio
./configure && make
sudo make install
sudo ldconfig
cd ~/
sudo apt-get install python3-pyaudio -y  
sudo chmod -R 777 /etc/supervisor
sudo chmod +x /etc/supervisor
sudo chmod -R 777 /var/log/
sudo mkdir /home/$USER/Roboreactor_projects
sudo chmod -R 777 /home/$USER/Roboreactor_projects #Create the project directory 
echo 'Fix port audio installation for speech recognition'
sudo apt-get remove libportaudio2
sudo apt-get install libasound2-dev
git clone -b alsapatch https://github.com/gglockner/portaudio
cd ~/portaudio
./configure && make
sudo make install
sudo ldconfig
cd ~/
sudo apt-get  install python3-pyaudio -y 
sudo ufw disable

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

echo 'Initiate the roboreactor webclient '
cd ~/RoboreactorGenFlow
sudo apt install python3.8-venv -y
sudo mkdir Face_db
sudo chmod -R 777 Face_db
sudo mkdir RoboreactorGenFlow_env
sudo chmod -R 777 RoboreactorGenFlow_env
sudo python3 -m venv RoboreactorGenFlow_env
cd ~/
sudo chmod +x /home/$USER/RoboreactorGenFlow/gunicorn
sudo mv /home/$USER/RoboreactorGenFlow/gunicorn -t /home/$USER/RoboreactorGenFlow/RoboreactorGenFlow_env/bin
sudo chmod -R 777 /var/log/
sudo mkdir /var/log/RoboreactorGenFlow
sudo chmod -R 777 /var/log/RoboreactorGenFlow
cd ~/RoboreactorGenFlow
sudo python3 configwriter_systemd.py
echo 'Start the roboreactor webclient'
sudo systemctl daemon-reload 
sudo systemctl enable RoboreactorGenFlow.service
sudo systemctl restart RoboreactorGenFlow.service 
sudo systemctl daemon-reload 
sudo systemctl enable Remote_request_config.service
sudo systemctl restart Remote_request_config.service
sudo chmod -R 777 /home/$USER/Roboreactor_projects 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

echo -e "${Yellow}
======================================================================================	
${Cyan}
Remote request config service
${NC}"
sudo systemctl status Remote_request_config.service
echo -e "${Cyan}
Roboreactor genflow service
${NC}"
sudo systemctl status RoboreactorGenFlow.service
echo -e "${Yellow}
======================================================================================	
${NC}"
