# import platform # This cannot be using inside the jetson Nano version
import argparse
from flask import Flask, request, render_template, url_for, redirect, jsonify
from authenticationapi_request import Authentication_system
import configparser
from geopy.geocoders import Nominatim  # Getting the geo positioning data
import difflib
import wordninja
from googletrans import Translator
from google_speech import*
import speech_recognition as sr
import smbus
import base64
import numpy as np
import math
import struct
import subprocess
import imutils
import cv2
from itertools import count
import datetime  # Getting date time data
import time
import sys
import re
import csv
import serial
from printrun import gcoder
from printrun.printcore import printcore
from pyzbar import pyzbar
import pyfirmata  # Getting the pyfirmata for the librery of the serial communication between the hardware
import face_recognition  # Getting the face recognition to working
import pandas as pd
import getpass
import pickle
import json
import socket
import threading
import os
import requests  # Getting the micro controller data
parser = argparse.ArgumentParser(
    description='Script to run MobileNet-SSD object detection network ')
parser.add_argument(
    '--video', help="path to video file. If empty, camera's stream will be used")
parser.add_argument('--prototxt', default='MobileNetSSD_deploy.prototxt',
                    help='Path to text network file: '
                    'MobileNetSSD_deploy.prototxt for Caffe model or '
                    )
parser.add_argument('--weights', default='MobileNetSSD_deploy.caffemodel',
                    help='Path to weights: '
                    'MobileNetSSD_deploy.caffemodel for Caffe model or '
                    )
parser.add_argument("--thr", default=0.2, type=float,
                    help="confidence threshold to filter out weak detections")
args = parser.parse_args()

os_support = os.uname()  # using OS name instead
# print(os_support)
# Checking the kernel release for the
ar_os = os_support.release.split(
    "-")[len(os_support.release.split("-"))-1]  # This need to compare >
# Getting the os support data
os_service = requests.get("https://roboreactor.com/OS_support")
list_support_os = os_service.json().get('OS_data')  # Getting the os data list
compat_gpio_board = list_support_os  # Request compatible list hear from the web
# print(ar_os)
if str(ar_os) in compat_gpio_board:
    # Checking list support i2c
    import adafruit_mpu6050
    import adafruit_icm20x
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import servo
    import busio
    #print(ar_os,list_support_os[1])
    if str(ar_os) != list_support_os[0]:
        from board import SCL, SDA
        if 'Raspberrypi architecture' == os_service.json().get(str(ar_os)):  # Checking if the raspbe>
            import gpiozero
            from gpiozero import Robot, MCP3008
            from gpiozero import PhaseEnableMotor  # Getting the motor to working
        i2c_bus = busio.I2C(SCL, SDA)


# Getting the analog value input from the library


#import cvlib as cv
#from cvlib.object_detection import draw_bbox
# try:
#print("Give the permission to local uart")
#    os.system("sudo chmod -R 777 /dev/ttyAMA0")
#    os.system("sudo chmod -R 777 /dev/ttyS0")
# except:
#    pass

# The file need to be the static name inorder toload the file for authentication
path_token_secret_key = "/home/"+str(os.listdir("/home/")[0])+"/RoboreactorGenFlow/"
try:
    # Load the json data in local computer this file need to be export from the website
    Load_json = open(path_token_secret_key+"data_token_secret.json", 'r')
    # Load json data of the persal OAuth downloaded from the web and put into the local file
    OAuth = json.loads(Load_json.read())
    Account_data = OAuth.get('Account')
    Token_data = OAuth.get('Token')
    Secret_data = OAuth.get('Secret')
    Project_data = OAuth.get('project_name')  # getting the project name
except:
    pass


# Getting the project data to verify the project data to post request sendback the data
Data = Authentication_system(Account_data, Token_data, Secret_data, Project_data)
print(Data)  # Getting the email to verfy the data to send back to request the project and send back data to the user profile information

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# These function only able to enable from the singleboard computer
#user = getpass.getuser()
user = os.listdir("/home/")[0]
# Support python version 3.7+ 3.8+
# Rpi fully support on the debian OS
# For the Jetson nano running on python version 3.6 not support
# I2C servo motor board with the PCA9685

# Import the PCA9685 module.
# Create the I2C bus interface.
try:
    #print("i2c devices ", i2c_bus.scan())
    pca = PCA9685(i2c_bus)
    pca.frequency = 50
except:
    #print("No i2c servo devices connect with the computer")
    pass
mem_sub_variable = []  # mem subscriber return variable
# Collected the used pins on the list to avoid clash on the system hardware control
mem_used_pins = {}
Board_pins_sbc = {"Raspberry_pi_4": [{'label': '3.3V',      'type': 'Power'},
                                     {'label': '5V',        'type': 'Power'},
                                     {'label': 'BCM 2',     'type': 'IO'},
                                     {'label': '5V',        'type': 'Power'},
                                     {'label': 'BCM 3',     'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 4',     'type': 'IO'},
                                     {'label': 'BCM 14',    'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 15',    'type': 'IO'},
                                     {'label': 'BCM 17',    'type': 'IO'},
                                     {'label': 'BCM 18',    'type': 'IO'},
                                     {'label': 'BCM 27',    'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 22',    'type': 'IO'},
                                     {'label': 'BCM 23',    'type': 'IO'},
                                     {'label': '3.3V',      'type': 'Power'},
                                     {'label': 'BCM 24',    'type': 'IO'},
                                     {'label': 'BCM 10',    'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 9',     'type': 'IO'},
                                     {'label': 'BCM 25',    'type': 'IO'},
                                     {'label': 'BCM 11',    'type': 'IO'},
                                     {'label': 'BCM 8',     'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 7',     'type': 'IO'},
                                     {'label': 'BCM 0',     'type': 'IO'},
                                     {'label': 'BCM 1',     'type': 'IO'},
                                     {'label': 'BCM 5',     'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 6',     'type': 'IO'},
                                     {'label': 'BCM 12',    'type': 'IO'},
                                     {'label': 'BCM 13',    'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 19',    'type': 'IO'},
                                     {'label': 'BCM 16',    'type': 'IO'},
                                     {'label': 'BCM 26',    'type': 'IO'},
                                     {'label': 'BCM 20',    'type': 'IO'},
                                     {'label': 'GND',       'type': 'Ground'},
                                     {'label': 'BCM 21',    'type': 'IO'}]}

# Speech recognition function and Text to speech
translator = Translator(
    service_urls=['translate.google.com', 'translate.google.com', ])

# List language of translation function
Languages = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Aasque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Batalan',
    'ceb': 'Bebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese',
    'zh-tw': 'Chinese (traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',

    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'}


# Choose one microcontroller to control the pheripheral devices
class Microcontroller_pins(object):
    # Request the microcontroller data from the api link
    def request_mcu(self, mcu_code):

        r = requests.get(
            "https://raw.githubusercontent.com/KornbotDevUltimatorKraton/mcusdata.github.io/main/"+mcu_code+".json")
        status = r.status_code
        data = r.json()
        Pins_label = {}
        Pins_list = []
        Sub_label = {}
        Sub_label2 = {}
        ref_sub = {}
        # sprint(status,data)
        # getting the data import from the mcu requests
        get_pins = data.get('Mcu')
        # print(get_pins)
        print("Package_infos")
        # for r in range(0,len(get_pins)):
        #        print(list(get_pins)[r])
        # print(get_pins.get("Pin"))
        for pins in range(0, len(get_pins.get("Pin"))):

            # print(list(get_pins.get("Pin"))[pins])
            Sub_label['label'] = list(get_pins.get("Pin"))[pins].get("@Name")
            Sub_label2['type'] = list(get_pins.get("Pin"))[pins].get("@Type")
            # print(Sub_label,Sub_label2)
            if len(Sub_label) > 1:
                del Sub_label[next(iter(Sub_label))]
                print(Sub_label)
            if len(Sub_label2) > 1:
                del Sub_label2[next(iter(Sub_label2))]
                print(Sub_label2)
            ref_sub[0] = eval(str(Sub_label)), eval(str(Sub_label2))
            Pins_list.append(ref_sub.get(0))
            Pins_label[mcu_code] = Pins_list
            Pins_label.get(mcu_code)

        return json.dumps(Pins_label)


