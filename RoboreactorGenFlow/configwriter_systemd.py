import os
import pwd
import time
import subprocess
import requests
import configparser

user = os.listdir("/home/")[0]
try:
    os.mkdir("/usr/lib/systemd/system", mode=0o777)
except:
    print("System directory was created")
Generate_path = "/usr/lib/systemd/system/"
os.system("sudo chmod -R 777 "+Generate_path)
os_platform = os.uname()  # uname

os_system = os_platform.sysname
os_release = os_platform.release
os_machine = os_platform.machine
os_processor = subprocess.check_output(
    "lscpu | grep 'Model name:' | sed -r 's/Model name:\s{1,}//g'", shell=True).strip().decode()

print(os_system, os_release, os_machine, os_processor)

project_name = 'Project:RoboreactorGenFlow'
mode = 'multi-user.target'
Python_exc_path = "/bin/bash "
Python_exc_path1 = "/usr/bin/python3 "
Working_path = "/home/"+user+"/RoboreactorGenFlow"
# Change username over the platform
Execute_path = "/home/"+user+"/RoboreactorGenFlow/RoboreactorGenFlow.py"
Execute_path2 = "/home/"+user+"/RoboreactorGenFlow/runsystem.sh" 
Execute_path1 = "/home/"+user+"/RoboreactorGenFlow/request_config.py"
config = configparser.ConfigParser()
config.optionxform = str
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Running Roboreactor_installer
# Checking the OS
ar_os_data = os_release.split("-")
# Getting the os architecture data from the os and classify the os data
ar_kernel = ar_os_data[len(ar_os_data)-1]
res_os = requests.get("https://roboreactor.com/OS_support")
ref_os_data = res_os.json()
list_support_os = ref_os_data.get("OS_data")  # Getting the list of the os
list_board_os = ref_os_data.get("OS_board")
print(list_support_os)
print(list_board_os)
if ar_kernel in list_support_os:
    if list_board_os.get(ar_kernel) == "Jetson architecture":
        settings = ['Unit', 'Service', 'Install']
        # Unit
        # Getting the section added into the list topic
        config.add_section(settings[0])
        config.set(settings[0], 'Description', str(project_name))
        config.set(settings[0], 'After', str(mode))
        # Service
        config.add_section(settings[1])
        config.set(settings[1], 'Type', 'idle')
        config.set(settings[1], 'WorkingDirectory', Working_path)
        config.set(settings[1], 'User', str(user))
        config.set(settings[1], 'ExecStart', str(
            Python_exc_path1+Execute_path))
        config.set(settings[1], 'WantedBy', 'always')
        # Install
        config.add_section(settings[2])
        config.set(settings[2], 'WantedBy', str(mode))
        configfile = open(
            Generate_path+"RoboreactorGenFlow.service", 'w')
        config.write(configfile)
    if list_board_os.get(ar_kernel) == "Raspberrypi architecture":
        settings = ['Unit', 'Service', 'Install']
        # Unit
        # Getting the section added into the list topic
        config.add_section(settings[0])
        config.set(settings[0], 'Description', str(project_name))
        config.set(settings[0], 'After', str(mode))
        # Service
        config.add_section(settings[1])
        config.set(settings[1], 'Type', 'idle')
        config.set(settings[1], 'WorkingDirectory', Working_path)
        config.set(settings[1], 'User', str(user))
        config.set(settings[1], 'ExecStart', str(Python_exc_path+Execute_path2))
        config.set(settings[1], 'WantedBy', 'always')
        # Install
        config.add_section(settings[2])
        config.set(settings[2], 'WantedBy', str(mode))
        configfile = open(Generate_path+"RoboreactorGenFlow.service", 'w')
        config.write(configfile)
    if list_board_os.get(ar_kernel) == "Laptop_PC":
        settings = ['Unit', 'Service', 'Install']
        # Unit
        # Getting the section added into the list topic
        config.add_section(settings[0])
        config.set(settings[0], 'Description', str(project_name))
        config.set(settings[0], 'After', str(mode))
        # Service
        config.add_section(settings[1])
        config.set(settings[1], 'Type', 'idle')
        config.set(settings[1], 'WorkingDirectory', Working_path)
        config.set(settings[1], 'User', str(user))
        config.set(settings[1], 'ExecStart', str(
            Python_exc_path1+Execute_path))
        config.set(settings[1], 'WantedBy', 'always')
        # Install
        config.add_section(settings[2])
        config.set(settings[2], 'WantedBy', str(mode))
        configfile = open(Generate_path+"RoboreactorGenFlow.service", 'w')
        config.write(configfile)
    if list_board_os.get(ar_kernel) == "Laptop_PC":
        settings = ['Unit', 'Service', 'Install']
        # Unit
        # Getting the section added into the list topic
        config.add_section(settings[0])
        config.set(settings[0], 'Description', str(project_name))
        config.set(settings[0], 'After', str(mode))
        # Service
        config.add_section(settings[1])
        config.set(settings[1], 'Type', 'idle')
        config.set(settings[1], 'WorkingDirectory', Working_path)
        config.set(settings[1], 'User', str(user))
        config.set(settings[1], 'ExecStart', str(
            Python_exc_path1+Execute_path))
        config.set(settings[1], 'WantedBy', 'always')
        # Install
        config.add_section(settings[2])
        config.set(settings[2], 'WantedBy', str(mode))
        configfile = open(Generate_path+"RoboreactorGenFlow.service", 'w')
        config.write(configfile)

    if list_board_os.get(ar_kernel) == "Khadas_VIMs":
        settings = ['Unit', 'Service', 'Install']
        # Unit
        # Getting the section added into the list topic
        config.add_section(settings[0])
        config.set(settings[0], 'Description', str(project_name))
        config.set(settings[0], 'After', str(mode))
        # Service
        config.add_section(settings[1])
        config.set(settings[1], 'Type', 'idle')
        config.set(settings[1], 'WorkingDirectory', Working_path)
        config.set(settings[1], 'User', str(user))
        config.set(settings[1], 'ExecStart', str(
            Python_exc_path1+Execute_path))
        config.set(settings[1], 'WantedBy', 'always')
        # Install
        config.add_section(settings[2])
        config.set(settings[2], 'WantedBy', str(mode))
        configfile = open(Generate_path+"RoboreactorGenFlow.service", 'w')
        config.write(configfile)

settings = ['Unit', 'Service', 'Install']
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
config1 = configparser.ConfigParser()
config1.optionxform = str
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Running remote_request_config
# Unit
# Getting the section added into the list topic
config1.add_section(settings[0])
config1.set(settings[0], 'Description', "Request_remote_config")
config1.set(settings[0], 'After', str(mode))
# Service
config1.add_section(settings[1])
config1.set(settings[1], 'Type', 'idle')
config1.set(settings[1], 'WorkingDirectory', Working_path)
config1.set(settings[1], 'User', str(user))
config1.set(settings[1], 'ExecStart', str(Python_exc_path1+Execute_path1))
config1.set(settings[1], 'WantedBy', 'always')
# Install
config1.add_section(settings[2])
config1.set(settings[2], 'WantedBy', str(mode))
configfile1 = open(Generate_path+"Remote_request_config.service", 'w')
config1.write(configfile1)
