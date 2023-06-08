import os 
import jwt 
import json 
import time
import socket
import requests 
import configparser 
import threading
import subprocess 
from itertools import count 
device_name = os.listdir("/home/")[0] # getting the device name data 
path_token = "/home/"+os.listdir("/home/")[0]+"/RoboreactorGenFlow/" # Getting the path token data 
path_rlib = "/home/"+os.listdir("/home/")[0]+"/Roboreactor_library/"
path_project = "/home/"+os.listdir("/home/")[0]+"/Roboreactor_projects/"
Current_device_data = {} 
data_transfer_OS = {}
Live_URL = "https://roboreactor.com"
#Live_URL = "http://192.168.50.201:5890"
server_1 = "https://roboreactor.com/Joint_control_datas"
server_joint = "https://roboreactor.com/package_iot_control"
#Put this in the function of loop generator on and off function 
mcus_pin_map = "https://raw.githubusercontent.com/KornbotDevUltimatorKraton/Microconroller_pin_map_database-/main/mcus_board_lists.json" # Re>
Serial_separator = {} 
Serial_datas = {} 
serial_separator = {} # Get the serial separator to separate the data of the serial type function 
serial_list = {} 
serial_group = {} #Get the serial json data of the group check list joint serial 
Commu_check_data = {} # Get the communication type data 
check_loop_joints = [] 
check_same_IO = [] # Check GPIO is the same pin generated inside the loop or not 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
# SBC communication code 
board_catg = {} # Get the board category data 
#get the data of the joint function communication 
sbc_communication = {} 
feedback_sensor_type = {} # get the feedback sensor type of data to check the analog sensor input from te list of the joint 
feedback_signal_intercept = {} # Check the data signal interception 
Check_hardware_board = {} #get the hardware board 
data_io_control = {'Servo_PWM_output':'s','PWM_output':'p'} # Get the data IO output and input 
#Getting the operating system and machine data of the user
os_platform = os.uname() # uname 
feedback_sensor_type = {} # get the feedback sensor type of data to check the analog sensor input from te list of the joint 
feedback_signal_intercept = {} # Check the data signal interception 
Check_hardware_board = {} #get the hardware board 
payload_feedback = ['{']   # Get the payload feedback to append in this list so that we can generate the variable for the joint feedback payload control 
payload_joints_container = [] # Get all data to record in the joint payload container

os_system = os_platform.sysname
os_release = os_platform.release
os_machine = os_platform.machine 
os_processor = subprocess.check_output("lscpu | grep 'Model name:' | sed -r 's/Model name:\s{1,}//g'", shell=True).strip().decode()

print(os_system,os_release,os_machine,os_processor)

path_project_data = "/home/"+str(device_name)+"/Roboreactor_projects/"  #Getting the path of the project 
project_json_path = open(path_project_data+"node_generated.json") # Getting the node generated project 
node_path_read = json.loads(project_json_path.read()) # getting the path of the multiple node 
detect_multiple_node = [] # Getting the multiple node data append into the list 
try:
   Load_json = open(path_token+"data_token_secret.json",'r') # Load the json data in local computer this file need to be export from the website 
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
                decode_Data = jwt.decode(q_res[0]+'.'+str(token),str(q_res[1]) ,algorithms=["HS512"])
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

class OS_data_transfer(object): 

    def send_os_data(self,email,topic,message):    
        try:  

             for i in range(0,len(topic)): # Getting the list of the command  input 
                   data_transfer_OS[topic[i]] = message[i]   # Getting the data from
             dictToSend = {email:data_transfer_OS} #Get this data from the back end fetching data from the front end 
             res = requests.post('https://roboreactor.com/API/profile_singleboard', json=dictToSend)
             print(res.json()) 
        except:
             pass 
#Getting the OS data request 
def OS_data_request():
       os_data_trans = OS_data_transfer() 
       os_data_trans.send_os_data(Account_data,['OS','Release','Architecture','Processor','Project_name'],[os_system,os_release,os_machine,os_processor,Data.get('project_name')]) # getting the machine data 

OS_data_request()
#Request the quest update current device data    
def update_current_data():
           try:
                 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                 s.connect(("8.8.8.8",80))
                 local_ip = s.getsockname()[0]
                 print(local_ip)
                 res_device_info = requests.get("http://"+local_ip+":8000/device_info")
                 data_device_info = res_device_info.json()
                 print(data_device_info)   
                 OS_data_request()               
                 #res_inactive = requests.post("https://roboreactor.com/device_info_data",json({Account>
                 #print(res_inactive.json()) # Return inactive data
           except:
                print("Error request internal server") 