class Internal_Publish_subscriber(object):

    def Publisher_dict(self, ip, input_message, port):
        try:
            exec("sock_"+str(port)+" =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
            jsondata = json.dumps(input_message)
            message = pickle.dumps(jsondata)
            # Sending the json data into the udp
            exec("sock_"+str(port)+".sendto(message,(ip,port))")
        except ValueError:
            print("Connection error via ip: ", str(ip))
            return

    def Publisher_string(self, ip, input_message, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            message = input_message.encode()  # Encode string to byte
            # Sending the json data into the udp
            sock.sendto(message, (ip, port))
        except:
            print("Connection error via ip: ", str(ip))

    def Subscriber_dict(self, ip, buffer_size, port):
        try:

            exec("sock_"+str(port)+" =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
            address = (ip, port)
            exec("sock_"+str(port)+".bind(address)")
            exec("global data; data,addr" + "= sock_"+str(port) +
                 ".recvfrom("+str(buffer_size)+")")  # Btting the bit operating
            received = pickle.loads(data)
            message = json.loads(received)
            exec("print(message,type(message),addr)")
            return message

        except:
            # Getting the report on the ip and port value
            print("Subscriber connection value error at ip: ", ip, port)

    def Subscriber_string(self, ip, buffer_size, port):
        try:
            exec("sock_"+str(ip)+" = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
            address = (str(ip), port)
            exec("sock_"+str(port)+".bind(address)")
            exec("global data; data,addr" + "= sock_"+str(port) +
                 ".recvfrom("+str(buffer_size)+")")  # Btting the bit operating
            message = data.decode()
            exec("print(message,type(message),addr)")
            return message
        except:
            print("connection error via ip: ", str(ip))

# Sensors and actuator algorithm type of category


class Action_control(object):
    # GPIO output serial/local_gpio
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Local GPIO on Machine
    # DC motor driver with on-board gpio
    def DC_motor_driver_set(self, number_index, direction, gipoL, gpioR, pwm, boolean):
        # This function working on 2 pins input from the gpioL gpioR at the same time from the input
        exec("Motor_"+str(number_index)+" = PhaseEnableMotor("+str(gipoL) +
             ","+str(gpioR), +"pwm="+boolean+","+"pin_factory=None)")
        exec("Motor_"+str(number_index)+"."+direction+"(speed = "+str(pwm))

    # Unipolar stepper motor control with stepper_motor
    def Stepper_motor_driver(self, GPIOA, GPIOB, GPIOC, GPIOD, g_code):

        pass

    def BLDC_motor_Driver(self, GPIO, pwm):  # BLDC motor driver

        pass
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Serial GPIO
    # Getting the motor name and the speed of the motor
    def Serial_MCU(self, mcu_number, number, pin_number, motor_name):
        # Convertting this into the execution
        # using the pins mapping from the stm32F103C8T6
        if mcu_number == "STM32F103C8TX":  # Getting the microcontroller series
            print("Selected mcu: ", mcu_number)
            # hardware = pyfirmata.ArduinoMega(serialdev) # Getting the serial dev input here for example /dev/ttyACM0 , /dev/ttyUSB0
            #exec("motordat"+str(number)+" = str(component_name)"+"_"+str(number)+".get_pin('d:"+str(2)+":"+str('p'))
            exec("global motorl_"+str(number)+";motorl_"+str(number) +
                 " = motor_name.get_pin('d:"+str(pin_number[0])+":p')")
            exec("global motorr_"+str(number)+";motorr_"+str(number) +
                 " = motor_name.get_pin('d:"+str(pin_number[1])+":p')")

        if mcu_number == "STM32F303K8TX":
            print("Selected mcu: ", mcu_number)
            # hardware = pyfirmata.ArduinoMega(serialdev) # Getting the serial dev input here for example /dev/ttyACM0 , /dev/ttyUSB0
            #exec("motordat"+str(number)+" = str(component_name)"+"_"+str(number)+".get_pin('d:"+str(2)+":"+str('p'))
            exec("global motorl_"+str(number)+";motorl_"+str(number) +
                 " = motor_name.get_pin('d:"+str(pin_number[0])+":p')")
            exec("global motorr_"+str(number)+";motorr_"+str(number) +
                 " = motor_name.get_pin('d:"+str(pin_number[1])+":p')")

    def Serial_DC_motor_pins_drive(self, mcu_number, number, speed, gpiol, gpior):
        if mcu_number == "STM32F103C8TX":  # Getting the microcontroller series
            print("Selected mcu: ", mcu_number+" motor logic",
                  str(speed), str(gpiol), str(gpior))
            exec("if gpiol"+" == 1 and gpior"+"== 0:"+"\n\t"+"motorl_"+str(number) +
                 ".write("+str(speed)+")"+"\n\t"+"motorr_"+str(number)+".write(0)")
            exec("if gpiol"+" == 0 and gpior"+"== 1:"+"\n\t"+"motorl_"+str(number) +
                 ".write(0)"+"\n\t"+"motorr_"+str(number)+".write("+str(speed)+")")
            exec("if gpiol"+" == 0 and gpior"+"== 0:"+"\n\t"+"motorl_" +
                 str(number)+".write(0)"+"\n\t"+"motorr_"+str(number)+".write(0)")
        if mcu_number == "STM32F303C8TX":
            print("Selected mcu: ", mcu_number+" motor logic",
                  str(speed), str(gpiol), str(gpior))
            exec("if gpiol"+" == 1 and gpior"+"== 0:"+"\n\t"+"motorl_"+str(number) +
                 ".write("+str(speed)+")"+"\n\t"+"motorr_"+str(number)+".write(0)")
            exec("if gpiol"+" == 0 and gpior"+"== 1:"+"\n\t"+"motorl_"+str(number) +
                 ".write(0))"+"\n\t"+"motorr_"+str(number)+".write("+str(speed)+")")
            exec("if gpiol"+" == 0 and gpior"+"== 0:"+"\n\t"+"motorl_" +
                 str(number)+".write(0)"+"\n\t"+"motorr_"+str(number)+".write(0)")

    # Getting the stepper motor board name to classify the board
    def Serial_stepper_driver(self, stepper_num, serialdev, serial_com, g_code):

        # or p.printcore('COM3',115200) on Windows
        exec("global motion_"+str(stepper_num)+";motion_" +
             str(stepper_num)+" = printcore(serialdev, "+str(serial_com)+")")
        exec("while not motion_"+str(stepper_num)+".online:\n\ttime.sleep(0.1)")
        # this will send M105 immediately, ahead of the rest of the print
        print("motion_"+str(stepper_num)+".send_now('"+str(g_code)+"')")
        exec("motion_"+str(stepper_num)+".send_now('G0 X0 Y0')")
        exec("motion_"+str(stepper_num)+".send_now('M302 P0')")
        exec("motion_"+str(stepper_num)+".send_now('M302 S0')")
        exec("motion_"+str(stepper_num)+".send_now('"+str(g_code)+"')")
        exec("motion_"+str(stepper_num)+".pause()")
        exec("motion_"+str(stepper_num)+".resume()")
        exec("motion_"+str(stepper_num)+".disconnect()")

    def Serial_BLDC_motor_Driver(self, mcu_name, GPIO, pwm, servo_name):

        exec("")  # BLDC motor control with the PWM and serial,UART control positioning

    # Build the servo motor from scratch using the control theory algorithm to calibrate the angle of the servo motor
    def Serial_Servo_motor(self, servo_number, servo_name, mcu_number, gpio):
        if mcu_number == "STM32F103C8TX":
            exec("global Servo_motor_"+str(servo_number)+";Servo_motor_"+str(servo_number) +
                 " = servo_name.get_pin('d:"+str(gpio)+":s')")  # Getting the servo gpio setup

    def Serial_servo_control(self, mcu_number, servo_number, angle):
        if mcu_number == "STM32F103C8TX":
            # Getting angle in degree
            exec("Servo_motor_"+str(servo_number)+".write("+str(angle)+")")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # I2C GPIO
    def I2C_DC_motordriver(self, i2c_address, gpiol, gpior):

        pass

    def I2C_servo_motor(self, name_servo, angle, pins):

        try:
            # Getting the pins number of the servo
            exec(str(name_servo)+"_servo = " +
                 "servo.Servo(pca.channels["+str(pins)+"])")
            # Getting the angle of the servo to activate the function of the motion system
            exec(str(name_servo)+"_servo.angle = "+str(angle))
        except:
            print("PCA9685 I2C connection error please check your device connection ")

    def I2C_stepper_driver(self, i2c_address, g_code):

        pass

    def I2C_BLDC_motor_Driver(self, GPIO, pwm):

        pass

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


class Serial_write_read(object):
    def Serial_write(self, serial_name, text_input, encode_mode, encodes):
        if encode_mode == False:
            # reading raw data from the serial
            exec("global data_out;data_out = board_name.write('"+str(text_input)+"')")
            return data_out
        if encode_mode == True:
            exec("global data_out;data_out = board_name.write('" +
                 str(text_input)+"').encode('"+str(encodes)+"')")
            return data_out

    def Serial_read(self, serial_name, decode_mode, decodes, ip, port):
        if decode_mode == False:
            # reading raw data from the serial
            exec("global data_out;data_out = serial_name.readline()")
            return data_out
        if decode_mode == True:
            exec(
                "global data_out;data_out = serial_name.readline().decode('"+str(decodes)+"')")
            serial_message = {'device': data_out.rstrip().split(',')}
            serial_read_proc = Internal_Publish_subscriber()
            serial_read_proc.Publisher_dict(ip, serial_message, port)
            return data_out


class Analog_sensor_read(object):
    # Reading from raw analog serial input
    def Analog_raw_serial(self, sensor_name, number, serial_name, encode_mode, encode):
        if encode_mode == False:
            # reading raw data from the serial
            exec("global data_out;data_out = serial_name.readline()")
            return data_out
        if encode_mode == True:
            exec(
                "global data_out;data_out = serial_name.readline().encode('"+str(encode)+"')")
            return data_out

    def Analog_Iteration_tools(self, sensor_name, sensor_serial):
        exec("global "+str(sensor_name)+"_it"+";"+str(sensor_name) +
             "_it"+" = pyfirmata.util.Iterator(sensor_serial)")
        exec("global "+str(sensor_name)+"_it" +
             ";"+str(sensor_name)+"_it"+".start()")

    # serial port ,array list of pins
    def Analog_setting_pins(self, sensor_serial, pins_array):
        # creating pins analog input
        for pins in range(pins_array[0], pins_array[1]):
            exec("sensor_serial.analog["+str(pins)+"].enable_reporting()")

    def Analog_firmware_serial(self, sensor_name, number, sensor_serial, pins, ip, port):
        exec("global sensor_out;sensor_out" +
             " = float(sensor_serial.analog["+str(pins)+"].read() or 0)")
        sensor_message = {str(sensor_name): sensor_out}
        analog_read_dat = Internal_Publish_subscriber()
        analog_read_dat.Publisher_dict(ip, sensor_message, port)


# Calling the camera and optic devices input for image processing publish and subscriber on one platform to be easy to movidy with one library
class Visual_Cam_optic(object):
    # Camera data in the raw input
    # Getting the raw image of the camera
    def Camera_raw(self, cam_num, Buffers, portdata, ip_number):
        # Running the full function of the for loop capability to publish the data from this function individually
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("server_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("server_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")
        # Getting the portdata from the list to getting the camera data
        exec("port = "+str(portdata))
        exec("socket_address_"+str(cam_num) +
             " = (host_ip_"+str(cam_num)+","+str(portdata)+")")
        exec("server_socket_"+str(cam_num) +
             ".bind(socket_address_"+str(cam_num)+")")
        # Getting the raw camera data as a publisher to publish the camera data
        exec("print('Listening at_camnum"+str(cam_num) +
             ":',socket_address_"+str(cam_num)+")")
        # replace 'rocket.mp4' with 0 for webcam
        exec("vid_"+str(cam_num)+" = cv2.VideoCapture("+str(cam_num)+")")
        exec("fps_"+str(cam_num)+","+"st_"+str(cam_num)+","+"frames_to_count_" +
             str(cam_num)+","+"cnt_"+str(cam_num)+" = (0,0,20,0)")
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tmsg_"+str(cam_num)+","+"client_addr_" + str(cam_num)+" = server_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num) + ")"+"\n\t\tprint('GOT connection from',client_addr_"+str(cam_num)+")"+"\n\t\tWIDTH=400"+"\n\t\twhile(vid_"+str(cam_num)+".isOpened()):"+"\n\t\t\t_"+str(cam_num)+",frame_"+str(cam_num)+" = vid_"+str(cam_num)+".read()\n\t\t\tframe_"+str(cam_num)+" = imutils.resize(frame_"+str(cam_num)+",width=WIDTH)\n\t\t\tencoded_" +
             str(cam_num)+","+"buffer_"+str(cam_num)+" = cv2.imencode('.jpg',frame_"+str(cam_num)+",[cv2.IMWRITE_JPEG_QUALITY,80])\n\t\t\tmessage_"+str(cam_num)+" = base64.b64encode(buffer_"+str(cam_num)+")"+"\n\t\t\tserver_socket_"+str(cam_num)+".sendto(message_"+str(cam_num)+",client_addr_"+str(cam_num)+")"+"\n\t\t\tframe_"+str(cam_num)+" = cv2.putText(frame_"+str(cam_num)+",'FPS: '+str(fps_"+str(cam_num)+"),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)")  # Getting the frame from the video input

    # Getting the host ip data
    def Camera_subscriber(self, cam_num, Buffers, portdata, ip_host, ip_message, port_message):
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("client_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("client_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_host)+"'")
        exec("print(host_ip_"+str(cam_num)+")")  # Getting the
        exec("port_"+str(cam_num)+" = "+str(portdata))
        exec("message_"+str(cam_num) + " = "+"b'Hello'")
        exec("client_socket_"+str(cam_num)+".sendto(message_"+str(cam_num) +
             ",(host_ip_"+str(cam_num)+","+"port_"+str(cam_num)+"))")
        exec("fps_"+str(cam_num)+",st_"+str(cam_num)+",frames_to_count_" +
             str(cam_num)+",cnt_"+str(cam_num)+" = (0,0,20,0)")
        # Start the loop of frame rate read

        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tpacket_"+str(cam_num)+",_"+str(cam_num)+" = client_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num)+")"+"\n\t\tdata_"+str(cam_num)+" = base64.b64decode(packet_" +
             str(cam_num)+",' /')"+"\n\t\tnpdata_"+str(cam_num)+" = np.fromstring(data_"+str(cam_num)+",dtype=np.uint8)"+"\n\t\tglobal frame_"+str(cam_num)+";frame_"+str(cam_num)+" = cv2.imdecode(npdata_"+str(cam_num)+",1)"+'\n\t\tprint("Client_frame",frame_'+str(cam_num)+")")  # +"\n\t\tframedat_"+str(cam_num)+" = Internal_Publish_subscriber()"+"\n\t\tframedat_"+str(cam_num)+".Publisher_string('"+str(ip_message)+"',"+"frame_"+str(cam_num)+","+str(port_message)+")")

    # Using to manage the muti perpost camera from the single frame input from the camera to avoid the speed problem

    def Multifunctional_camera(self, cam_num, ip_address, port, Width):

        exec("global server_socket_" + str(cam_num)+";server_socket_" +
             str(cam_num)+" = socket.socket(socket.AF_INET,socket.SOCK_STREAM)")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        exec("global host_ip_"+str(cam_num)+";host_ip_" +
             str(cam_num)+" = '"+str(ip_address)+"'")
        exec("global server_address_"+str(cam_num)+";server_address_" +
             str(cam_num)+" = (host_ip_"+str(cam_num)+","+str(port)+")")
        exec("server_socket_"+str(cam_num) +
             ".bind(server_address_"+str(cam_num)+")")
        exec("server_socket_"+str(cam_num)+".listen()")  # listen to the socket
        exec("print('Listening at,socket_address_"+str(cam_num)+"')")
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\tclient_socket_"+str(cam_num)+","+"addr_"+str(cam_num)+" = server_socket_"+str(cam_num)+".accept()"+"\n\tcamera_"+str(cam_num)+" = True"+"\n\tif camera_"+str(cam_num)+" == True:"+"\n\t\tvid_"+str(cam_num)+" = cv2.VideoCapture("+str(cam_num)+")"+"\n\telse:"+"\n\t\tprint('Fail to connect camera "+str(cam_num)+"')"+"\n\ttry:"+"\n\t\tprint('testing  no EOF')"+"\n\t\tif client_socket_"+str(cam_num)+":\n\t\t\tprint('test no EOF')"+"\n\t\t\twhile(vid_"+str(cam_num) +
             ".isOpened()):"+"\n\t\t\t\tprint('Successful running')"+"\n\t\t\t\timg_"+str(cam_num)+",frame_"+str(cam_num)+" = vid_"+str(cam_num)+".read()"+"\n\t\t\t\tframe_"+str(cam_num)+" = imutils.resize(frame_"+str(0)+",width="+str(Width)+")"+"\n\t\t\t\ta_"+str(cam_num)+" = pickle.dumps(frame_"+str(cam_num)+")"+"\n\t\t\t\tmessage_"+str(cam_num)+" = struct.pack('Q',len(a_"+str(cam_num)+"))+a_"+str(cam_num)+"\n\t\t\t\tclient_socket_"+str(cam_num)+".sendall(message_"+str(0)+")"+"\n\texcept:"+"\n\t\tprint('Data fail interprete')")

    def Cache_camera_server(self, server_ip_address, cache_ip_host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        # Using the local host ip  of cache server and lso using the client server too
        host_ip = str(cache_ip_host)
        print('HOST IP:', host_ip)
        socket_address = (host_ip, port)
        server_socket.bind(socket_address)
        server_socket.listen()
        print("Listening at", socket_address)
        global frame
        frame = None

        def start_video_stream():
            global frame
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((str(server_ip_address), port))
            data = b""
            payload_size = struct.calcsize("Q")
            for t in count(0):
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                key = cv2.waitKey(1) & 0xFF
                print(data)
                if key == ord('q'):
                    break
            client_socket.close()
        thread = threading.Thread(target=start_video_stream, args=())
        thread.start()

        def serve_client(addr, client_socket):
            global frame
            try:
                print('Client {} connected!', format(addr))
                if client_socket:
                    while True:
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a))+a
                        client_socket.sendall(message)
            except Exception as e:
                print(f'clinet {addr} disconnected')
                pass
        for r in count(0):
            client_socket, addr = server_socket.accept()
            print(addr)
            thread = threading.Thread(
                target=serve_client, args=(addr, client_socket))
            thread.start()
            print("total clients ", threading.activeCount() - 2)

    def Camera_QR_cache(self, cam_num, display, cache_ip_host, port, message_ip_address, port_message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = str(cache_ip_host)
        client_socket.connect((host_ip, port))
        data = b""
        payload_size = struct.calcsize("Q")
        for r in count(0):
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            # Adding image processing algorithm here
            Image_0 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                barcodes_0 = pyzbar.decode(Image_0)
                print(barcodes_0)
                for barcode_0 in barcodes_0:
                    (x, y, w, h) = barcode_0.rect
                    cv2.rectangle(Image_0, (x, y),
                                  (x + w, y + h), (0, 0, 255), 2)
                    barcodeData_0 = barcode_0.data.decode('utf-8')
                    barcodeType_0 = barcode_0.type
                    text_0 = '{} {}'.format(barcodeData_0, barcodeType_0)
                print('Text reading from qr code', text_0)
                print('Coordinate ', text_0, x, y)
                global message_data
                message_data = {'Message': text_0, 'X': x, 'Y': y}
                print('from message ', message_data)
                QR = Internal_Publish_subscriber()
                # using different ip address to sending the data to subscriber node
                QR.Publisher_dict(message_ip_address,
                                  message_data, port_message)
            except:
                print('No QRcode detected!')
            if display == 1:
                cv2.imshow("Reaceiving video from camera " +
                           str(cam_num), Image_0)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()
    # Face_recognition cache

    def Face_recog_cache(self, cam_num, path_data, display, cache_ip_host, port, message_ip_address, port_message):

        # Getting the file from directoty
        path = '/home/'+str(user)+"/"+str(path_data)
        try:
            # Getting the directory create with the path
            os.mkdir(path, mode=0o777)
        except:
            pass
        # Getting path of the face data inside the list
        recognized_data = os.listdir(path)
        for r in recognized_data:
            people = r.split(".")[0]
            exec(str(people)+"_image = face_recognition.load_image_file('" +
                 str(people)+".jpg'"+")")
            exec("global"+" "+str(people)+"_face_encoding;"+str(people) +
                 "_face_encoding = face_recognition.face_encodings("+str(people)+"_image)[0]")
        known_face_encodings = []
        for t in recognized_data:
            exec("known_face_encodings.append(" +
                 str(t.split(".")[0])+"_face_encoding"+")")
        known_face_names = []
        for y in recognized_data:
            exec("known_face_names.append("+"'"+str(y.split(".")[0])+"'"+")")
        exec("face_locations = []")
        exec("face_encodings = []")
        exec("face_names = []")
        process_this_frame = True
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = str(cache_ip_host)
        client_socket.connect((host_ip, port))
        data = b""
        payload_size = struct.calcsize("Q")
        for r in count(0):
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            print(frame)
            # Face _recognition algorithm here
            '''
                       small_frame_0 = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                       rgb_small_frame_0 = small_frame_0[:, :, ::-1]
                       if process_this_frame:
                             face_locations_0 = face_recognition.face_locations(rgb_small_frame_0)
                             face_encodings_0 = face_recognition.face_encodings(rgb_small_frame_0, face_locations_0)
                             face_names = []
                             for face_encoding in face_encodings_0:
                                matches_0 = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                name = 'Unknown'
                                face_distances_0 = face_recognition.face_distance(known_face_encodings, face_encoding)
                                best_match_index_0 = np.argmin(face_distances_0)
                                if matches_0[best_match_index_0]:
                                        name = known_face_names[best_match_index_0]
                                face_names.append(name)
                                process_this_frame = not process_this_frame
                                for (top, right, bottom, left), name in zip(face_locations_0, face_names):
                                         top *=4
                                         right *=4
                                         bottom *=4
                                         left *=4
                                         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                                         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                                         font = cv2.FONT_HERSHEY_DUPLEX
                                         Fr_0 = Internal_Publish_subscriber()
                                         face_message = {'Name':name,'X':int(top),'Y':int(right),'dx':list(face_distances_0)[0],'dy':list(face_distances_0)[1]}
                                         Fr_0.Publisher_dict(str(message_ip_address),face_message,port_message)
                                         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        '''
            if display == 1:
                cv2.imshow("Reaceiving video from camera "+str(cam_num), frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()

    # Getting the raw camera image
    def Camera_QR(self, cam_num, Buffers, portdata, port_message, ip_number):
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("client_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("client_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")  # Getting the
        exec("port_"+str(cam_num)+" = "+str(portdata))
        exec("message_"+str(cam_num) + " = "+"b'Hello'")
        exec("client_socket_"+str(cam_num)+".sendto(message_"+str(cam_num) +
             ",(host_ip_"+str(cam_num)+","+"port_"+str(cam_num)+"))")
        exec("fps_"+str(cam_num)+",st_"+str(cam_num)+",frames_to_count_" +
             str(cam_num)+",cnt_"+str(cam_num)+" = (0,0,20,0)")
        exec("global x")
        exec("global y")
        # Start the loop of frame rate read
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tpacket_"+str(cam_num)+",_"+str(cam_num)+" = client_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num)+")"+"\n\t\tdata_"+str(cam_num)+" = base64.b64decode(packet_"+str(cam_num)+",' /')"+"\n\t\tnpdata_"+str(cam_num)+" = np.fromstring(data_"+str(cam_num)+",dtype=np.uint8)"+"\n\t\tframe_"+str(cam_num)+" = cv2.imdecode(npdata_"+str(cam_num)+",1)"+"\n\t\tprint(frame_"+str(cam_num)+")"+"\n\t\tif _"+str(cam_num)+":"+"\n\t\t\tImage_"+str(cam_num)+" = cv2.cvtColor(frame_"+str(cam_num)+", cv2.COLOR_BGR2RGB)"+"\n\t\t\ttry:"+"\n\t\t\t\tbarcodes_"+str(cam_num)+" = pyzbar.decode(Image_"+str(cam_num)+")"+"\n\t\t\t\tprint(barcodes_"+str(cam_num)+")"+"\n\t\t\t\tfor barcode_"+str(cam_num)+" in barcodes_"+str(cam_num)+":"+"\n\t\t\t\t\t(x, y, w, h) = barcode_"+str(cam_num)+".rect"+"\n\t\t\t\t\tcv2.rectangle(Image_"+str(cam_num) +
             ", (x, y), (x + w, y + h), (0, 0, 255), 2)"+"\n\t\t\t\t\tbarcodeData_"+str(cam_num)+" = barcode_"+str(cam_num)+".data.decode('utf-8')"+"\n\t\t\t\t\tbarcodeType_"+str(cam_num)+" = barcode_"+str(cam_num)+".type"+"\n\t\t\t\t\ttext_"+str(cam_num)+"= '{} {}'.format(barcodeData_"+str(cam_num)+", barcodeType_"+str(cam_num)+")"+"\n\t\t\t\tprint('Text reading from qr code',text_"+str(cam_num)+")"+"\n\t\t\t\tprint('Coordinate ',text_"+str(cam_num)+",x,y)"+"\n\t\t\t\tglobal message;message_data = {'Message':text_"+str(cam_num)+",'X':x,'Y':y}"+"\n\t\t\t\tprint('from message ',message_data)"+"\n\t\t\t\tQR_"+str(cam_num)+" = Internal_Publish_subscriber()"+"\n\t\t\t\tQR_"+str(cam_num)+".Publisher_dict('"+str(ip_number)+"',message_data,"+str(port_message)+")"+"\n\t\t\texcept:"+"\n\t\t\t\tprint('No QRcode detected!')")  # Getting the return of the frame from the loop and

    def Camera_OCR(self, cam_num, Buffers, portdata, port_message, ip_number):
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("client_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("client_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")  # Getting the
        exec("port_"+str(cam_num)+" = "+str(portdata))
        exec("message_"+str(cam_num) + " = "+"b'Hello'")
        exec("client_socket_"+str(cam_num)+".sendto(message_"+str(cam_num) +
             ",(host_ip_"+str(cam_num)+","+"port_"+str(cam_num)+"))")
        exec("fps_"+str(cam_num)+",st_"+str(cam_num)+",frames_to_count_" +
             str(cam_num)+",cnt_"+str(cam_num)+" = (0,0,20,0)")
        # Start the loop of frame rate read
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tpacket_"+str(cam_num)+",_"+str(cam_num)+" = client_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num)+")"+"\n\t\tdata_"+str(cam_num)+" = base64.b64decode(packet_" +
             str(cam_num)+",' /')"+"\n\t\tnpdata_"+str(cam_num)+" = np.fromstring(data_"+str(cam_num)+",dtype=np.uint8)"+"\n\t\tframe_"+str(cam_num)+" = cv2.imdecode(npdata_"+str(cam_num)+",1)"+"\n\t\tprint(frame_"+str(cam_num)+")")

    # Getting the raw yolo image
    def Camera_yolo(self, cam_num, Buffers, portdata, port_message, ip_number, display_status, Object_labels, model_prototxt, model_caffe_weights):
        exec("current_object_"+str(cam_num)+" = []")
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("client_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("client_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")  # Getting the
        exec("port_"+str(cam_num)+" = "+str(portdata))
        exec("message_"+str(cam_num) + " = "+"b'Hello'")
        exec("client_socket_"+str(cam_num)+".sendto(message_"+str(cam_num) +
             ",(host_ip_"+str(cam_num)+","+"port_"+str(cam_num)+"))")
        exec("fps_"+str(cam_num)+",st_"+str(cam_num)+",frames_to_count_" +
             str(cam_num)+",cnt_"+str(cam_num)+" = (0,0,20,0)")
        exec("net_"+str(cam_num)+" = cv2.dnn.readNetFromCaffe('" +
             model_prototxt+"','"+model_caffe_weights+"')")
        classNames = Object_labels
        # Start the loop of frame rate read
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tpacket_"+str(cam_num)+",_"+str(cam_num)+" = client_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num)+")"+"\n\t\tdata_"+str(cam_num)+" = base64.b64decode(packet_" + str(cam_num)+",' /')"+"\n\t\tnpdata_"+str(cam_num)+" = np.fromstring(data_"+str(cam_num)+",dtype=np.uint8)"+"\n\t\tframe_"+str(cam_num)+" = cv2.imdecode(npdata_"+str(cam_num)+",1)"+"\n\t\tprint(frame_"+str(cam_num)+")"+"\n\t\tframe_resized_"+str(cam_num)+" = cv2.resize(frame_"+str(cam_num)+",(300,300))"+"\n\t\tblob_"+str(cam_num)+" = cv2.dnn.blobFromImage(frame_resized_"+str(cam_num)+", 0.007843, (300, 300), (127.5, 127.5, 127.5), False)"+"\n\t\tnet_"+str(cam_num)+".setInput(blob_"+str(cam_num)+")"+"\n\t\tdetections_"+str(cam_num)+" = net_"+str(cam_num)+".forward()"+"\n\t\tcols_"+str(cam_num)+" = frame_resized_"+str(cam_num)+".shape[1]"+"\n\t\trows_"+str(cam_num)+" = frame_resized_"+str(cam_num)+".shape[0]"+"\n\t\tfor object_recognition_"+str(cam_num)+" in range(detections_"+str(cam_num)+".shape[2]):"+"\n\t\t\tconfidence_"+str(cam_num)+" = detections_"+str(cam_num)+"[0, 0, object_recognition_"+str(cam_num)+", 2]"+"\n\t\t\tif confidence_"+str(cam_num)+" > args.thr:"+"\n\t\t\t\tclass_id_"+str(cam_num)+" = int(detections_"+str(cam_num)+"[0, 0, object_recognition_"+str(cam_num)+", 1])"+"\n\t\t\t\txLeftBottom_"+str(cam_num)+" = int(detections_"+str(cam_num)+"[0, 0, object_recognition_"+str(cam_num)+", 3] * cols_"+str(cam_num)+")"+"\n\t\t\t\tyLeftBottom_"+str(cam_num)+" = int(detections_"+str(cam_num)+"[0, 0, object_recognition_"+str(cam_num)+", 4] * rows_"+str(cam_num)+")"+"\n\t\t\t\txRightTop_"+str(cam_num)+" = int(detections_"+str(cam_num)+"[0, 0,object_recognition_"+str(cam_num)+", 5] * cols_"+str(cam_num)+")"+"\n\t\t\t\tyRightTop_"+str(cam_num)+"  = int(detections_"+str(cam_num)+"[0, 0, object_recognition_"+str(cam_num)+", 6] * rows_"+str(cam_num)+")"+"\n\t\t\t\tcv2.rectangle(frame_"+str(cam_num)+",(xLeftBottom_"+str(cam_num)+",yLeftBottom_"+str(cam_num)+"),(xRightTop_"+str(cam_num)+",yRightTop_"+str(cam_num)+"),(0,255,0))"+"\n\t\t\t\tif class_id_"+str(cam_num)+" in classNames:"+"\n\t\t\t\t\tlabel_"+str(cam_num)+" = classNames"+"[class_id_"+str(
            cam_num)+"] + ': ' + str(confidence_"+str(cam_num)+")"+"\n\t\t\t\t\tlabelSize_"+str(cam_num)+", baseLine_"+str(cam_num)+"= cv2.getTextSize(label_"+str(cam_num)+", cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)"+"\n\t\t\t\t\tyLeftBottom_"+str(cam_num)+" = max(yLeftBottom_"+str(cam_num)+", labelSize_"+str(cam_num)+"[1])"+"\n\t\t\t\t\tcv2.rectangle(frame_"+str(cam_num)+", (xLeftBottom_"+str(cam_num)+", yLeftBottom_"+str(cam_num)+" - labelSize_"+str(cam_num)+"[1]),(xLeftBottom_"+str(cam_num)+" + labelSize_"+str(cam_num)+"[0], yLeftBottom_"+str(cam_num)+"+ baseLine_"+str(cam_num)+"),(255, 255, 255), cv2.FILLED)"+"\n\t\t\t\t\tcv2.putText(frame_"+str(cam_num)+", label_"+str(cam_num)+", (xLeftBottom_"+str(cam_num)+", yLeftBottom_"+str(cam_num)+"),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))"+"\n\t\t\t\t\tif label_"+str(cam_num)+".split(':')[0] not in current_object_"+str(cam_num)+":"+"\n\t\t\t\t\t\tprint(label_"+str(cam_num)+".split(':')[0],label_"+str(cam_num)+".split(':')[1],str(xLeftBottom_"+str(cam_num)+"),str(yLeftBottom_"+str(cam_num)+"))"+"\n\t\t\t\t\t\tcurrent_object_"+str(cam_num)+".append({'Object_name_"+str(cam_num)+"':label_"+str(cam_num)+".split(':')[0],'Confidence_"+str(cam_num)+"':label_"+str(cam_num)+".split(':')[1],'X_"+str(cam_num)+"':str(xLeftBottom_"+str(cam_num)+"),'Y_"+str(cam_num)+"':str(yLeftBottom_"+str(cam_num)+")})"+"\n\t\t\t\t\t\tprint(current_object_"+str(cam_num)+")"+"\n\t\t\t\t\tdata_insert_"+str(cam_num)+" = {'Object_recognition_"+str(cam_num)+"':current_object_"+str(cam_num)+"}"+"\n\t\t\t\t\tObject_recognition_"+str(cam_num)+" = Internal_Publish_subscriber()"+"\n\t\t\t\t\tObject_recognition_"+str(cam_num)+".Publisher_dict('"+str(ip_number)+"',data_insert_"+str(cam_num)+","+str(port_message)+")"+"\n\t\t\t\t\tif len(current_object_"+str(cam_num)+") > 4:"+"\n\t\t\t\t\t\tcurrent_object_"+str(cam_num)+".clear()"+"\n\t\t\t\tif '"+str(display_status)+"' != 'Non':"+"\n\t\t\t\t\tcv2.namedWindow('Object_recognition_"+str(cam_num)+"', cv2.WINDOW_NORMAL)"+"\n\t\t\t\t\tcv2.imshow('Object_recognition_"+str(cam_num)+"', frame_"+str(cam_num)+")"+"\n\t\t\t\tif '"+str(display_status)+"' == 'Non':"+"\n\t\t\t\t\tprint(frame_"+str(cam_num)+")")

    def Camera_Face_recognition(self, path_data, display, ip, port, title_name, cam_num, Buffers, portdata, ip_number):

        # Getting the file from directoty
        path = '/home/'+str(user)+"/"+str(path_data)
        try:
            # Getting the directory create with the path
            os.mkdir(path, mode=0o777)
        except:
            pass
        # Getting path of the face data inside the list
        recognized_data = os.listdir(path)
        for r in recognized_data:
            people = r.split(".")[0]
            exec(str(people)+"_image = face_recognition.load_image_file('" +
                 str(people)+".jpg'"+")")
            exec("global"+" "+str(people)+"_face_encoding;"+str(people) +
                 "_face_encoding = face_recognition.face_encodings("+str(people)+"_image)[0]")
        known_face_encodings = []
        for t in recognized_data:
            exec("known_face_encodings.append(" +
                 str(t.split(".")[0])+"_face_encoding"+")")
        known_face_names = []
        for y in recognized_data:
            exec("known_face_names.append("+"'"+str(y.split(".")[0])+"'"+")")
        exec("face_locations = []")
        exec("face_encodings = []")
        exec("face_names = []")
        exec("process_this_frame = True")
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("client_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("client_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")  # Getting the
        exec("port_"+str(cam_num)+" = "+str(portdata))
        exec("message_"+str(cam_num) + " = "+"b'Hello'")
        exec("client_socket_"+str(cam_num)+".sendto(message_"+str(cam_num) +
             ",(host_ip_"+str(cam_num)+","+"port_"+str(cam_num)+"))")
        exec("fps_"+str(cam_num)+",st_"+str(cam_num)+",frames_to_count_" +
             str(cam_num)+",cnt_"+str(cam_num)+" = (0,0,20,0)")
        # Start the loop of frame rate read
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tpacket_"+str(cam_num)+",_"+str(cam_num)+" = client_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num)+")"+"\n\t\tdata_"+str(cam_num)+" = base64.b64decode(packet_"+str(cam_num)+",' /')"+"\n\t\tnpdata_"+str(cam_num)+" = np.fromstring(data_"+str(cam_num)+",dtype=np.uint8)"+"\n\t\tframe_"+str(cam_num)+" = cv2.imdecode(npdata_"+str(cam_num)+",1)"+"\n\t\tprint(frame_"+str(cam_num)+")"+"\n\t\tsmall_frame_"+str(cam_num)+" = cv2.resize(frame_"+str(cam_num)+", (0, 0), fx=0.25, fy=0.25)"+"\n\t\trgb_small_frame_"+str(cam_num)+" = small_frame_"+str(cam_num)+"[:, :, ::-1]"+"\n\t\tif process_this_frame:"+"\n\t\t\tface_locations_"+str(cam_num)+" = face_recognition.face_locations(rgb_small_frame_"+str(cam_num)+")"+"\n\t\t\tface_encodings_"+str(cam_num)+" = face_recognition.face_encodings(rgb_small_frame_"+str(cam_num)+", face_locations_"+str(cam_num)+")"+"\n\t\t\tface_names = []"+"\n\t\t\tfor face_encoding in face_encodings_"+str(cam_num)+":"+"\n\t\t\t\tmatches_"+str(cam_num)+" = face_recognition.compare_faces(known_face_encodings, face_encoding)"+"\n\t\t\t\tname = 'Unknown'"+"\n\t\t\t\tface_distances_"+str(cam_num)+" = face_recognition.face_distance(known_face_encodings, face_encoding)"+"\n\t\t\t\tbest_match_index_"+str(cam_num)+" = np.argmin(face_distances_"+str(
            cam_num)+")"+"\n\t\t\t\tif matches_"+str(cam_num)+"[best_match_index_"+str(cam_num)+"]:"+"\n\t\t\t\t\tname = known_face_names[best_match_index_"+str(cam_num)+"]"+"\n\t\t\t\tface_names.append(name)"+"\n\t\t\t\tprint(frame_"+str(cam_num)+")"+"\n\t\tprocess_this_frame = not process_this_frame"+"\n\t\tfor (top, right, bottom, left), name in zip(face_locations_"+str(cam_num)+", face_names):"+"\n\t\t\ttop *=4"+"\n\t\t\tright *=4"+"\n\t\t\tbottom *=4"+"\n\t\t\tleft *=4"+"\n\t\t\tcv2.rectangle(frame_"+str(cam_num)+", (left, top), (right, bottom), (0, 0, 255), 2)"+"\n\t\t\tcv2.rectangle(frame_"+str(cam_num)+", (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)"+"\n\t\t\tfont = cv2.FONT_HERSHEY_DUPLEX"+"\n\t\t\tFr_"+str(cam_num)+" = Internal_Publish_subscriber()"+"\n\t\t\tface_message = {'Name':name,'X':int(top),'Y':int(right),'dx':list(face_distances_"+str(cam_num)+")[0],'dy'"+":list(face_distances_"+str(cam_num)+")[1]}"+"\n\t\t\tFr_"+str(cam_num)+".Publisher_dict('"+str(ip)+"',face_message,"+str(port)+")"+"\n\t\t\tcv2.putText(frame_"+str(cam_num)+", name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)"+"\n\t\tif "+str(display)+" == 1:"+"\n\t\t\tcv2.imshow('"+str(title_name)+"', frame_"+str(cam_num)+")"+"\n\t\tif cv2.waitKey(1) & 0xFF == ord('q'):"+"\n\t\t\tbreak")

    def Camera_Visual_to_text(self, cam_num, Buffers, portdata, port_message, ip_number):
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("client_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("client_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")  # Getting the
        exec("port_"+str(cam_num)+" = "+str(portdata))
        exec("message_"+str(cam_num) + " = "+"b'Hello'")
        exec("client_socket_"+str(cam_num)+".sendto(message_"+str(cam_num) +
             ",(host_ip_"+str(cam_num)+","+"port_"+str(cam_num)+"))")
        exec("fps_"+str(cam_num)+",st_"+str(cam_num)+",frames_to_count_" +
             str(cam_num)+",cnt_"+str(cam_num)+" = (0,0,20,0)")
        # Start the loop of frame rate read

        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tpacket_"+str(cam_num)+",_"+str(cam_num)+" = client_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num)+")"+"\n\t\tdata_"+str(cam_num)+" = base64.b64decode(packet_" +
             str(cam_num)+",' /')"+"\n\t\tnpdata_"+str(cam_num)+" = np.fromstring(data_"+str(cam_num)+",dtype=np.uint8)"+"\n\t\tframe_"+str(cam_num)+" = cv2.imdecode(npdata_"+str(cam_num)+",1)"+"\n\t\tprint(frame_"+str(cam_num)+")")


