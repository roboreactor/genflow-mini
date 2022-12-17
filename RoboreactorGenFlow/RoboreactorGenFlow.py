import jwt 
import smbus
from ast import literal_eval
from flask import Flask,jsonify,request,render_template,redirect,url_for 
import os 
import getpass 
import configparser
import json 
import time 
import cv2
import socket
import threading
import subprocess
import requests # Getting the request from the json api of the update version on the microcontroller support version path 
import sounddevice as sd
import serial.tools.list_ports
from itertools import count
bus = smbus.SMBus(1)

#user = getpass.getuser() 
user = os.listdir("/home/")[0]
Home_path = '/home/'+str(user)+"/" #Home path to get the config file and project setting outside the node generator

Path = '/home/'+str(user)+"/Roboreactor_projects" # getting the file path 
Path_local = '/home/'+str(user)+"/Roboreactor_Gen_config"  # Generate the main path for config gen and code generator

path_serial = "/sys/class/tty"
mem_dir_create = [] 
app = Flask(__name__) 
serial_count = []

#MCU series of stm32 in the json file
mcu_list_series_stm32 = "https://raw.githubusercontent.com/stm32duino/BoardManagerFiles/main/package_stmicroelectronics_index.json"
path_data = "/home/"+user+"/RoboreactorGenFlow/"
try:
   Load_json = open(path_data+"data_token_secret.json",'r') # Load the json data in local computer this file need to be export from the website 
   OAuth  = json.loads(Load_json.read())  # Load json data of the persal OAuth downloaded from the web and put into the local file 
   Account_data = OAuth.get('Account')
   Token_data = OAuth.get('Token')
   Secret_data = OAuth.get('Secret') 
   Project_data = OAuth.get('project_name') # getting the project name  
except:
     pass 

class Authentication_function(object): 
        def request_authentication_API(self,Email,token,secret,Project):
                Authentication_data = {'Email':Email,'project_name':Project}
                res = requests.post('https://roboreactor.com/API/endpoint_request', json=Authentication_data)
                #return logic to the authentication to check the status of the hardware connection 
                q_res = res.json().get(Authentication_data.get('Email'))
                token_data = str(q_res[0])+'.'+str(token)
                decode_Data = jwt.decode(q_res[0]+'.'+str(token),str(q_res[1]) ,algorithm=["HS512"])
                return decode_Data 

def Authentication_system(Email,token,secret,Project): 
      authen = Authentication_function() 
      data_out = authen.request_authentication_API(Email,token,secret,Project)
      return data_out

try:
     Data = Authentication_system(Account_data,Token_data,Secret_data,Project_data)  # Getting the project data to verify the project data to post request sendback the data 
     print(Data) # Getting the email to verfy the data to send back to request the project and send back data to the user profile information  
except: 
     pass 
class Machine_data_processing(object):
           
           def get_ip(self): 
                   loc = requests.request('GET', 'https://api.ipify.org')
                   ip = loc.text
                   return ip # Getting the ip data return this will return the public ip of the client machine 
           def get_serial_port(self):   # Getting the serial devices name 
               
               try:
                    devices_data = subprocess.check_output(" python3 -m serial.tools.list_ports -s",shell=True)
                    serial_port = devices_data.decode().split()
                    if '/dev/stlinkv2-1_1' in serial_port:
                           serial_port.remove('/dev/stlinkv2-1_1')
                    ports = serial.tools.list_ports.comports()
                    serial_devices_name = {}
                    for port, desc ,hid in sorted(ports):
                                 print("{}: {} [{}]".format(port, desc, hid))
                                 serial_devices_name[port] = desc                     
                    return serial_devices_name
               except:
                    print("No serial device found ")
                    return "No serial device found"
           def get_local_ip(self):
                     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     s.connect(("8.8.8.8",80))
                     return s.getsockname()[0]  

           def get_audio_device(self):
                    devices = list(sd.query_devices())
                    return devices 
           def get_camera_device(self):
                    index = 0
                    arr = []
                    i = 6
                    for i in range(0,i):
                        cap = cv2.VideoCapture(index)
                        if cap.read()[0]:
                            arr.append(index)
                            cap.release()
                        index += 1
                        i -= 1
                    return {"camera_array":arr}                          
           def get_devicehost(self):
                    return os.listdir("/home/")[0]
           def Get_i2c_address(self):
                    address_mem = []
                    def bearing255(address):
                          bear = bus.read_byte_data(address, 1)
                          
                    def bearing3599(address):
                          bear1 = bus.read_byte_data(address, 2)
                          bear2 = bus.read_byte_data(address, 3)
                          bear = (bear1 << 8) + bear2
                          bear = bear/10.0
                          #return bear
                    for i in range(0,128):
                           try:
                              address_data = literal_eval(hex(i)) 
                              bearing3599(address_data)     #this returns the value to 1 decimal place in degrees. 
                              bearing255(address_data)      #this returns the value as a byte between 0 and 255. 
                              address_mem.append(hex(i))
                              
                           except: 
                                  pass 
                    return {'I2C':address_mem}

 