#Loading the data from the path of the token 
def Main_request(): 
  for i in count(0):
        #Step 0 checking the email account of the user to get the status payload 
        #Step 1 post request into the broker to run checking status 
        #Step 2 after detect status ON then running the json file input from the payload 
        #Step 3 after running the payload finish then change the status of the json input to status off 
     try:
       Get_devices_info = requests.get("https://roboreactor.com/get_device_info") 
          
       if str(Get_devices_info.json().get(Account_data)) == 'None':
           try:
              s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
              s.connect(("8.8.8.8",80))
              local_ip = s.getsockname()[0]
              print(local_ip)
              res_device_info = requests.get("http://"+local_ip+":8000/device_info")
              data_device_info = res_device_info.json()
              print(data_device_info)     
              #res_inactive = requests.post("https://roboreactor.com/device_info_data",json({Account_data:"Inactive"}))
              #print(res_inactive.json()) # Return inactive data
           except:
             print("Error request internal server")
       if str(Get_devices_info.json().get(Account_data)) != 'None': # Checking if not in None then request the new device update 
           print("Checking device update ")
           devices_list = list(Get_devices_info.json().get(Account_data))
                 
           if  device_name not in devices_list:
                        print("Now updating device....")
                        
                        try:
                             
                              res_device_info = requests.get("http://0.0.0.0:8000/device_info")
                              data_device_info = res_device_info.json()
                              print(data_device_info)     
                              #res_inactive = requests.post("https://roboreactor.com/device_info_data",json({Account>
                              #print(res_inactive.json()) # Return inactive data
                        except:
                              print("Error request internal server") 
           if device_name in devices_list: 
                           print("Now updating device sub data....")
                           #Checking the header of the device 
                                                                     
     except:
          print("Error requesting the server data")
     try:
        res = requests.get("https://roboreactor.com/Config_status") # Getting the remote config of the data  
        data_check = res.json() # Step 0 checking the email 
        status = data_check.get(Account_data) # Getting the status payload for step 1 and step 2
        try:
           
           if status != {}:
                if status.get("status") == "ON": # Checking the status
                             # Getting the request 
                             
                             
                              
                             # Sending the post request
                             res_config = requests.post("https://roboreactor.com/api/remote_config",json={Account_data:{"status":"OFF","path":status.get('path'),"payload":status.get('payload')}})
                             print(res_config.json())
                             print("Writing the payload code",status.get("payload")) # Writing the payload  
                             json_object = json.dumps(status.get("payload"))
                             user_check = status.get("path").split("/")
                             user_check.remove(user_check[0]) # request the user data reference for the devices authentication
                             Path = "/home/"+os.listdir("/home/")[0]+"/Roboreactor_projects"        
                             if os.listdir("/home/")[0] == user_check[1]:    
                                 for i in range(0,3):
                                    res = requests.post("https://roboreactor.com/remote_config",json=res_config.json().get('payload'))
                                    generate_json  = open(Path+"/node_generated.json","w") #Generate inside the path of node_generated_code path  
                                    generate_json.write(json.dumps(status.get("payload")))                           
                                    try:
                                         if len(user_check) == 4: 
                                               user_check_dir = user_check[len(user_check)-2]                                 
                                               if user_check_dir in os.listdir("/home/"+os.listdir("/home/")[0]):
                                                           try: 
                                                               print("Creating directory path")
                                                               #Path = "/home/"+os.listdir("/home/")[0]+"/Roboreactor_projects" #+user_check[len(user_check)-1]   
                                                               try:
                                                                   config = configparser.ConfigParser() 
                                                                   config.add_section('Project_path')
                                                                   print("Start writing path config file......")
                                                                   config.set('Project_path','path',"/home/"+os.listdir("/home/")[0]+"/Roboreactor_projects") 
                                                                   configfiles = open(Path+"/config_codegen.cfg",'w') 
                                                                   config.write(configfiles) 

                                                               except: 
                                                                    print("Start writing config file...")
                    
                                                               try:
                                                                   configs = configparser.ConfigParser() 
                                                                   configs.add_section('Project_path')
                                                                   print("Start writing config file......")
                                                                   configs.set('Project_path','path',status.get('path')) 
                                                                   configfile = open(Path+"/config_project_path.cfg",'w') 
                                                                   configs.write(configfile) 
                                                                  
                                                               except: 
                                                                    print("Start writing config file...")
                                                               os.mkdir(status.get('path'),mode=0o777)    
                                                               #os.system("python3 /home/"+str(os.listdir("/home/")[0])+"/RoboreactorGenFlow/roboreactor_config_gen.py")
                                                           except:
                                                               print("Directory was created")
                                                                                                                     
                                    except:
                                         print("Haven't create the name for the project")                                             
                                 if user_check[len(user_check)-1] in os.listdir("/home/"+os.listdir("/home/")[0]+"/Roboreactor_projects"):
                                                                 os.system("python3 /home/"+str(os.listdir("/home/")[0])+"/RoboreactorGenFlow/roboreactor_config_gen.py")         
                if status.get("status") == "OFF":
                               print(res.json()) # Waiting for the new remote config                                                                
                               
        except:
            print("Data is not json type")       

     except:
          print("Cannot connect to the server")                 
def side_request():
   for i in count(0):  
       try:
              res_devices = requests.get("https://roboreactor.com/devices_remote") 
              devices_data = res_devices.json().get(Account_data)
              if str(devices_data) == "None":
                        print("Data is not json type please check server")
              if str(devices_data) !="None":
                     print(devices_data)
                     if devices_data.get("devices_request") == "ON":
                                    update_current_data()
                                    rest_post_Device = requests.post("https://roboreactor.com/devices_off_req",json={Account_data:{"devices_request":"OFF"}}) 
                                    print(rest_post_Device.json())     
                                    
       except:
            print("Error server connection")    
def Generate_request():
    for i in count(0):
           try:
              res_gen = requests.get("https://roboreactor.com/generation_statement") 
              devices_gen = res_gen.json().get(Account_data)
              if str(devices_gen) == "None":
                        print("Data is not json type please check server")
              if str(devices_gen) !="None":
                     #Generate the running path file here to run the library 
                     if devices_gen.get('Generator') == "ON":
                                   print("Generate_path",devices_gen.get('Path_project'))
                                   #Getting the new path generate into the system 
                                   Path_data = devices_gen.get('Path_project').split("/")
                                   Path_data.remove(Path_data[0]) # remove the first data inside the list 
                                   Length_path = len(Path_data)
                                   if Length_path == 4: 
                                        for r in range(0,5):
                                              Project_name = Path_data[Length_path-1]
                                              print("Project_name",Project_name)
                                              # Now starting to generate the systemd file to running the service
                                              print("Generate the service file")
                                              Generate_path = "/usr/lib/systemd/system/" 
                                              project_name = 'Project:'+Project_name   
                                              mode = 'multi-user.target' 
                                              Python_exc_path = "/usr/bin/python3 "
                                              Working_path1 = "/home/"+device_name+"/RoboreactorGenFlow/" 
                                              Working_path = "/home/"+device_name+"/Roboreactor_projects/"+Project_name
                                              Execute_path = "/home/"+device_name+"/Roboreactor_projects/"+Project_name+"/"+Project_name+".py"  
                                              Execute_path1 = "/home/"+device_name+"/RoboreactorGenFlow"+"/Multiple_node_data_projection.py" 
                                              config = configparser.ConfigParser() 
                                              config.optionxform = str
                                              settings = ['Unit','Service','Install']
                                              #Unit
                                              config.add_section(settings[0]) # Getting the section added into the list topic 
                                              config.set(settings[0],'Description',str(project_name)) 
                                              config.set(settings[0],'After',str(mode))
                                              #Service 
                                              config.add_section(settings[1])
                                              config.set(settings[1],'Type','idle')
                                              config.set(settings[1],'WorkingDirectory',Working_path)
                                              config.set(settings[1],'User',str(device_name))
                                              config.set(settings[1],'ExecStart',str(Python_exc_path+Execute_path))
                                              config.set(settings[1],'WantedBy','always')
                                              #Install 
                                              config.add_section(settings[2])
                                              config.set(settings[2],'WantedBy',str(mode))
                                              configfile = open(Generate_path+"/"+Project_name+".service",'w')
                                              config.write(configfile)
                                              os.system("sudo chmod -R 777 "+Generate_path+"/"+Project_name+".service")                                         
                                              #Now turn off the activation 
                                              send_off_gen_com = {Account_data:{"Generator":"OFF","Path_project":devices_gen.get('Path_project')}}
                                              res_off_gen = requests.post("https://roboreactor.com/Generator_onchange",json=send_off_gen_com)
                                              print(res_off_gen.json())
                                              for mpi in range(0,2):
                                                            try:    
                                                                   write_data_projector = open(path_token+"Multiple_node_data_projection.py",'w')
                                                                   write_data_projector.writelines("import os" +"\nimport sys"+"\nimport json"
                                                                   +"\nfrom flask import Flask,request,jsonify,render_template,url_for,redirect"+"\napp = Flask(__name__)"
                                                                   +"\ndata_transfer = {}"+"\n@app.route('/Multiplenode_logic',methods=['GET','POST'])"+"\ndef index():"+"\n\t\tinput_json = request.get_json(force=True)"+"\n\t\thead_function = list(input_json)[0]"+"\n\t\tdata_transfer[head_function] = input_json.get(head_function)"+"\n\t\treturn jsonify(data_transfer)"+"\n@app.route('/get_Multiplenode_logic')"
                                                                   +"\ndef get_multiple_node():"+"\n\treturn jsonify(data_transfer)"
                                                                   +"\napp.run(debug=True,threaded=True,host='0.0.0.0',port=5340)")
                                                                         
                                                            except:
                                                                 print("Writing the multiple node data request error")
                                              config1 = configparser.ConfigParser() 
                                              config1.optionxform = str
                                              settings = ['Unit','Service','Install']
                                              config1.add_section(settings[0]) # Getting the section added into the list topic 
                                              config1.set(settings[0],'Description',"Multiple_node_data_projection") 
                                              config1.set(settings[0],'After',str(mode))
                                              #Service 
                                              config1.add_section(settings[1])
                                              config1.set(settings[1],'Type','idle')
                                              config1.set(settings[1],'WorkingDirectory',Working_path1)
                                              config1.set(settings[1],'User',str(device_name))
                                              config1.set(settings[1],'ExecStart',str(Python_exc_path+Execute_path1))
                                              config1.set(settings[1],'WantedBy','always')
                                              #Install 
                                              config1.add_section(settings[2])
                                              config1.set(settings[2],'WantedBy',str(mode))
                                              configfile1 = open(Generate_path+"/Multiple_node_data_projection.service",'w')
                                              config1.write(configfile1)
                                              os.system("sudo chmod -R 777 "+Working_path)   
                                              os.system("sudo chmod -R 777 "+Generate_path+"/Multiple_node_data_projection.service")
                                              os.system("sudo cp "+path_rlib+"roboreactmaster.py -t "+Working_path)  
                                              os.system("sudo cp "+path_rlib+"authenticationapi_request.py -t "+Working_path)
                                              list_fdb_path = "/home/"+os.listdir("/home/")[0]+"/Face_db/"
                                              path_list = os.listdir(list_fdb_path)
                                              try:
                                                   for fdb in path_list:
                                                         print("Moving path of face database into the system")
                                                         os.system("sudo cp "+list_fdb_path+fdb+" -t "+Working_path+"/") 
                                              except:
                                                   print("Face path database cannot remove")                                                                   
                                              OS_data_request()
                                        
           except:
                print("Error server connection")            