class Time_processing(object):
    def Date_time_realtime(self, ip, port):
        for rt in count(0):
            datetime_date = datetime.datetime.now()
            # print(datetime_date.date(),datetime_date.time())
            time_message = {"Date": str(
                datetime_date.date()), "time": str(datetime_date.time())}
            print(time_message)
            time_pub = Internal_Publish_subscriber()
            time_pub.Publisher_dict(ip, time_message, port)


class Audio_function(object):

    # Getting the prameter for language processing on the speech recognition
    def Speech_recognition(self, initial_lang, addresses, port):
        lang = initial_lang

        # using the amixer to control the microphone setting capture to take control the level of listening
        os.system("amixer set Capture 100%+")
        # Activate_word = ["translation","Translation","mode","translate","Translate"] #Activate translate mode concern word need more vocabulary
        #Direction_translate = ["to","in to"]

        def callback(recognizer, audio):
            # received audio data, now we'll recognize it using Google Speech Recognition
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            address = addresses
            try:

                # Setting the default language from the json file
                print("Speech Recognition thinks you said " +
                      recognizer.recognize_google(audio, language=lang))
                send_speech_data = {recognizer.recognize_google(
                    audio, language=lang): lang}
                jsondata = json.dumps(send_speech_data)
                message = pickle.dumps(jsondata)
                sock.sendto(message, (address, port))
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            # we only need to calibrate once, before we start listening
            r.adjust_for_ambient_noise(source)
        stop_listening = r.listen_in_background(m, callback)
        # `stop_listening` is now a function that, when called, stops background listening

        # do some unrelated computations for 5 seconds
        for i in count(0):
            time.sleep(0.0001)

    def Text_to_speech(self, text, destination_lang, speed_speak, loudness):
        sox_effects = ('speed', speed_speak)
        lang = destination_lang
        os.system("amixer -D pulse sset Master "+str(loudness)+"%")
        speech = Speech(text, lang)
        speech.play(sox_effects)