@app.route("/device_info")
def device_info():
       getdevice_data = Machine_data_processing()
       cam_device = getdevice_data.get_camera_device()
       audio_device = getdevice_data.get_audio_device()
       serial_devices = getdevice_data.get_serial_port()
       host_name = getdevice_data.get_devicehost() 
       ip = getdevice_data.get_ip() 
       i2c_address =  getdevice_data.Get_i2c_address() 
       localip = getdevice_data.get_local_ip()
       Account_data = OAuth.get('Account')
       
       data_host = {'email':Account_data,"i2c_devices":i2c_address,"serial_devices":serial_devices,"Vision_system":cam_device,"Audio_system":audio_device,"Host_name":host_name,"IP":ip,'Local_ip':localip}
       try:
         res = requests.post('https://roboreactor.com/devices/report',json=data_host) #Report node client connection 
         print(res.json())
         print(Account_data)
         return jsonify(data_host)
       except:
            print("Server communication error please check your internet connection")
@app.route("/path_fetch")
def fetch_path():
       path_dat = "/home/"+user+"/Roboreactor_projects/"
       json_data = {"Path_file":path_dat}
       return jsonify(json_data)  

class data_transfer_features():
         def send_component_selected_data(self,email,project_name,components_list):
            try:
                 #Getting the data from the email project_name and the component_list to create the new patter of the data to classify data from the post request and get the display from the value account data 
                 #example pattern   {"category": [{"title":"Roboreactor_project",'items':[{'title':'Face_recognition_1'},{'title':'Servo_motor_1'}]}] } #
                 #Created pattern = {'kornbot380@hotmail.com':{"category": [{"title":"Roboreactor_project",'items':[{'title':'Face_recognition_1'},{'title':'Servo_motor_1'}]}] }} # Getting the current email patter>
                 Items_list_created = []  #Getting the item list mapping into the current data input
                 Category_data = [] # Getting the category data to input into the project features data transfer into the server 
                 #Items_json = {}
                 # The right form of the pattern 
                 #{"kornbot380@hotmail.com":{"category":[{"items":[{"title":"face_recog_1  ======> 127.0.0.1,0,5080,5081,Non"},{"title":"Servo_control_2  ======> 127.0.0.1,5081,I2C,2"}],"title":"Roboreactor"}]}} 
                 for r in list(components_list):  # Getting the list of the components from the data inserted 

                                sub_items = {'title':str(r)+"  ======> "+str(components_list.get(r))}
                                Items_list_created.append(sub_items) # Getting the components list from the current data insert from the components list 
                                print("Current Items",Items_list_created)
                                #Items_json[r] = str(components_list.get(r)) 
                 #                  print(Items_json)   
                                #Create Full pattern of the data 
                 create_category = {'title':project_name,'items':Items_list_created}
                 print(create_category)
                 Category_data.append(create_category)
                 #json_dumps = json.dumps({"category":Category_data}) 
                 Message_pattern = {email:{"category":Category_data}} 
                 print(Message_pattern)
                 #Sending the feature data in the full message to activate the function inside the features data 
                 res = requests.post('https://roboreactor.com/api/features_component',json=Message_pattern)  
                 print(res.json())
                
            except:
               pass

def host_info_callback(path_serial):
       
       list_serial = os.listdir(path_serial)
       for l in range(0,len(list_serial)):
          
           if len(list_serial[l].split("ttyACM")) >1: 
              
              if list_serial[l] not in serial_count: 
                  serial_count.append(list_serial[l])      
           if len(list_serial[l].split("ttyUSB")) >1: 
               if list_serial[l] not in serial_count:
                     serial_count.append(list_serial[l])
       for check_serial in serial_count: 
                       if check_serial not in list_serial: 
                                      serial_count.remove(check_serial) #remove the list of the serial in case not found attach on physical devices connection           

@app.route("/",methods=['GET','POST'])  # Initial page start will collect and send the local machine data to update into the front end local machine data
def index():
      
      return render_template("roboreactor_node.html")
      
@app.route('/filepath',methods=['GET','POST'])
def filepathcreate():
      if request.method == 'POST':
            print('Creating path....')
            print(request.get_json())  # parse as JSON
            code_json = request.get_json()
            print("Creating to this path",code_json.get('path'))
            try: 
                 print("Creating directory path")
                 
                 try:
                     config = configparser.ConfigParser()
                     config.add_section('Project_path')
                     print("Start writing config file......")
                     config.set('Project_path','path',code_json.get('path')) 
                     configfile = open(Path+"/config_project_path.cfg",'w') 
                     config.write(configfile) 
                 except: 
                     print("Start writing config file...")
                 os.mkdir(code_json.get('path'),mode=0o777)    
                
            except:
                print("Directory was created")
                message_status = {'dir_status':'created'}
                mem_dir_create.append(message_status)
                if len(mem_dir_create) >1: 
                     mem_dir_create.remove(mem_dir_create[0])
                print(mem_dir_create)
                 

            print(type(code_json)) 
            return 'OK created path', 200 
      else:
        try:
             config = configparser.ConfigParser()    
             config.read(Path+'/config_project_path.cfg') 
             list_data = os.listdir(Path)
             print(list_data)
             path_config = config['Project_path']['path']
             host_info_callback(path_serial)
             message = {'Local_machine_data':{'local_directory':path_config},'Serial_local':serial_count,'Directory_status':{'dir_status':'created'}}  # Getting the data from local machine by running the usb check loop and other local data components conection 
             return jsonify(message)  # serialize and use JSON headers
        except:
             print("Error in reading the config file")