def Restart_request():
             try: 
                  res_restart_devices = requests.get('https://roboreactor.com/device_restart_status')
                  data_restart_status =  res_restart_devices.json()
                  device_restart = data_restart_status.get(Account_data) 
                  #print(device_restart)        
                  if device_restart.get('Restart_project') == "ON":
                                    print("Activate the onchange request")  
                                    Path_project = device_restart.get("Path_project") # Getting the path data      
                                    #Getting the Path splitter 
                                    list_path = Path_project.split("/") # Getting the first path remove
                                    list_path.remove(list_path[0])
                                    #checking the length 
                                    Project_name = str(list_path[len(list_path)-1]) # Getting the Project path 
                                    if len(list_path) == 4:
                                            print("Enable project to start....")
                                            #file = open("Test_detect_command.txt",'w')
                                            #file.write("Data_test_on_restart "+Project_name)
                                            try:
                                                os.system("sudo systemctl enable "+Project_name+".service") # Getting the project_name enable 
                                                os.system("sudo systemctl restart "+Project_name+".service") # Getting the Project_name restart 
                                                os.system("sudo systemctl status "+Project_name+".service") # Getting the status of the Project name 
                                            except:
                                                print("Error enable project")
                                                                                         
                                            send_activation_restart = {Account_data:{'Restart_project':"OFF","Path_project":Path_project}}  
                                            restart_state_off = requests.post("https://roboreactor.com/device_restart",json=send_activation_restart)
                                            print(restart_state_off.json()) # restart status 
                                            try:
                                                os.system("sudo systemctl enable "+"Multiple_node_data_projection.service") # Getting the project_name enable 
                                                os.system("sudo systemctl restart "+"Multiple_node_data_projection.service") # Getting the Project_name restart 
                                                os.system("sudo systemctl status "+"Multiple_node_data_projection.service") # Getting the status of the Project name 
                                            except:
                                                print("Error enable project")
                                                          
                                            OS_data_request()      
             except:
                 print("Error server connection restart")
def Stop_request():
     for i in count(0):
  
            try:
                res_stop_project = requests.get("https://roboreactor.com/device_stop_project_state")  
                device_stop_project = res_stop_project.json().get(Account_data)  # json type data  check 
                if device_stop_project != "None": # Getting data check to avoid none type data 
                       print("Active stop project")
                       print(device_stop_project)
                       if device_stop_project.get("Stop_project") =="ON":
                                            print("Trigger off switch project")
                                            Path_project = device_stop_project.get("Path_project")  
                                            list_local_path = Path_project.split("/")   #Getting the list of the path components 
                                            list_local_path.remove(list_local_path[0]) # remove the first list data 
                                            if len(list_local_path) == 4:
                                                     Project_name = list_local_path[len(list_local_path)-1]
                                                     #file = open("Test_stopping_service.txt",'w') # Getting the 
                                                     #file.write("Testing_stop_service "+str(Project_name)) # Getting the stopping service status active
                                                     #Running the disable command function to disable service on the linux
                                                     try: 
                                                         os.system("sudo systemctl disable "+str(Project_name))
                                                         os.system("sudo systemctl stop "+str(Project_name))  
                                                         os.system("sudo systemctl status "+str(Project_name))
                                                     except:
                                                          print("Error disable project")   
                                                     send_stop_project = {Account_data:{"Stop_project":"OFF","Path_project":Path_project}}
                                                     Stop_project_data  = requests.post("https://roboreactor.com/device_stop_project",json=send_stop_project) # Sending the off command data
                                                     print(Stop_project_data.json())
                                                     try: 
                                                         os.system("sudo systemctl disable "+"Multiple_node_data_projection.service")
                                                         os.system("sudo systemctl stop "+"Multiple_node_data_projection.service")  
                                                         os.system("sudo systemctl status "+"Multiple_node_data_projection.service")
                                                     except:
                                                          print("Error disable project") 
                                                     OS_data_request()

            except:  
                print("Error server connection to stop the project")