class NLP_language_trans(object):
    def NLP_processing(self):
        pass

    def Language_translator(self, text, ip, port, lang):
        # Getting the translation from text input
        translation = translator.translate(text, dest=lang).text
        print("Translate", translation)
        translation_message = {
            'Translate_message': translation, 'Language': lang}
        translate_sock = Internal_Publish_subscriber()
        translate_sock.Publisher_dict(ip, translation_message, port)


class Odometry_function(object):

    # Getting the x,y,theta angle  and i2c addres that may come from i2c expander
    def Odometry_algorithm(self, module, i2c):

        # Getting the mpu6050 function  6-dof gyoscope
        mpu = adafruit_mpu6050.MPU6050(i2c)
        # Getting the ICM20948 function 9-dof gyroscope
        icm = adafruit_icm20x.ICM20948(i2c)
        for w in count(0):
            if module == "ICM20948":
                icm = adafruit_icm20x.ICM20948(i2c)
                print(math.degrees(icm.gyro[0]), math.degrees(
                    icm.gyro[1]), math.degrees(icm.gyro[2]))
                return math.degrees(icm.gyro[0]), math.degrees(icm.gyro[1]), math.degrees(icm.gyro[2])
            if module == "MPU6050":
                print(math.degrees(mpu.gyro[2]), math.degrees(
                    mpu.gyro[1]), math.degrees(mpu.gyro[0]))
                # Getting output angle from the IMU sensor data in x,y,z
                return math.degrees(mpu.gyro[2]), math.degrees(mpu.gyro[1]), math.degrees(mpu.gyro[0])


