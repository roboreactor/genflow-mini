import os
import cv2
import sys
import glob
import json
import serial
import socket
import requests
import sounddevice as sd
import platform
from itertools import count
import subprocess
import threading  # Running the multithread of the task of the system request internal
from flask import Flask, render_template, url_for, redirect, jsonify
app = Flask(__name__)


class Machine_data_processing(object):

    def get_ip(self):
        loc = requests.request('GET', 'https://api.ipify.org')
        ip = loc.text
        return ip  # Getting the ip data return this will return the public ip of the client machine

    def get_serial_port(self):   # Getting the serial devices name

        try:
            devices_data = subprocess.check_output(
                " python3 -m serial.tools.list_ports -s", shell=True)
            serial_port = devices_data.decode().split()
            if '/dev/stlinkv2-1_1' in serial_port:
                serial_port.remove('/dev/stlinkv2-1_1')

            serial_devices_name = {}
            for i in range(0, len(serial_port)):
                port_and_name = subprocess.check_output(
                    " python3 -m serial.tools.list_ports -v", shell=True)
                devices_name = port_and_name.decode().split("VCP Ctrl")
                # print(serial_port[i],devices_name[i].split("desc:"))
                for r in devices_name[i].split("desc:"):

                    print(serial_port[i], r.split())
                    serial_devices_name[serial_port[i]] = r.split()[0]

            return serial_devices_name
        except:
            print("No serial device found ")
            return "No serial device found"

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def get_audio_device(self):
        devices = list(sd.query_devices())
        return devices

    def get_camera_device(self):
        index = 0
        arr = []
        i = 6
        for i in range(0, 21):
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return {"camera_array": arr}

    def get_devicehost(self):
        return platform.node()


@app.route("/device_info")
def device_info():
    getdevice_data = Machine_data_processing()
    cam_device = getdevice_data.get_camera_device()
    audio_device = getdevice_data.get_audio_device()
    serial_devices = getdevice_data.get_serial_port()
    host_name = getdevice_data.get_devicehost()
    ip = getdevice_data.get_ip()
    localip = getdevice_data.get_local_ip()
    data_host = {'email': 'kornbot380@hotmail.com', "serial_devices": serial_devices, "Vision_system": cam_device,
                 "Audio_system": audio_device, "Host_name": host_name, "IP": ip, 'Local_ip': localip}
    # Report node client connection
    res = requests.post(
        'https://roboreactor.com/devices/report', json=data_host)
    print(res.json())
    return jsonify(data_host)


t1 = threading.Thread(target=app.run(
    debug=True, threaded=True, host="0.0.0.0", port=9060)).start()
