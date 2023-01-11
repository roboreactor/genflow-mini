import os 
import jwt 
import json 
import socket
import requests 
import configparser 
import threading
import subprocess 
from itertools import count 
device_name = os.listdir("/home/")[0] # getting the device name data 
path_token = "/home/"+os.listdir("/home/")[0]+"/RoboreactorGenFlow/" # Getting the path token data 
path_rlib = "/home/"+os.listdir("/home/")[0]+"/Roboreactor_library/"
Current_device_data = {} 
data_transfer_OS = {}
#Getting the operating system and machine data of the user
os_platform = os.uname() # uname 

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
                                     if middle_ware_name not in firmware_inside:         
                                              os.system("sudo rm -rf /home/"+user+"/"+middle_ware_name) # Remove the middle ware name before added the new on into the computer 
                                              os.system("git -C /home/"+user+ " clone "+str(data_soft)) # Clone the github data into the computer
                                              os.system("sudo mv /home/"+user+"/data_token_secret.json -t "+"/home/"+user+"/"+middle_ware_name)  

                                     payload_update = {Account_data:{'upload':'OFF','github':data_soft}}
                                     try:
                                             res_off_update = requests.post("https://roboreactor.com/software_update_stop",json=payload_update) # Sending back the payload update function
                                     except:
                                          print("Server fail connection on update!")

                     
    except:
          print("Error connecting server")
# Running multithread 
t1 = threading.Thread(target=Main_request)
t2 = threading.Thread(target=side_request) 
t3 = threading.Thread(target=Generate_request)
t4 = threading.Thread(target=Restart_request)
t5 = threading.Thread(target=Stop_request)
t6 = threading.Thread(target=upload_maneger)
t1.start()
t2.start()
t3.start()
t4.start() 
t5.start() 
t6.start() 