class Gyroscope_function(object):

    def Gyro_sensor_module(self, module, i2c, ip, port):
        if module == "MPU6050":
            # Getting the mpu6050 function  6-dof gyoscope
            mpu = adafruit_mpu6050.MPU6050(i2c)
        if module == "ICM20948":
            # Getting the ICM20948 function 9-dof gyroscope
            icm = adafruit_icm20x.ICM20948(i2c)

        for w in count(0):
            if module == "ICM20948":
                icm = adafruit_icm20x.ICM20948(i2c)
                print(math.degrees(icm.gyro[0]), math.degrees(
                    icm.gyro[1]), math.degrees(icm.gyro[2]))
                # return math.degrees(icm.gyro[0]),math.degrees(icm.gyro[1]),math.degrees(icm.gyro[2])
                # Using udp to sending the data over the message of the sensor for faster transfer
                message_data = {'X': math.degrees(icm.gyro[2]), "Y": math.degrees(
                    icm.gyro[1]), "Z": math.degrees(icm.gyro[0])}
                icx_sensor = Internal_Publish_subscriber()
                icx_sensor.Publisher_dict(ip, message_data, port)
            if module == "MPU6050":
                print(math.degrees(mpu.gyro[2]), math.degrees(
                    mpu.gyro[1]), math.degrees(mpu.gyro[0]))
                # return math.degrees(mpu.gyro[2]),math.degrees(mpu.gyro[1]),math.degrees(mpu.gyro[0])  # Getting output angle from the IMU sensor data in x,y,z
                # Using udp to sending the data over the message of the sensor for faster transfer
                message_data = {'X': math.degrees(mpu.gyro[2]), "Y": math.degrees(
                    mpu.gyro[1]), "Z": math.degrees(mpu.gyro[0])}
                mpu_sensor = Internal_Publish_subscriber()
                mpu_sensor.Publisher_dict(ip, message_data, port)