@app.route('/code', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        code_json = request.get_json()
        print(type(code_json)) 
        #Start generating the file here 
        json_object = json.dumps(code_json) # getting the json config and generate the components features send back to the database 
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Getting the data from the json to create the features data transfer into the server 
        # Account data use to activate the generation of the code 
        email = Data.get('Account')
        project_name = Data.get('project_name') #Getting the project name and email to verify and sending the data into the server
        features_data = data_transfer_features()
        features_data.send_component_selected_data(email,project_name,json_object) # Getting the email,project_name,component_list ==> This refer to the json generated from the json_object
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        Generated_node = open(Path+"/"+"node_generated.json", "w") 
        Generated_node.write(json_object) 
        Generated_node = open(Path+"/"+"node_generated.json", "r") 
        data = json.loads(Generated_node.read())
        print("Node of the code",data)
        os.system("python3 roboreactor_config_gen.py")
        return 'OK', 200
@app.route('/start_project', methods=['GET', 'POST'])
def start_project():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        code_json = request.get_json()
        print(type(code_json)) 
        #Start generating the file here 
        json_object = json.dumps(code_json) # getting the json config 
        print(json_object) 
        load_json = json.loads(json_object) 
        try:
            local_path = load_json.get('Local_machine_data').get('Local_machine_data').get('local_directory')
            print(local_path) #getting the test path directory 
        except: 
            print("local path blank please fill directory path") 
        #Generate the path on the supervisor to start software at boot 
        
        path_supervisor = "/lib/systemd/system/"  # Running the path for the software  on supervisor
        project_name = local_path.split('/')[len(local_path.split('/'))-1]
        log_project_path = "/var/log/"+str(project_name)
        command = "/usr/bin/python3 "
        try:
            os.mkdir(log_project_path,mode=0o777) # Crating the log project file 
        except:
             print("Directory was created")
        config = configparser.ConfigParser()
        config = configparser.RawConfigParser()
        config.optionxform = str
        sections = 'Unit' # Getting the project name 
        services = 'Service'
        wanted = 'Install'
        print(sections) 
        config.add_section(sections)
        config.set(sections,'Description','Project:'+str(project_name))
        config.set(sections,'After','multi-user.target')
        config.add_section(services)
        config.set(services,'Type','idle')
        config.set(services,'ExecStart',command+str(local_path)+"/"+str(project_name)+".py")
        config.add_section(wanted)
        config.set(wanted,'WantedBy','multi-user.target')
        configfile = open(path_supervisor+str(project_name)+".service",'w')
        config.write(configfile) 
        #os.system("sudo chmod 644 /lib/systemd/system/"+str(project_name)+".service") # Run the
     
       

        return 'OK', 200
@app.route('/restart_project', methods=['GET', 'POST'])
def restart_project():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        code_json = request.get_json()
        print(type(code_json)) 
        #Start generating the file here 
        json_object = json.dumps(code_json) # getting the json config 
        print(json_object) 
        load_json = json.loads(json_object)
        local_path = load_json.get('Local_machine_data').get('Local_machine_data').get('local_directory')
        print(local_path) #getting the test path directory 
        #Generate the path on the supervisor to start software at boot 
        
        path_supervisor = "/lib/systemd/system/"  # Running the path for the software  on supervisor
        project_name = local_path.split('/')[len(local_path.split('/'))-1]
        log_project_path = "/var/log/"+str(project_name)
        command = "/usr/bin/python3 "
        os.system("systemctl daemon-reload")
        os.system("systemctl enable "+str(project_name)+".service") 
        os.system("systemctl start "+str(project_name)+".service")
        return 'OK', 200
@app.route('/stop_project', methods=['GET','POST'])
def stop_project():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        code_json = request.get_json()
        print(type(code_json)) 
        #Start generating the file here 
        json_object = json.dumps(code_json) # getting the json config 
        print(json_object) 
        load_json = json.loads(json_object)
        local_path = load_json.get('Local_machine_data').get('Local_machine_data').get('local_directory')
        print(local_path) #getting the test path directory 
        #Generate the path on the supervisor to start software at boot 
        
        path_supervisor = "/lib/systemd/system/"  # Running the path for the software  on supervisor
        project_name = local_path.split('/')[len(local_path.split('/'))-1]
        log_project_path = "/var/log/"+str(project_name)
        command = "/usr/bin/python3 "
        os.system("systemctl stop "+str(project_name)+".service")
        return 'OK', 200   
    # GET request
    #else:
    #    message = {'greeting':'Hello from Flask!'}
    #    return jsonify(message)  # serialize and use JSON headers

#if __name__ =="__main__":
app.run(debug=True,threaded=True,host="0.0.0.0",port=8000)