def upload_maneger():
  for i in count(0):
    try:
        user = device_name
        res_update = requests.get("https://roboreactor.com/software_update")  # Update software from the request
        software_update = res_update.json().get(Account_data) # Getting the data of the request
          
        if software_update !="None":
              if software_update == {}:
                       print("No data inside the payload")
                           
              if software_update !={}:
                   
                      print("Data in payload update",software_update)
                      if software_update.get('upload') == "ON":
                                     data_soft = software_update.get("github") # Getting the github link data to run in the git clone update the new middleware   
                                     print(data_soft) # Clone here
                                     firmware_inside = os.listdir("/home/"+user+"/") # Getting the firmware update from the   
                                     print(firmware_inside)
                                     middle_ware_name = data_soft.split("/")[len(data_soft.split("/"))-1]
                                     if middle_ware_name in firmware_inside:
                                              #Check if there is a data token secret key inside the system or not then run the command to back up the datatoken secret key to the home directory 
                                              token_inside = os.listdir("/home/"+user+"/"+middle_ware_name)
                                              if "data_token_secret.json" in token_inside: 
                                                       print("Move the data_token_secret.json to the home directory of the computer") 
                                                       os.system("sudo mv /home/"+user+"/"+middle_ware_name+"/data_token_secret.json -t "+"/home/"+user)  # Remove the data_token_secret_key to the home directory                                           
                                              os.system("sudo rm -rf /home/"+user+"/"+middle_ware_name)  
                                              os.system("git -C /home/"+user+ " clone "+str(data_soft)) 
                                              os.system("sudo mv /home/"+user+"/data_token_secret.json -t "+"/home/"+user+"/"+middle_ware_name)

                                     if middle_ware_name not in firmware_inside:         
                                              os.system("git -C /home/"+user+ " clone "+str(data_soft)) # Clone the github data into the computer
                                              if "data_token_secret.json" in token_inside:
                                                         os.system("sudo mv /home/"+user+"/data_token_secret.json -t "+"/home/"+user+"/"+middle_ware_name)  

                                     payload_update = {Account_data:{'upload':'OFF','github':data_soft}}
                                     try:
                                             res_off_update = requests.post("https://roboreactor.com/software_update_stop",json=payload_update) # Sending back the payload update function
                                     except:
                                          print("Server fail connection on update!")

                     
    except:
          print("Error connecting server")
def Turn_off_data(user,extract_data,data_joint_update,code_gens,Live_URL):
          extract_data['status'] = "OFF"
          print("Updated status joint generator ", extract_data)
          data_joint_update[Account_data] = extract_data
          res = requests.get(Live_URL+"/Joint_data_request",json=data_joint_update)
          print(res.json())  
          code_gens = open("/home/"+user+"/Joint_remote_controller.py",'a')   # Generate the code here running in the loop check when status is on                             