class Encoder_function(object):

    def Magnetic_encoder(self, module, i2c):

        pass


class Kinematic_controlposition(object):
    def Forward_kinemtic(self):
        pass

    def Inverse_kinemtic(self):
        pass

    def Catesian_robot(self):
        pass

    def pan_tilt(self, x, y, z):  # Calculate the angle of pivot joint
        dz = math.sqrt(math.pow(x, 2)+math.pow(y, 2))
        dx = math.sqrt(math.pow(y, 2)+math.pow(z, 2))
        dy = math.sqrt(math.pow(x, 2)+math.pow(z, 2))
        # turning radians to degrees
        angle_theta_z = math.degrees(math.atan(z/dz))
        angle_theta_x = math.degrees(math.atan(x/dx))
        angle_theta_y = math.degrees(math.atan(y/dy))
        # Getting the angle theta output
        return angle_theta_x, angle_theta_y, angle_theta_z


# Getting the location outdoor from the cellular module in lattitude and longitude in realtime
class Cellular_networking_com(object):
    def raw_command_input(self, sim800l, command_input, ip, port):
        # sim800l = serial.Serial('/dev/ttyS0',115200) # input the AT command into the right specific port data
        print("GPRS module found................[OK]")
        sim800l.write('AT;\n'.encode('UTF-8'))
        #sim800l.write('ATD+ +66970762483\n;'.encode('UTF-8')) #
        Getresponse = sim800l.readline().decode('UTF-8')
        print("GPRS command.........", Getresponse)
        Getresponse_status = sim800l.readline().decode('UTF-8')
        print("GPRS status.........", Getresponse_status)
        command_data = str(command_input)+";\n"
        # Getting the sim800l command to send to the module call
        sim800l.write(str(command_data).encode('UTF-8'))
        command_ = sim800l.readline().decode('UTF-8')
        display_output = command_
        print(display_output)  # Getting the output
        # Getting the gprs message output from the ommand
        gprs_message = {'GPRS_message': display_output}
        gprs_mod = Internal_Publish_subscriber()
        gprs_mod.Publisher_dict(ip, gprs_message, port)

    def Location_cellular_network(self, sim800l, ip, port):
        sim800l.write('AT;\n'.encode('UTF-8'))
        sim800l.readline().decode('UTF-8')
        sim800l.write('AT +SAPBR = 3,1,"CONTYPE","GPRS"\n;'.encode('UTF-8'))
        sim800l.write('AT +SAPBR = 3,1,"APN","RCMNET"\n;'.encode('UTF-8'))
        sim800l.write('AT +SAPBR = 1,1\n;'.encode('UTF-8'))
        sim800l.write('AT +SAPBR= 1,1\n;'.encode('UTF-8'))
        sim800l.write('AT +SAPBR= 2,1\n;'.encode('UTF-8'))
        sim800l.write('AT +CIPGSMLOC=1,1\n;'.encode('UTF-8'))
        print(sim800l.readline().decode('UTF-8'))
        loc_message = {"GPRS_Location_message": loc}
        location_message = Internal_Publish_subscriber()
        location_message.Publisher_dict(ip, loc_message, port)
        if sim800l.readline().decode('UTF-8').split(" ")[0] == "+CIPGSMLOC:":
            loc = sim800l.readline().decode('UTF-8').split(" ")[1]
            # getting the location from the tuple of data
            print("Long,Lat:", loc)
            loc_message = {"GPRS_Location_message": loc}
            location_message = Internal_Publish_subscriber()
            location_message.Publisher_dict(ip, loc_message, port)