def Joint_remote_control():
      user = device_name
      for i in count(0):
             try:

                   account_payload = {'email':Account_data} # Container account data 
                   res = requests.post(Live_URL+"/run_joint",json=account_payload)
                   extract_data = res.json() # Get the extracted payload request from the account payload data 
                   print(extract_data)
                   project_name = list(extract_data.get('data_joint'))[0]               
                   host_name = list(extract_data.get('data_joint').get(project_name))[0] 
                   #print(project_name,host_name)
                   joint_dats = extract_data.get('data_joint').get(project_name).get(host_name) 
                   #print(joint_dats) # Get the internal joint data request
                   #Check status of the statement on the payload to start on and off 
                   #Record the json data back to the user account 
                   data_joint_update = {} #Keep the data joint update 
                   if extract_data['status'] == "ON":
                       #Working on something while status on 
                       print("Working on the code generator now generating code")
                       try:
                           print("Removing old file....")
                           os.remove("/home/"+user+"/Joint_remote_controller.py")
                       except:
                           print("File not found") 
                           
                       print("Now generating the code for joint remote control! ...")
                       #code_gens = open("/home/"+user+"/urdf_creator_template/Joint_remote_controller.py",'a')
                       #code_gens.write("import os"+"\nimport json"+"\nimport requests"+"\nimport serial"+"\nimport pyfirmata")
                       #code_gens = open("/home/"+user+"/urdf_creator_template/Joint_remote_controller.py",'a')
                       #First task get the serial USB port 
                       
                       for  joints in list(joint_dats):
                          
                          board_controller = list(joint_dats.get(joints))[0]    
                          board_catg[joints] = board_controller
                          port_type = joint_dats.get(joints).get(board_controller).get('communication') 
                          #Get the data from the port 
                          if board_controller == "MCUs":   
                                 print(joints,joint_dats.get(joints).get(board_controller))  
                                 #Get the commmunication data_type 
                                 #Mem the data of the joint function
                                 if port_type == "Serial":
                                                                        
                                       port_address = joint_dats.get(joints).get(board_controller).get('Port_address')  # Get the serial usb port or the data of the 
                                       #check port type port data 
                                       print("Check port type and port data ",port_type,port_address) # Check port data and port type 
                                       serial_group[joints] = port_address # Check the port address data of the
                                       serial_separator[port_address] = joints  #Get the intercept address include as list in here 
                                       serial_list[port_type] = list(serial_separator)  # get the list of the serial ssperator in here to running in the loop generate the control function 
                                       Commu_check_data[joints] = port_type+","+board_controller
                                       print("Data_port_container",serial_group,serial_separator,serial_list,Commu_check_data)# Get the serial data list group and separator           
                                       feed_back_sensor_check = joint_dats.get(joints).get(board_controller).get('Pin_analog_sensor') # Check of the pin analog sensor is exist 
                                       if feed_back_sensor_check != {}:
                                                       print("Check the data of the feedback sensor") #After found the data of the  feedback sensor extract them and categorized base on signal and purpose 
                                                       print("Feedback_sensor data ",feed_back_sensor_check)
                                                       feedback_sense = joint_dats.get(joints).get(board_controller).get("Signal_fbs")
                                                       print("Check type of signal input feedback sensor ",feedback_sense) # Get the feedback sensor type of data 
                                                       feedback_sensor_type[joints] = {feedback_sense:feed_back_sensor_check} # Get the feedback sensor 
                                                       print("Feed_back group check signal category ",feedback_sensor_type)
                                                        
                          if board_controller == "SBC":   
                                 print(joints,joint_dats.get(joints).get(board_controller))        
                                 #Get the communication data_type 
                                 #Mem the data of joint parameter function
                                 if port_type == "I2C":     
                                           print("I2C communication data mem function address port") 
                                           board_i2c_controller = joint_dats.get(joints).get(board_controller).get('i2c_sbc_devices') 
                                           serial_group[joints] = joint_dats.get(joints).get(board_controller).get('i2c_sbc_devices') 
                                           serial_separator[board_i2c_controller] = joints
                                           serial_list[port_type] = list(serial_separator)
                                           Commu_check_data[joints] = port_type+","+board_controller  
                                           print("Data_i2c_container",serial_group,serial_separator,serial_list,Commu_check_data)

                          
                       #for joints_com in list(Commu_check_data):
                       print("Generating library code.....")
                       code_gens = open("/home/"+user+"/Joint_remote_controller.py",'a')
                       if "I2C" in list(serial_list):
                                           code_gens.write("import os"+"\nimport json"+"\nimport requests"+"\nimport serial"+"\nimport busio"+"\nimport smbus"+"\nimport pyfirmata"+"\nfrom board import SCL, SDA"+"\nfrom adafruit_motor import servo"+"\nfrom adafruit_pca9685 import PCA9685"+"\nfrom gpiozero.pins.pigpio import PiGPIOFactory"+"\nfrom gpiozero import AngularServo,LED"+"\nfrom itertools import count"+"\nimport busio"+"\nimport smbus"+"\nfrom board import SCL,SDA"+"\nfrom adafruit_motor import servo"+"\nfrom adafruit_pca9685 import PCA9685")
                                           #code_gens.write("import os"+"\nimport json"+"\nimport requests"+"\nimport serial"+"\nimport busio"+"\nimport smbus"+"\nimport pyfirmata"+"\nfrom board import SCL, SDA"+"\nfrom adafruit_motor import servo"+"\nfrom adafruit_pca9685 import PCA9685"+"\nfrom gpiozero.pins.pigpio import PiGPIOFactory"+"\nfrom gpiozero import AngularServo,LED"+"\nfrom itertools import count")
                                           code_gens = open("/home/"+user+"/Joint_remote_controller.py",'a')     
                                           #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
                                                        # Generate header and serial port controller 
                                           code_gens.write("\ntry:")             
                                           for joints_com in list(Commu_check_data):
                                                        #get the data joint communication in the loop to generate the code inside 
                                                        print("Generating the body code controller i2c found......")  
                                                        #Generate the joint data
                                                        board_controllers = Commu_check_data.get(joints_com).split(",")[1]  #Get the data of the board controller                    
                                                        if board_controllers == "SBC":
                                                                    print("Check control data")
                                                                    if Commu_check_data.get(joints_com).split(",")[0] == "I2C": 
                                                                                       print("Generate the i2c data of joints ......") 
                                                                                       if serial_group.get(joints_com)  == "PCA_9685":
                                                                                                    print("Generating controller board ",serial_group.get(joints_com))
                                                                                                    #code_gens.write("\ntry:"+"\n\thardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]+" = pyfirmata.ArduinoMega('"+port_ad+"')")
                                                                                                    code_gens.write("\n\ti2c = busio.I2C(SCL, SDA)")
                                                                                                    code_gens.write("\n\tpca = PCA9685(i2c)") 
                                                                                                    code_gens.write("\n\tpca.frequency = 50")   
                                                                                                    #code_gens = open("/home/"+user+"/urdf_creator_template/Joint_remote_controller.py",'a')     
            
                                                        if board_controllers == "MCUs": 
                                                                    print("Check control data")  
                                                                    if Commu_check_data.get(joints_com).split(",")[0] == "Serial": 
                                                                                       print("Generate the serial data of joints....")
                                                                                       port_ad = serial_group.get(joints_com)
                                                                                       print("Serial port address ",port_ad)
                                                                                       code_gens.write("\n\thardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]+" = pyfirmata.ArduinoMega('"+port_ad+"')")
                                                                                       Check_hardware_board["hardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]] = port_ad                                       
                                                                    #Get the sensor type of the feedback sensor 
                                                                    if feedback_sensor_type != {}:
                                                                             #Check the list of the feedback sensor 
                                                                             for joints in list(feedback_sensor_type): 
                                                                                           print("Get the total feedback sensor interception from each joint data ") # Check the intercept of the sensor input list to detect the sensor type enable 
                                                                                           print(joints,feedback_sensor_type[joints])
                                                                                           #feedback_signal_intercept[list(feedback_signal_intercept[joints])[0]] = joints    #Get the joints and signal integration 

                                           #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.
                                                            #Generate the joint controller algorithm  
                                           for joints_com in list(Commu_check_data): 
                                                           print("Generate the joint function control algorithm")
                                                           print(Commu_check_data.get(joints_com).split(",")[1])  
                                                           
                                                           if Commu_check_data.get(joints_com).split(",")[1] == "SBC":
                                                                                 
                                                                                 if Commu_check_data.get(joints_com).split(",")[0] == "I2C": 
                                                                                                         print("Generate the i2c control board function")
                                                                                                         pin_data_sbc = joint_dats.get(joints_com).get(Commu_check_data.get(joints_com).split(",")[1]).get("i2c_sbc_pin")                      
                                                                                                         print(pin_data_sbc)
                                                                                                         code_gens.write("\n\t"+joints_com+"_servo_"+Commu_check_data.get(joints_com).split(",")[0]+" = servo.Servo(pca.channels["+pin_data_sbc+"])")           
                                                           if Commu_check_data.get(joints_com).split(",")[1] == "MCUs":
                                                                                 if Commu_check_data.get(joints_com).split(",")[0] == "Serial":
                                                                                                         print(Commu_check_data)
                                                                                                         print("Generate the serial control board function") 
                                                                                                         mcus_IO = joint_dats.get(joints_com).get(board_controller).get('mcus_IO')
                                                                                                         mcus_pins = joint_dats.get(joints_com).get(board_controller).get('mcus_pins') 
                                                                                                         mcus_fam = joint_dats.get(joints_com).get(board_controller).get('mcus_families')
                                                                                                         mcus_name = joint_dats.get(joints_com).get(board_controller).get('mcus_code_number') + joint_dats.get(joints_com).get(board_controller).get('mcus_package')
                                                                                                         #Get the mcus_name data combine with the 2 parts package 
                                                                                                         res_map = requests.get(mcus_pin_map) 
                                                                                                         pin_map = res_map.json().get(mcus_fam).get(mcus_name)
                                                                                                         #check the mcus_IO data 
                                                                                                         if mcus_IO == "Servo_PWM_output":
                                                                                                                   io_function = data_io_control.get(mcus_IO)
                                                                                                                   mcus_pins_data = mcus_pins.get('pin_name') # Get the pin name in real-time
                                                                                                                   code_gens.write("\n\t"+joints_com+"_"+joint_dats.get(joints_com).get(board_controller).get("mcus_IO")+" = hardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]+".get_pin('d:"+str(pin_map.get(mcus_pins_data))+":"+io_function+"')")
                                                                                                                   #Get the pins data of the name of joint 

                                                                                                         if mcus_IO == "PWM_output":
                                                                                                                   #Get the pwm data of the serial control of the DC motor
                                                                                                                   io_function = data_io_control.get(mcus_IO)   
                                                                                                                   for io_list in list(mcus_pins):
                                                                                                                          pin_physical_PI = mcus_pins.get(io_list).get('pin_name') #3 Get the pins name         
                                                                                                                          code_gens.write("\n\t"+joints_com+"_"+joint_dats.get(joints_com).get(board_controller).get("mcus_IO")+"_"+io_list+" = hardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]+".get_pin('d:"+str(pin_map.get(pin_physical_PI))+":"+str(io_function)+"')")                   
                                                            
                       
                                           #Turn_off_data(code_gens)                           
                       
                       if "I2C" not in list(serial_list):
                                           code_gens.write("import os"+"\nimport json"+"\nimport requests"+"\nimport serial"+"\nimport pyfirmata"+"\nfrom itertools import count") 
                                           code_gens = open("/home/"+user+"/Joint_remote_controller.py",'a')
                                           code_gens.write("\ntry:")
                                           #for joints_com in list(Commu_check_data):
                                           print("Genereating the body code controller serial and other found....")
                                           #board_controllers = Commu_check_data.get(joints_com).split(",")[1]  #Get the data of the board controller 
                                           #if board_controllers == "MCUs":
                                           for port_ad in serial_list.get("Serial"):     
                                                                    #print("Check control data")  
                                                                    #if Commu_check_data.get(joints_com).split(",")[0] == "Serial": 
                                                                                       print("Generate the serial data of joints....")
                                                                                       #port_ad = serial_group.get(joints_com)
                                                                                       print("Serial port address ",port_ad)
                                                                                       code_gens.write("\n\thardware_"+port_ad.split("/")[len(port_ad.split
                                                                                       
                                                                                        ("/"))-1]+" = pyfirmata.ArduinoMega('"+port_ad+"')")
                                                                                       Check_hardware_board["hardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]] = port_ad 
                                           if feedback_sensor_type != {}:
                                                                             #Check the list of the feedback sensor 
                                                                             
                                                                             #Check the list of the feedback sensor 
                                                                             for joints in list(feedback_sensor_type): 
                                                                                           print("Get the total feedback sensor interception from each joint data ") # Check the intercept of the sensor input list to detect the sensor type enable 
                                                                                           print(joints,list(feedback_sensor_type[joints])[0])
                                                                                           feedback_signal_intercept[list(feedback_sensor_type[joints])[0]] = joints    #Get the joints and signal integration 
                                                                                           print(feedback_signal_intercept)
                                                                             
                                                                             for joints in list(feedback_sensor_type): 
                                                                                                  print("Preparing the input of the feedback sensor data and classify each type of the sensor") 
                                                                                                  signal_type = list(feedback_sensor_type[joints])[0] 
                                                                                                  if signal_type == "Analog-read": 
                                                                                                              print("Generate analog input code ")                                                                              
                                                                                                              #Get the function of the analog input iteration
                                                                                                              
                                                                                                              get_analog_pins = feedback_sensor_type[joints].get(signal_type).get('mcus_analog_pin') #.get('mcus_analog_pin')
                                                                                                              #print("Get pin number ",get_analog_pins);
                                                                                                              code_gens.write("\n\t"+joints+"_"+signal_type.split("-")[0]+"_"+signal_type.split("-")[1]+" = "+str(get_analog_pins)) #Set the analog define parameter value input 
                                                                                                              #Get the analog values save  
                                                                                                               
                                                                             for signal_feed in list(feedback_signal_intercept): 
                                                                                                   print("Generate signal feedback intercept ")
                                                                                                   if signal_feed == "Analog-read":
                                                                                                                 print("Generate the feedback iteration code ...") 
                                                                                                                 for board_hardware in list(Check_hardware_board): 
                                                                                                                             code_gens.write("\n\t"+"Sensor"+"_"+signal_feed.split("-")[0]+"_"+signal_feed.split("-")[1] +"_"+board_hardware.split("_")[1]+" = pyfirmata.util.Iterator("+board_hardware+")") # Get the sensor analog sensor itereation  
                                                                                                                             code_gens.write("\n\t"+"Sensor"+"_"+signal_feed.split("-")[0]+"_"+signal_feed.split("-")[1]+"_"+board_hardware.split("_")[1]+".start()") #Start the interation of the analog sensor input 
                                                                                                                             #Get the lst of the analog sensor with the defined value parameter sensor 
                                                                                                                             for joints in list(feedback_sensor_type): 
                                                                                                                                             print("Preparing the input of the feedback sensor data and classify each type of the sensor") 
                                                                                                                                             signal_type = list(feedback_sensor_type[joints])[0] 
                                                                                                                                             if signal_type == "Analog-read": 
                                                                                                                                                      print("Generate analog input code ")                                                                              
                                                                                                                                                      #Get the function of the analog input iteration 
                                                                                                                                                      #code_gens.write("\n\t"+joints+"_"+signal_type.split("-")[0]+"_"+signal_type.split("-")[1]+" = 0")
                                                                                                                                                      code_gens.write("\n\t"+board_hardware+".analog["+joints+"_"+signal_type.split("-")[0]+"_"+signal_type.split("-")[1]+"].enable_reporting()") # Get the analog sensor feedback setting                                             
                                           for joints_com in list(Commu_check_data):
                                                        if Commu_check_data.get(joints_com).split(",")[1] == "MCUs":
                                                                                 if Commu_check_data.get(joints_com).split(",")[0] == "Serial":
                                                                                                         print(Commu_check_data)
                                                                                                         print("Generate the serial control board function") 
                                                                                                         mcus_IO = joint_dats.get(joints_com).get(board_controller).get('mcus_IO')
                                                                                                         mcus_pins = joint_dats.get(joints_com).get(board_controller).get('mcus_pins') 
                                                                                                         mcus_fam = joint_dats.get(joints_com).get(board_controller).get('mcus_families')
                                                                                                         mcus_name = joint_dats.get(joints_com).get(board_controller).get('mcus_code_number') + joint_dats.get(joints_com).get(board_controller).get('mcus_package')
                                                                                                         #Get the mcus_name data combine with the 2 parts package 
                                                                                                         res_map = requests.get(mcus_pin_map) 
                                                                                                         pin_map = res_map.json().get(mcus_fam).get(mcus_name)
                                                                                                         #check the mcus_IO data 
                                                                                                         if mcus_IO == "Servo_PWM_output":
                                                                                                                   io_function = data_io_control.get(mcus_IO)
                                                                                                                   mcus_pins_data = mcus_pins.get('pin_name') # Get the pin name in real-time
                                                                                                                   code_gens.write("\n\t"+joints_com+"_"+joint_dats.get(joints_com).get(board_controller).get("mcus_IO")+" = hardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]+".get_pin('d:"+str(pin_map.get(mcus_pins_data))+":"+io_function+"')")
                                                                                                                   #Get the pins data of the name of joint 
                            
                                                                                                         if mcus_IO == "PWM_output":
                                                                                                                   #Get the pwm data of the serial control of the DC motor
                                                                                                                   io_function = data_io_control.get(mcus_IO)   
                                                                                                                   for io_list in list(mcus_pins):
                                                                                                                          pin_physical_PI = mcus_pins.get(io_list).get('pin_name') #3 Get the pins name         
                                                                                                                          code_gens.write("\n\t"+joints_com+"_"+joint_dats.get(joints_com).get(board_controller).get("mcus_IO")+"_"+io_list+" = hardware_"+port_ad.split("/")[len(port_ad.split("/"))-1]+".get_pin('d:"+str(pin_map.get(pin_physical_PI))+":"+str(io_function)+"')")                   
                                           #Turn_off_data(user,extract_data,data_joint_update,code_gens,Live_URL)          
                       code_gens.write("\nexcept:\n\t\tprint('Package iot control server not found!')")                                                                                                                                                                        
                       code_gens.write("\nfor i in count(0):"+"\n\ttry:"+"\n\t\tres = requests.get('https://roboreactor.com/package_iot_control')"+"\n\t\tjoint_parameters = res.json()"+"\n\t\temail = list(joint_parameters)[0]"+"\n\t\tproject_name = list(joint_parameters.get(email))[0]"+"\n\t\tjoint_type = list(joint_parameters.get(email).get(project_name))[0]"+"\n\t\tjoint_motion = joint_parameters.get(email).get(project_name).get(joint_type)") 
                       #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                                          #Generate Joint  control algorithm data 
                       
                       
                       for joints_data in list(Commu_check_data):
   
                                       if Commu_check_data.get(joints_data).split(",")[1] == "SBC":
                                                              print("Generate single board computer joint algorithm") 
                                                              code_gens.write("\n\t\t"+joints_data+" = joint_motion.get('"+joints_data+"')")  # Get the joint motion control 
                                                              code_gens.write("\n\t\t"+"print('Joint "+joints_data+"',"+joints_data+",abs(float("+joints_data+")))")
                                                              #Get joint status
                                                              code_gens.write("\n\t\tif float("+joints_data+") >= 0:")  
                                                              code_gens.write("\n\t\t\t"+joints_data+"_servo_"+Commu_check_data.get(joints_data).split(",")[0]+".angle = (abs(float("+joints_data+")))") 
                                                              code_gens.write("\n\t\tif float("+joints_data+") <= 0:")  
                                                              code_gens.write("\n\t\t\t"+joints_data+"_servo_"+Commu_check_data.get(joints_data).split(",")[0]+".angle = (90+abs(float("+joints_data+")))")           
                                       if Commu_check_data.get(joints_data).split(",")[1] == "MCUs":
                                                              print("Generate microcontroller joint algorithm") 
                                                              if Commu_check_data.get(joints_data).split(",")[0] == "Serial":  # Get  I2C ata communication     
                                                                                  mcus_IO = joint_dats.get(joints_data).get(board_controller).get('mcus_IO')
                                                                                  if mcus_IO == "Servo_PWM_output":    
                                                                                           print("Generating pin remote control")
                                                                                           if feedback_sensor_type != {}:
                                                                                                                 print("Generating the analog reader for ")
                                                                                                                 for signal_feed in list(feedback_signal_intercept): 
                                                                                                                             print("Generate signal feedback intercept ")
                                                                                                                             if signal_feed == "Analog-read":
                                                                                                                                            print("Generate the feedback iteration code ...") 
                                                                                                                                            for board_hardware in list(Check_hardware_board):
                                                                                                                                                               print("Generate the algorithm for the analog signal processing") 
                                                                                                                                                               #Classify type of the joint to set the control algorithm 
                                                                                                                                                               check_joint_type = list(joint_dats.get(joints_data).get(board_controller).get("Joints_type"))[0] #Get joint type to classify the control algorithm and tuning the optimization function 
                                                                                                                                                               if check_joint_type == "revolute":
                                                                                                                                                                               print("Generate the PID control algorithm")
                                                                                                                                                                               code_gens.write("\n\t\t"+"Analog_signal_"+joints_data+" = "+board_hardware+".analog["+joints_data+"_"+signal_feed.split("-")[0]+"_"+signal_feed.split("-")[1]+"].read()") 
                                                                                                                                                                               code_gens.write("\n\t\t"+"if Analog_signal_"+joints_data+" != None:"+"\n\t\t\t"+"print(float("+"Analog_signal_"+joints_data+")*360)")         
                                                                                           code_gens.write("\n\t\t"+joints_data+" = joint_motion.get('"+joints_data+"')")  # Get the joint motion control 
                                                                                           code_gens.write("\n\t\t"+"print('Joint "+joints_data+"',"+joints_data+",abs(float("+joints_data+")))")
                                                                                           #Get joint status
                                                                                           code_gens.write("\n\t\tif float("+joints_data+") >= 0:")  
                                                                                           code_gens.write("\n\t\t\t"+joints_data+"_"+joint_dats.get(joints_data).get(board_controller).get("mcus_IO")+".write(abs(float("+joints_data+")))") 
                                                                                           code_gens.write("\n\t\tif float("+joints_data+") <= 0:")  
                                                                                           code_gens.write("\n\t\t\t"+joints_data+"_"+joint_dats.get(joints_data).get(board_controller).get("mcus_IO")+".write(90+abs(float("+joints_data+")))")  
            
                                                                                  if mcus_IO == "PWM_output":
                                                                                                        print("Generating pin remote control")
                                                                                                        if feedback_sensor_type != {}:
                                                                                                                 print("Generating the analog reader for ")
                                                                                                                 for signal_feed in list(feedback_signal_intercept): 
                                                                                                                             print("Generate signal feedback intercept ")
                                                                                                                             if signal_feed == "Analog-read":
                                                                                                                                            print("Generate the feedback iteration code ...") 
                                                                                                                                            for board_hardware in list(Check_hardware_board):
                                                                                                                                                               print("Generate the algorithm for the analog signal processing") 
                                                                                                                                                               #Classify type of the joint to set the control algorithm 
                                                                                                                                                               check_joint_type = list(joint_dats.get(joints_data).get(board_controller).get("Joints_type"))[0] #Get joint type to classify the control algorithm and tuning the optimization function 
                                                                                                                                                               if check_joint_type == "revolute":
                                                                                                                                                                               print("Generate the PID control algorithm")
                                                                                                                                                                               code_gens.write("\n\t\t"+"Analog_signal_"+joints_data+" = "+board_hardware+".analog["+joints_data+"_"+signal_feed.split("-")[0]+"_"+signal_feed.split("-")[1]+"].read()") 
                                                                                                                                                                               code_gens.write("\n\t\t"+"if Analog_signal_"+joints_data+" != None:"+"\n\t\t\t"+"print(float("+"Analog_signal_"+joints_data+")*360)")      
                                                                                                        io_function = joint_dats.get(joints_data).get(board_controller).get(mcus_IO) 
                                                                                                        mcus_pins = joint_dats.get(joints_data).get(board_controller).get('mcus_pins') 
                                                                                                        mcus_fam = joint_dats.get(joints_data).get(board_controller).get('mcus_families')
                                                                                                        mcus_name = joint_dats.get(joints_data).get(board_controller).get('mcus_code_number') + joint_dats.get(joints_data).get(board_controller).get('mcus_package')
                                                                                                        res_map = requests.get(mcus_pin_map) 
                                                                                                        pin_map = res_map.json().get(mcus_fam).get(mcus_name)  
                                                                                                        #for io_list in list(mcus_pins):
                                                                                                        #            print(io_list)
                                                                                                        code_gens.write("\n\t\t"+joints_data+" = joint_motion.get('"+joints_data+"')")
                                                                                                        code_gens.write("\n\t\t"+"print('Joint "+joints_data+"',"+joints_data+",abs(float("+joints_data+")))")
                                                                                                        #PD control algorithm 
                                                                                                        #Control the position of the motor based on the pins control function on the H-bridge motor driver  control 
                                                                                                        polar_switcher = {"Pin_R":"Pin_L","Pin_L":"Pin_R"}  #Pin connection switcher of the motor H-bridge
                                                                                                        logic_polar = {"max":{"Pin_R":'0',"Pin_L":joints_data},"min":{"Pin_L":'0',"Pin_R":joints_data}}
                                                                                                        code_gens.write("\n\t\t"+"if float("+joints_data+") == 0:")
                                                                                                        for io_list in list(mcus_pins):
                                                                                                                   print(io_list)                                                                     
                                                                                                                   code_gens.write("\n\t\t\t"+joints_data+"_"+joint_dats.get(joints_data).get(board_controller).get("mcus_IO")+"_"+io_list+".write(0)")#("\n\t\t\t"+joints_data+"_"+joint_dats.get(joints_data).get("mcus_IO")+"_"+polar_switcher.get(io_list)+".write(0)")
                                                                                                        code_gens.write("\n\t\t"+"if float("+joints_data+") > 0:")
                                                                                                        for io_list in list(mcus_pins):
                                                                                                                    print(io_list)
                                                                                                                    gpio_logic_max = logic_polar.get('max') # Get the max logic polar 
                                                                                                                    code_gens.write("\n\t\t\t"+joints_data+"_"+joint_dats.get(joints_data).get(board_controller).get("mcus_IO")+"_"+io_list+".write(abs(float("+gpio_logic_max.get(io_list)+"))/360)")
                                                                                                        code_gens.write("\n\t\t"+"if float("+joints_data+") < 0:")
                                                                                                        for io_list in list(mcus_pins):
                                                                                                                               print(io_list)
                                                                                                                               gpio_logic_min = logic_polar.get('min')
                                                                                                                               code_gens.write("\n\t\t\t"+joints_data+"_"+joint_dats.get(joints_data).get(board_controller).get("mcus_IO")+"_"+io_list+".write(abs(float("+gpio_logic_min.get(io_list)+"))/360)")                    
                                       #Generate the systemd file                                                                
                                       #Generate the systemd confgurection file 
                                       print("Generrating the systemd file 4sec.......")        
                                       Generate_path = "/usr/lib/systemd/system/" 
                                       project_name = 'Joint_remote_controller'   
                                       mode = 'multi-user.target' 
                                       Python_exc_path = "/usr/bin/python3 "
                                       Working_path1 = "/home/"+user+"/" 
                                       #Working_path = "/home/"+device_name+"/Roboreactor_projects/"+Project_name
                                       Execute_path = "/home/"+user+"/"+project_name+".py"  
                                       #Execute_path1 = "/home/"+device_name+"/RoboreactorGenFlow"+"/Multiple_node_data_projection.py" 
                                       config = configparser.ConfigParser() 
                                       config.optionxform = str
                                       settings = ['Unit','Service','Install']
                                       #Unit
                                       config.add_section(settings[0]) # Getting the section added into the list topic 
                                       config.set(settings[0],'Description',"Project:"+str(project_name)) 
                                       config.set(settings[0],'After',str(mode))
                                       #Service 
                                       config.add_section(settings[1])
                                       config.set(settings[1],'Type','idle')
                                       config.set(settings[1],'WorkingDirectory',Working_path1)
                                       config.set(settings[1],'User',str(user))
                                       config.set(settings[1],'ExecStart',str(Python_exc_path+Execute_path))
                                       config.set(settings[1],'WantedBy','always')
                                       #Install 
                                       config.add_section(settings[2])
                                       config.set(settings[2],'WantedBy',str(mode))
                                       configfile = open(Generate_path+"/"+project_name+".service",'w')
                                       config.write(configfile)
                                       os.system("sudo chmod -R 777 "+Generate_path+"/"+project_name+".service")
                                       os.system("sudo systemctl daemon-reload") 
                                       os.system("sudo systemctl enable "+project_name+".service") 
                                       os.system("sudo systemctl restart "+project_name+".service")
                                       Turn_off_data(user,extract_data,data_joint_update,code_gens,Live_URL)
                       #Processing the joint data of fedback sensor to send back the data to the main system                                                                
                       if feedback_sensor_type !={}:
                               #Recall the function of the joint data to add data into the code 
                               for joints in list(feedback_sensor_type):
                                                         print("Preparing the input of the feedback sensor data and classify each type of the sensor") 
                                                         signal_type = list(feedback_sensor_type[joints])[0] 
                                                         if signal_type == "Analog-read": 
                                                                    print("Generate analog input code ")                                                                              
                                                                    payload_joints_container.append("'"+joints+"':{'"+signal_type+"':"+"float(Analog_signal_"+joints+")*360},")       
                                                                    
                               #Generate the feedback code data to run the motion control into the web 
                               #In the process running procedure always check the data of index to detect the last value of the data in list and remove comma 
                               print("Feedback payload data ",payload_joints_container)
                               
                               for fbs in range(0,len(payload_joints_container)):
                                                   if payload_joints_container[fbs] != payload_joints_container[len(payload_joints_container)-1]:
                                                                                payload_feedback.append(payload_joints_container[fbs]) 
                                                   if payload_joints_container[fbs] == payload_joints_container[len(payload_joints_container)-1]: 
                                                                                payload_feedback.append(payload_joints_container[fbs].split(",")[0])                                                
                               
                               payload_feedback.append("}") 
                               data_combiner = "".join(payload_feedback) 
                               code_gens.write("\n\t\tAccount_data = open('/home/"+user+"/RoboreactorGenFlow/data_token_secret.json','r')") 
                               code_gens.write("\n\t\tdata_account = json.loads(Account_data.read()).get('Account')") 
                               code_gens.write("\n\t\tres = requests.post('"+Live_URL+"/feedback_sensor',json={data_account:"+data_combiner+"})") #Feedback data json   
                       code_gens.write("\n\texcept:\n\t\tprint('Package iot control server not found!')")                                                                                                                                                                        
                       code_gens.close()
                       #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>...
                                           # Activate OFF status data 
                      
                   if extract_data['status'] == "OFF":
                              print("Now status offline stop generating the code ")    

             except:
                print("Server not found on the post request to the web services")  

# Running multithread 
t1 = threading.Thread(target=Main_request)
t2 = threading.Thread(target=side_request) 
t3 = threading.Thread(target=Generate_request)
t4 = threading.Thread(target=Restart_request)
t5 = threading.Thread(target=Stop_request)
t6 = threading.Thread(target=upload_maneger)
t7 = threading.Thread(target=Joint_remote_control)
t1.start()
t2.start()
t3.start()
t4.start() 
t5.start() 
t6.start() 
t7.start() 