class Navigation_sensors(object):
    def Lidar_nav(self):
        pass

    def GPS_module_nav(self, gpsname, serialdev, baudrate, ip, port):
        # Set the comport and baudrate
        ser = serial.Serial(serialdev, baudrate)
        x = str(ser.read(1200))
        pos1 = x.find("$GPRMC")
        pos2 = x.find("\n", pos1)
        compass = x.find("$GPGLL")
        loc = x[pos1:pos2]
        data = loc.split(',')
        geolocator = Nominatim(user_agent=gpsname)
        if data[2] == 'V':
            print('No location found')
        for ty in count(0):
            print(ser.readline())
            try:
                print("Latitude =" + str(float(data[117])/100))
                print("Longtitude = " + str(float(data[119])/100))
                location = geolocator.reverse(
                    str(float(data[117])/100)+"," + str(float(data[119])/100))
                print(location.address)
                global output_address
                output_address = location.address
                gps_dat = {"Latitude": str(float(
                    data[3])/100), "Longitude": str(float(data[5])/100), "Adress": output_address}
                GPS_com_sat = Internal_Publish_subscriber()
                GPS_com_sat.Publisher_dict(ip, gps_dat, port)
            except:
                print("GPS status pending connection.....")

    def camera_slam_nav(self):

        pass

    # Getting the ip and port to publish the rssi value
    def rssi_distance_converter(self, ip, port):
        for r in count(0):
            bssid_list = subprocess.check_output("iwlist scanning", shell=True)
            data_raw_decode = bssid_list.decode()  # decode the raw data
            # Finding the Signal strange from the list index
            for i in data_raw_decode.split(":"):
                try:

                    if len(i.split("=")) == 3:

                        rssi = int(i.split("=")[2].split(
                            "\n")[0].split(" ")[0])
                        Pl = int(i.split("=")[1].split(" ")[0].split("/")[0])
                        Pt = int(i.split("=")[1].split(" ")[0].split("/")[1])
                        A = Pt-Pl
                        c_dat = (A-rssi)*0.014336239
                        global distance
                        distance = math.pow(10, c_dat)
                        #print("Output distance ",Pt,Pl,rssi," dbm",distance-2.55," m")
                        message = {"rssi_distance": distance-2.55}
                        rssi_pub = Internal_Publish_subscriber()
                        rssi_pub.Publisher_dict(ip, message, port)

                    return distance-2.55
                except:
                    pass

    def Audio_navigation(self):
        pass
# Getting the Multiple node logic function to working at the control multi communication level


class Multiple_node_request_logic():  # This function can be using the url and ip both http and https request

    def Multi_node_post_resq(self, message, local_ip, port, node_name):
        # Getting the node request post
        res = requests.post(local_ip+":"+str(port)+"/"+node_name, json=message)
        return res.json()  # Getting the json return data from the request port multinode logic

    def Multi_node_get_resq(self, local_ip, port, node_name):
        get_res = requests.get(local_ip+":"+str(port)+"/"+node_name)
        # Getting the raw json to transfer the data of all post into the system
        return get_res.json()

    def Multi_node_get_server(self, local_ip, port, get_func):
        get_res = equests.get(local_ip+":"+str(port)+"/"+get_func)
        return get_res.json()

# This can be using with the multiple array of chemical sensor,Force sensor,Pressure sensor,


class Tactile_sensor(object):
    # Input sensor list with tuple
    # This array sensor can be streaming over multicache server and the frame data streaming will be process by the other image processing algorithm
    # Getting the image frame from the numpy array sensor
    def Numpy_array_image_frame(self, sensor_list_input, title_name, vis_output, size_video):
        for tr in count(0):
            # Getting the sensor list input
            sensor_list = list(sensor_list_input)
            array = np.array(sensor_list)
            array = array.astype(np.uint8)
            shape_data = array.shape
            # using this shape of sensor input
            ex_shapecal = int(shape_data[0])
            sqrt_state = math.sqrt(ex_shapecal)
            check_int = isinstance(sqrt_state, int)
            if check_int == True:
                array = array.astype(np.uint8)
                array = np.reshape(array, (int(sqrt_state), int(sqrt_state)))
                color_image = cv2.cvtColor(array, cv2.COLOR_GRAY2RGB)*255
                if vis_output == 1:
                    im2 = cv2.resize(
                        color_image, (size_video[0], size_video[1]))
                    cv2.imshow('"'+str(title_name)+'"', im2)
                    if cv2.waitKey(1) & 0xFF == ord(' '):
                        break
            if check_int == False:
                array = array.astype(np.uint8)
                # Finding the factors before add into the reshape by using the factor to calculate the right number
                # Checking the vertical and herizontal state
                upper = math.ceil(math.sqrt(ex_shapecal))+1
                lower = math.floor(math.sqrt(ex_shapecal))
                array = np.reshape(array, (upper, lower))
                color_image = cv2.cvtColor(array, cv2.COLOR_GRAY2RGB)*255
                if vis_output == 1:
                    im2 = cv2.resize(
                        color_image, (size_video[0], size_video[1]))
                    cv2.imshow('"'+str(title_name)+'"', im2)
                    if cv2.waitKey(1) & 0xFF == ord(' '):
                        break
            return color_image  # Output image frame

# Array to image streamer


class Array_image_streamer(object):
    # Getting all data array number into this function
    def Array_image_transfer(cam_num, array_frame, Buffers, ip_number, portdata):
        exec("BUFF_SIZE_"+str(cam_num)+" = "+str(Buffers))
        exec("server_socket_"+str(cam_num) +
             " = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)")
        exec("server_socket_"+str(cam_num) +
             ".setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE_"+str(cam_num)+")")
        exec("host_name_"+str(cam_num)+" = socket.gethostname()")
        # socket.gethostbyname(host_name)
        exec("host_ip_"+str(cam_num)+" = '"+str(ip_number)+"'")
        exec("print(host_ip_"+str(cam_num)+")")
        # Getting the portdata from the list to getting the camera data
        exec("port = "+str(portdata))
        exec("socket_address_"+str(cam_num) +
             " = (host_ip_"+str(cam_num)+","+str(portdata)+")")
        exec("server_socket_"+str(cam_num) +
             ".bind(socket_address_"+str(cam_num)+")")
        # Getting the raw camera data as a publisher to publish the camera data
        exec("print('Listening at_camnum"+str(cam_num) +
             ":',socket_address_"+str(cam_num)+")")
        exec("fps_"+str(cam_num)+","+"st_"+str(cam_num)+","+"frames_to_count_" +
             str(cam_num)+","+"cnt_"+str(cam_num)+" = (0,0,20,0)")
        exec("for r_"+str(cam_num)+" in count(0):"+"\n\t\tmsg_"+str(cam_num)+","+"client_addr_" + str(cam_num)+" = server_socket_"+str(cam_num)+".recvfrom(BUFF_SIZE_"+str(cam_num) + ")"+"\n\t\tprint('GOT connection from',client_addr_"+str(cam_num)+")"+"\n\t\twhile(True):"+"\n\t\t\tencoded_" +
             str(cam_num)+","+"buffer_"+str(cam_num)+" = cv2.imencode('.jpg',"+str(array_frame)+",[cv2.IMWRITE_JPEG_QUALITY,80])\n\t\t\tmessage_"+str(cam_num)+" = base64.b64encode(buffer_"+str(cam_num)+")"+"\n\t\t\tserver_socket_"+str(cam_num)+".sendto(message_"+str(cam_num)+",client_addr_"+str(cam_num)+")")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Create the node public from the json file input from component selection and define function of the code in the node to control
def Create_node_pub(topic, message, addresses, initial_port):
    # Create the module of the node component input into the function
    # Before running the loop of publisher check that the module node is created
    port = initial_port
    address = addresses
    exec("pub_"+str(port) + "= Internal_Publish_subscriber()")
    # Sending the data type dicationary now thinking about getting the value input from json file and convert data into the specific data type
    exec("pub_"+str(port)+".Publisher_dict('"+str(address) +
         "',{"+"'"+str(topic)+"'"+":"+str(message)+"},"+str(port)+")")

# Create the sensor receiver as the subscriber for each sensor parameter input from the json component input but this function going to define by json type code generator


def Create_node_sub(t, addresses, buffer, initial_port):

    port = initial_port
    address = addresses
    exec("sub_"+str(t)+" = Internal_Publish_subscriber()")
    exec("global data_return;data_return"+" = sub_"+str(t) +
         ".Subscriber_dict('"+str(address)+"',"+str(buffer)+","+str(port)+")")
    return data_return


def Camera_multi_cache(cam_num, ip_address, port, Width):
    cache_server = Visual_Cam_optic()
    cache_server.Multifunctional_camera(cam_num, ip_address, port, Width)


def Cache_server(server_ip_address, cache_ip_host, port):
    multicache_server = Visual_Cam_optic()
    multicache_server.Cache_camera_server(
        server_ip_address, cache_ip_host, port)


def Camera_Qr_cache(cam_num, display, cache_ip_host, port, message_ip_address, port_message):
    qr_cache = Visual_Cam_optic()
    qr_cache.Camera_QR_cache(
        cam_num, display, cache_ip_host, port, message_ip_address, port_message)


def Face_cache(cam_num, path_data, display, cache_ip_host, port, message_ip_address, port_message):
    Face_rec_cache = Visual_Cam_optic()
    Face_rec_cache.Face_recog_cache(
        cam_num, path_data, display, cache_ip_host, port, message_ip_address, port_message)


def Face_recognition(path_data, display, ip, port, title_name, cam_num, Buffers, portdata, ip_number):

    face_rec = Visual_Cam_optic()
    face_rec.Camera_Face_recognition(
        path_data, display, ip, port, title_name, cam_num, Buffers, portdata, ip_number)


def Speech_recognition(initial_lang, address, port):

    speech_recog = Audio_function()
    speech_recog.Speech_recognition(initial_lang, address, port)


def Speaking_languages(text, destination_lang, speed, loudness):
    audio_speech = Audio_function()
    audio_speech.Text_to_speech(text, destination_lang, speed, loudness)


def Sensor_array_input(sensor_name, number, sensor_list_input, vis_output, size_video):

    exec(str(sensor_name)+"_"+str(number)+" = Tactile_sensor()")
    Sensor_name_data = str(sensor_name)+"_"+str(number)
    title_name = "'"+str(Sensor_name_data)+"'"
    exec("global data_return;data_return = "+str(sensor_name)+"_"+str(number)+".Numpy_array_image_frame(" +
         str(sensor_list_input)+","+str(title_name)+","+str(vis_output)+","+str(size_video)+")")
    return data_return


def Sensor_anaiter(sensor_name, number, sensor_serial):
    exec("sensor_name_"+str(number)+" = Analog_sensor_read()")
    exec("sensor_name_"+str(number) +
         ".Analog_Iteration_tools('"+str(sensor_name)+"',sensor_serial)")


def Sensor_anasetpins(sensor_name, number, sensor_serial, pins_array):
    exec("sensor_name_"+str(number)+" = Analog_sensor_read()")
    exec("sensor_name_"+str(number) +
         ".Analog_setting_pins(sensor_serial,"+str(pins_array)+")")


def Sensor_anafirmserial(sensor_name, number, sensor_serial, pins, ip, port):
    exec("sensor_name_"+str(number)+" = Analog_sensor_read()")
    exec("sensor_name_"+str(number)+".Analog_firmware_serial(sensor_name," +
         str(number)+","+"sensor_serial"+","+str(pins)+",'"+str(ip)+"',"+str(port)+")")


def Array_streamer_input(cam_num, array_frame, Buffers, ip_number, portdata):
    exec("Sensor_"+str(cam_num)+"= Array_image_streamer()")
    exec("Sensor_"+str(cam_num)+".Array_image_transfer("+str(cam_num)+"," +
         str(array_frame)+","+str(Buffers)+",'"+str(ip_number)+"',"+str(portdata)+")")


def Gyroscope_sensor(module, ip, port):  # Getting i2c address
    gyro_pos_1 = Gyroscope_function()
    # Getting i2c address and name of module
    gyro_pos_1.Gyro_sensor_module(module, i2c_bus, ip, port)


def Language_translator(text, ip, port, lang):
    trans_lang = NLP_language_trans()
    trans_lang.Language_translator(text, ip, port, lang)
# Checking if serial is main_node or node


def Serial_write_multipurpose(number, serial_name, text_input, encode_mode, encode):
    exec("board_name_"+str(number)+" = Serial_write_read()")
    exec("board_name_"+str(number)+".Serial_write(serial_name," +
         str(text_input)+","+str(encode_mode)+",'"+str(encode)+"')")


def Serial_read_multipurpose(number, serial_name, decode_mode, decode, ip, port):
    exec("board_name_"+str(number)+" = Serial_write_read()")
    exec("board_name_"+str(number)+".Serial_read(serial_name," +
         str(decode_mode)+",'"+str(decode)+"','"+str(ip)+"',"+str(port)+")")


def Create_serial_motor(mcu_number, number, pin_number, motor_name):
    # node_type,component_name,Serialdev,mcu_number,number,pin_number,motor_name,speed,gpiol,gpior
    motor_node = Action_control()    # STM32F103C8TX 1 [2, 3] motor_1 1 1 0
    motor_node.Serial_MCU(mcu_number, number, pin_number, motor_name)


def Create_serial_motor_logic(mcu_number, number, speed, gpiol, gpior):
    motor_logic = Action_control()
    motor_logic.Serial_DC_motor_pins_drive(
        mcu_number, number, speed, gpiol, gpior)


def Create_i2c_Servo(servo_num, servo_name, angle, pin):
    try:
        # define the name angle and pin of the servo to connect into the board
        exec("servo_"+str(servo_num)+" = Action_control()")
        exec("servo_"+str(servo_num)+".I2C_servo_motor('" +
             str(servo_name)+"',"+str(angle)+","+str(pin)+")")
    except:
        print("Checking your variables and pins data input")


def Create_serial_Servo(servo_number, servo_name, mcu_number, gpio):

    Servo_motor = Action_control()
    Servo_motor.Serial_Servo_motor(servo_number, servo_name, mcu_number, gpio)


def Create_Servo_motor(mcu_number, servo_number, angle):
    servo_motor_write = Action_control()
    servo_motor_write.Serial_servo_control(mcu_number, servo_number, angle)


def Stepper_serial_gcode(stepper_num, serialdev, serial_com, g_code):
    stepper_node = Action_control()
    stepper_node.Serial_stepper_driver(
        stepper_num, serialdev, serial_com, g_code)


def microcontroller_info_dat(mcu_code_name):
    exec("mcu_"+str(mcu_code_name)+" = Microcontroller_pins()")
    exec("global data_mcu; data_mcu" + " = mcu_"+str(mcu_code_name) +
         ".request_mcu('"+str(mcu_code_name)+"')")  # Getting the request mcu data
    return data_mcu

# Non execution pub node


def Create_sub_node_string(ip, buffer_size, port):
    node_sub_string = Internal_Publish_subscriber()
    node_sub_string.Subscriber_string(ip, buffer_size, port)


def Camera_pub_node(cam_num, buffers, port, ip_number):  # running all theses in exec

    exec("cam_"+str(cam_num)+" = Visual_Cam_optic()")
    exec("cam_"+str(cam_num)+".Camera_raw("+str(cam_num)+"," +
         str(buffers)+","+str(port)+",'"+str(ip_number)+"')")


def Camera_sub_node(cam_num, Buffers, portdata, ip_host, ip_message, port_message):
    exec("cam_"+str(cam_num)+" = Visual_Cam_optic()")
    exec("cam_"+str(cam_num)+".Camera_subscriber("+str(cam_num)+"," +
         str(Buffers)+","+str(portdata)+",'"+str(ip_host)+"','"+str(ip_message)+"',"+str(port_message)+")")

# Non execution sub node


# Input the function into the the command all list of computer vision are { Camera_raw , Camera_QR, Camera_OCR, Camera_yolo, Camera_face_recognition, Camera_Visual_to_text}
def Camera_QR_sub_node(cam_num, buffers, port, port_message, ip_number):

    exec("cam_"+str(cam_num)+" = Visual_Cam_optic()")
    exec("cam_"+str(cam_num)+".Camera_QR("+str(cam_num)+","+str(buffers) +
         ","+str(port)+","+str(port_message)+",'"+str(ip_number)+"')")


def Camera_OCR_sub_node(cam_num, buffers, port, port_message, ip_number):
    exec("cam_"+str(cam_num)+" = Visual_Cam_optic()")
    exec("cam_"+str(cam_num)+".Camera_OCR("+str(cam_num)+","+str(buffers) +
         ","+str(port)+","+str(port_message)+",'"+str(ip_number)+"')")


def Camera_face_rec_sub_node(cam_num, buffers, port, port_message, ip_number):
    exec("cam_object_recog"+str(cam_num)+" = Visual_Cam_optic()")
    exec("cam_object_recog"+str(cam_num)+".Camera_Face_recongnition("+str(cam_num)+"," +
         str(buffers)+","+str(port)+","+str(port_message)+",'"+str(ip_number)+"')")


def Camera_yolo_pub_node(cam_num, Buffers, portdata, port_message, ip_number, display_status, object_labels, model_prototxt, model_caffe_weights):

    cam_object_recog = Visual_Cam_optic()
    cam_object_recog.Camera_yolo(cam_num, Buffers, portdata, port_message, ip_number,
                                 display_status, object_labels, model_prototxt, model_caffe_weights)


def get_datetime(ip, port):
    time_date = Time_processing()
    time_date.Date_time_realtime(ip, port)


def rssi_indoor(ip, port):
    rssi_distance = Navigation_sensors()
    distance = rssi_distance.rssi_distance_converter(ip, port)
    return distance


def GPS_navigation(gpsname, serialdev, baudrate, ip, port):
    gps_nav = Navigation_sensors()
    gps_nav.GPS_module_nav(gpsname, serialdev, baudrate, ip, port)


def GPRS_communication_system(sim800l, command_input, ip, port):
    GPRS_mod = Cellular_networking_com()
    GPRS_mod.raw_command_input(sim800l, command_input, ip, port)


def Location_cellular_network(sim800l, ip, port):
    GPRS_loc = Cellular_networking_com()
    GPRS_loc.Location_cellular_network(sim800l, ip, port)


def Lidar_publisher():
    pass


def Skeletal_detect_cam():
    pass


def Body_detect_cam():
    pass


def Multi_node_logic(local_ip, port, get_func):
    get_res_func = Multiple_node_request_logic()
    global data_out
    data_out = get_res_func.Multi_node_get_server(local_ip, port, get_func)
    return data_out


# Getting the non statement if not found any lib
def Multiplenode_post_logic(message, local_ip, port, node_name):
    post_logic = Multiple_node_request_logic()
    global data_out
    data_out = post_logic.Multi_node_post_resq(
        message, local_ip, port, node_name)
    return data_out


def Multiplenode_get_logic(local_ip, port, node_name):
    get_logic = Multiple_node_request_logic()
    global data_out
    data_out = get_logic.Multi_node_get_resq(local_ip, port, node_name)
    return data_out


def OCR_code_detect():
    pass


def NLP_language():
    pass


def mcu1():
    mcu_data = "STM32F103CBTx"
    mcu_list = microcontroller_info_dat(mcu_data)
    print(mcu_list)


def mcu2():
    mcu_data = "STM32F303K8Tx"
    mcu_list = microcontroller_info_dat(mcu_data)
    print(mcu_list)

#b = Internal_Publish_subscriber()
#data_return = b.Subscriber_dict("127.0.0.1",4096,5090)
# print(data_return)

#c = Internal_Publish_subscriber()
# c.Publisher_dict("127.0.0.1",{"input_1":5048},5040)
