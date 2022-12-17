import configparser
import json 
import os 
import sys  
import getpass
import os.path
from os import path 
#+++++++++++++++++Warning ! the file should created in authorized directory inorder to create the config file +++++++++++++++++++++++++++# 
user = os.listdir("/home/")[0]
Home_path = '/home/'+str(user)+"/" #Home path to get the config file and project setting outside the node generator
# Reading the path of the project config

Path = '/home/'+str(user)+"/Roboreactor_projects"
config = configparser.ConfigParser()
config.read(Path+'/config_project_path.cfg') 
path_project_config = config['Project_path']['path']   # Reading the path of the project 
Path_local = '/home/'+str(user)+"/Roboreactor_Gen_config"  # Generate the main path for config gen and code generator
print("Current project path",path_project_config)
f = open (Path+"/"+'node_generated.json', "r")
data_requested = json.loads(f.read())
try:
    os.mkdir(Path,mode=0o777) # Give permission to create path of directory
    #Getting the name of the face_recognition directory 
    config.read(Path_local+"/roboreactor_node/vision/face_recognition/facerec.cfg")
    face_path = config['face_rec_dat']['face_path'] 
    print(face_path)
  
except:
   print("Directory")
try:
   print("Start writing config file......") 
   config = configparser.ConfigParser()    
   config.add_section('Project_path')
   config.set('Project_path','path',Path) # Created the path file of config 
   configfile = open(Path+"/config_codegen.cfg",'w') # Reading the path file of the project 
   config.write(configfile)
   
except: 
   print("Configfile was created!")
   
config.read('config_codegen.cfg') 
path_config = config['Project_path']['path']
print("Reading current path:",path_config) # Reading current path file 
message_path = Path_local+"/roboreactor_node/message_node/"
vision_path = Path_local+"/roboreactor_node/vision/"
navigation_path = Path_local+"/roboreactor_node/navigation/"
motion_path = Path_local+"/roboreactor_node/motion/motor/"
audio_path = Path_local+"/roboreactor_node/audio/"
nlp_path = Path_local+"/roboreactor_node/nlp/"
serial_path = Path_local+"/roboreactor_node/Serialcom/"
Sensor_array_path = Path_local+"/roboreactor_node/sensor_array/"
Multiple_logic_path = Path_local+"/roboreactor_node/multiple_logic_node/"
Multi_cache_path = Path_local +"/roboreactor_node/multi_cache_node/"  
mem_multi_cache = [] #Mem multi cache node
list_path_project = os.listdir(path_project_config)
print("Project Path list",list_path_project)
# Pre library element for setting the lib data config
pre_lib = ['Create_node_pub','Create_node_sub','Camera_Qr_cache,Camera_multi_cache,Cache_server','Camera_pub_node','Face_recognition','Speaking_languages','Camera_yolo_pub_node','Camera_QR_sub_node','OCR_code_detect','Skeletal_detect_cam','Body_detect_cam','Speech_recognition','NLP_language','Language_translator','Stepper_serial_gcode','BLDC_motor','Create_serial_motor,Create_serial_motor_logic','Create_i2c_Servo,Create_serial_Servo,Create_Servo_motor',"Serial_write_multipurpose,Serial_read_multipurpose",'Lidar_publisher','GPS_navigation','Sensor_array_input','Multi_node_logic']
read_current_json = {"publish_data":"pub_node","subscriber_data":"sub_node","Multi_cache_server":"Multi_cache_server","Multiple_node_logic":"Multiple_node_logic","Camera_raw":"Camera_raw","face_recog":"face_rec","Object_recognition_pub":"object_rec","QR_code_scanner_pub":"QR_code_scanner_pub","OCR_code_scanner_pub":"OCR_code","Skeletal_detection":"Skeletal_detection","Body_detection":"Body_detection","tts":"Text_to_speech","Speech_recognition":"Speech_recognition","NLP_languageprocessing":"NLP_language_processing","Translate_language":"Translage_language","Stepper_motor_control":"Stepper_motor","BLDC_motor":"BLDC_motor","DC_motor_control":"DC_motor","Servo_control":"Servo_motor","Serial_com_connect":"Serial_com","Lidar_publisher":"Lidar","GPS":"GPS","Sensor_array":"Sensor_Array","Multiple_node_logic":"Multiple_node_logic"}
pre_lib_config = "import pyfirmata"+"\nimport serial"+"\nfrom itertools import count"+"\nimport configparser"+"\nimport threading"+"\nimport os"+"\nfrom roboreactmaster import " 

matching_lib = {} # Getting the matching
Library_mem = [] # Getting the library mem from the function gen 
Library_mem.append('Create_node_sub,')
mem_thread_function = [] # mem thread 
new_order = {} # language _new order to get the breviation of lanuage name 
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
for r in list(Languages):
        
         new_order[Languages.get(str(r))] = str(r)
print(new_order)  
#Generate config code 
class config_from_keys(object):
       def pub_node(self,path_num,data_requested):
             print(message_path)
             config = configparser.ConfigParser()    
             config.read(message_path+'publisher_node.cfg') 
             list_data = os.listdir(message_path)
             print(list_data)
             pub_buffer= config['pub_node']['pub_node_buffers'] # Getting the path data of the buffers          
             print(pub_buffer) 
             #Write config code 
             print("Start writing path....")
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"buffer",pub_buffer) 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                       
             except: 
                  print("Configfile was created!")                

       def sub_node(self,path_num,data_requested): 
             print(message_path)
             config = configparser.ConfigParser()    
             config.read(message_path+'subscriber_node.cfg') 
             list_data = os.listdir(message_path)
             print(list_data)
             sub_buffer= config['sub_node']['sub_node_buffers'] # Getting the path data of the buffers          
             print(sub_buffer) 
             #write config code 
             print("Start writing path....")
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"buffer",sub_buffer)
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")     
       #Vision part 
       def Camera_raw(self,path_num,data_requested):
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'camera_raw/camera_raw.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             camera_buffer= config['camera_data']['camera_buffer'] # Getting the path data of the buffers          
             print(camera_buffer) 
             #Write path
             print("Start writing path....")     
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"camera_number",data_requested.split(",")[2])
                  config.set(str(path_num),"Camera_buffer",camera_buffer)
                   
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")   
       def Multi_cache_server(self,path_num,data_requested):
             #Read path 
             print(Multi_cache_path)
             config = configparser.ConfigParser()    
             config.read(Multi_cache_path+'multicache_server.cfg') 
             list_data = os.listdir(Multi_cache_path)
             print(list_data)
             display_config= config['multi_cache_server']['Multicache_server_displaywidth'] # Getting the path data of the buffers          
             local_ip = config['multi_cache_server']['local_ip']
             print("Display_config",display_config)
             print("Local_ip",local_ip) 
             #Write path
             print("Start writing path....")     
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"camera_number",data_requested.split(",")[0])
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[1])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[2])
                  config.set(str(path_num),'display_width',display_config)
                  config.set(str(path_num),'local_ip',local_ip) 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  
                  print("Configfile was created!")           
       def face_rec(self,path_num,data_requested): 
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'face_recognition/facerec.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             face_buffer = config['face_rec_dat']['face_rec_buffer'] # Getting the path data of the buffers          
             face_path = config['face_rec_dat']['face_path']  # Getting the face path 
             message_ip = config['face_rec_dat']['message_ip'] # getting the message ip 
             display = config['face_rec_dat']['display']
             print(face_buffer) 
             print(face_path)
             print(message_ip) 
             print(display)

             #Write path   
             print("Start writing path....")
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"camera_number",data_requested.split(",")[1])
                  config.set(str(path_num),"port",data_requested.split(",")[2])  
                  config.set(str(path_num),"port_message",data_requested.split(",")[3])
                  config.set(str(path_num),"Buffer",face_buffer)
                  config.set(str(path_num),"face_path",face_path) 
                  config.set(str(path_num),"message_ip",message_ip)
                  config.set(str(path_num),"display",display)
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!") 
       def object_rec(self,path_num,data_requested):
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'object_recognition/object_recognition.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             object_recog_buffer = config['object_recog']['object_recog_buffer'] # Getting the path data of the buffers          
             model_prototxt_path = config['object_recog']['model_prototxt_path']  # Getting the face path 
             model_caffe_path = config['object_recog']['model_caffe_path'] #Getting the caffe weights 
             object_rec_label = config['object_recog']['object_rec_label'] # Getting the object_recognition label data 
             message_ip = config['object_recog']['message_ip'] # getting the message ip 
             display = config['object_recog']['display']
             print(object_recog_buffer)
             print(model_prototxt_path) 
             print(model_caffe_path)
             print(object_rec_label)
             print(message_ip) 
             print(display)

             #Write path   
             print("Start writing path....")
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"camera_number",data_requested.split(",")[1])
                  config.set(str(path_num),"port",data_requested.split(",")[2])  
                  config.set(str(path_num),"port_message",data_requested.split(",")[3])
                  config.set(str(path_num),"Buffer",object_recog_buffer)
                  config.set(str(path_num),"model_prototxt_path",model_prototxt_path)
                  config.set(str(path_num),"model_caffe_path",model_caffe_path) 
                  config.set(str(path_num),"object_rec_label",object_rec_label)       
                  config.set(str(path_num),"message_ip",message_ip)
                  config.set(str(path_num),"display",display)
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")               
       def QR_code_scanner_pub(self,path_num,data_requested):
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'qr_code/qr_detect.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             qr_buffer = config['qr_detect']['qr_detect_buffer'] # Getting the path data of the buffers          
             print(qr_buffer) 
             #Write path   
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")            
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"camera_number",data_requested.split(",")[1])
                  config.set(str(path_num),"port",data_requested.split(",")[2])
                  config.set(str(path_num),"port_message",data_requested.split(",")[3])
                  config.set(str(path_num),"Qr_buffer",qr_buffer)  
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")   
       def OCR_code(self,path_num,data_requested):
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'ocr/ocr_detect.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             ocr_buffer = config['ocr_detec']['ocr_detec_buffer'] # Getting the path data of the buffers          
             print(ocr_buffer) 
             #Write path
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")            
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"camera_number",data_requested.split(",")[1])
                  config.set(str(path_num),"port",data_requested.split(",")[2]) 
                  config.set(str(path_num),"port_message",data_requested.split(",")[3]) 
                  config.set(str(path_num),"ocr_buffer",ocr_buffer)
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")     
       def Skeletal_detection(self,path_num,data_requested):
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'skeletal_detection/skeletal_detect.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             skeletal_buffer = config['skeletal_detect']['skeletal_detect_buffer'] # Getting the path data of the buffers          
             print(skeletal_buffer) 
             #Write path 
             project_config_path = path_project_config+"/"+str(path_num)  # Config path for create config file in the project 
             print("Created path",project_config_path) #show the writing path 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")

             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"camera_number",data_requested.split(",")[1])
                  config.set(str(path_num),"port",data_requested.split(",")[2]) 
                  config.set(str(path_num),"port_message",data_requested.split(",")[3]) 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")      
       def Body_detection(self,path_num,data_requested):
             #Read path 
             print(vision_path)
             config = configparser.ConfigParser()    
             config.read(vision_path+'body_detection/body_detection.cfg') 
             list_data = os.listdir(vision_path)
             print(list_data)
             body_buffer = config['body_detect']['body_detect_buffer'] # Getting the path data of the buffers          
             print(body_buffer) 
             #Write path    
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
                
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"camera_number",data_requested.split(",")[1])
                  config.set(str(path_num),"port",data_requested.split(",")[2]) 
                  config.set(str(path_num),"port_message",data_requested.split(",")[3]) 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")  
       #Audio part
       def Speech_recognition(self,path_num,data_requested):
             #Read path 
             print(audio_path)
             config = configparser.ConfigParser()    
             config.read(audio_path+'speech_recognition/speech_recognition.cfg') 
             list_data = os.listdir(audio_path)
             print(list_data)
             asr_buffers = config['Speech_recognition']['asr_buffers'] 
             print(asr_buffers) 
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"Destination_language",data_requested.split(",")[2]) # convert into the breviation  
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")    
       def Text_to_speech(self,path_num,data_requested):
             #Read path 
             print(audio_path)
             config = configparser.ConfigParser()    
             config.read(audio_path+'speech_synthesis/speech_synthesis.cfg') 
             list_data = os.listdir(audio_path)
             print(list_data)
             speed = config['Speech_synthesis']['tts_speed'] # Getting the path data of the buffers          
             loudness = config['Speech_synthesis']['tts_loudness']  # Getting loudness of the 
             print(speed,loudness) # Getting speed of voice and loudness  
             #Write path    
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")

             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"Destination_language",data_requested.split(",")[0])
                  config.set(str(path_num),"Loudness",data_requested.split(",")[1])
                  config.set(str(path_num),"Speed",speed) # Getting the speech speed of the tts 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")  
       #NLP part 
       def NLP_language_processing(self,path_num,data_requested):
             #Read path 
             print(nlp_path)
             config = configparser.ConfigParser()    
             config.read(nlp_path+'nlp.cfg') 
             list_data = os.listdir(nlp_path)
             print(list_data)
             language_default = config['nlp']['nlp_lang_default'] # Getting the path data of the buffers          
             print(language_default) 
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"port_message",data_requested.split(",")[2])
                  config.set(str(path_num),"Language",data_requested.split(",")[3])
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")     
       def Translate_language(self,path_num,data_requested):
             print(nlp_path)
             config = configparser.ConfigParser()    
             config.read(nlp_path+'translate.cfg') # Getting the translator config
             list_data = os.listdir(nlp_path)
             print(list_data)
             path_config = config['translate_lang']['translate_lang_default'] # Getting the path data of the buffers          
             print(path_config) 
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"input_language",data_requested.split(",")[2])
                  config.set(str(path_num),"destination_language",data_requested.split(",")[3])
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")     
       #Motion system 
       def BLDC_motor(self,path_num,data_requested):
             print(motion_path)
             config = configparser.ConfigParser()    
             config.read(motion_path+'bldc/bldc_motor.cfg') 
             list_data = os.listdir(motion_path)
             print(list_data)
             bldc_baudrate = config['bldc_motor']['bldc_motor_serial_baudrate'] # Getting the path data of the buffers          
             print(bldc_baudrate) 
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")  
       def Stepper_motor(self,path_num,data_requested):
             print(motion_path)
             config = configparser.ConfigParser()    
             config.read(motion_path+'stepper/Stepper_motor.cfg') 
             list_data = os.listdir(motion_path)
             print(list_data)
             stepper_baudrate = config['stepper']['stepper_motor_serial'] # Getting the path data of the buffers          
             print(stepper_baudrate) 
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"serial_port",data_requested.split(",")[2]) # Getting the serial port data
                  config.set(str(path_num),"Baud_rate",stepper_baudrate) 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")  
       def DC_motor(self,path_num,data_requested):
             print(motion_path)
             config = configparser.ConfigParser()    
             config.read(motion_path+'dc/Dc_motor.cfg') 
             list_data = os.listdir(motion_path)
             print(list_data)
             baud_rate = config['DC_motor']['DC_motor_serial_baudrate'] # Getting the path data of the buffers          
             serial_mcu_chip = config['DC_motor']['serial_mcu_chip'] #serial mcu 
             print(baud_rate)  
             print(serial_mcu_chip)

             #Write path    
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:

                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"serial_port",data_requested.split(",")[2])
                  config.set(str(path_num),"baud_rate",baud_rate)
                  config.set(str(path_num),"serial_mcu_chip",serial_mcu_chip) # Getting the serial mcu chip for the microcontroller config generate
                  config.set(str(path_num),"GPIOR",data_requested.split(",")[3]) # GPIO right 
                  config.set(str(path_num),"GPIOL",data_requested.split(",")[4]) # GPIO left 

                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")  
       def Servo_motor(self,path_num,data_requested):
             print(motion_path)
             config = configparser.ConfigParser()    
             config.read(motion_path+'servo/servo.cfg') 
             list_data = os.listdir(motion_path)
             print(list_data)
             servo_baudrate = config['Servo_motor']['Servo_motor_serial_baudrate'] # Getting the path data of the buffers          
             servo_i2c = config['Servo_motor']['Servo_motor_i2c_com']
             Servo_mcu_device = config['Servo_motor']['Servo_mcu_chip']
             print(servo_baudrate)
             print(servo_i2c)  
             print(Servo_mcu_device)   
             #Write path     
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  config.set(str(path_num),"serial_port",data_requested.split(",")[2]) 
                  config.set(str(path_num),"pins",data_requested.split(",")[3])
                  config.set(str(path_num),"Servo_motor_i2c_com",servo_i2c)
                  config.set(str(path_num),"Servo_mcu_device",Servo_mcu_device) # Servo mcu serial device 
                  config.set(str(path_num),"baud_rate",servo_baudrate)
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")     
       #Serial com 
       def Serial_com(self,path_num,data_requested):
             print(serial_path)
             config = configparser.ConfigParser()    
             config.read(serial_path+'serial_com.cfg') 
             list_data = os.listdir(serial_path)
             print(list_data)
             serial_baudrate = config['serial_com']['serial_com_baud_rate'] # Getting the path data of the buffers          
             serial_decode = config['serial_com']['serial_decode']
             serial_code = config['serial_com']['serial_code']
             serial_mcu_chip = config['serial_com']['serial_mcu_chip']
             print(serial_baudrate) 

             #Write path    
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"Serial_port",str(data_requested.split(",")[0]))
                  config.set(str(path_num),"Baud_rate",serial_baudrate)
                  config.set(str(path_num),'ip_address',"'"+str(data_requested.split(",")[1])+"'")
                  config.set(str(path_num),'port',data_requested.split(",")[2])  
                  config.set(str(path_num),'serial_decode',serial_decode)
                  config.set(str(path_num),'serial_code',serial_code) 
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")   
       #Navigation 
       def Lidar(self,path_num,data_requested):
             print(navigation_path)
             config = configparser.ConfigParser()    
             config.read(navigation_path+'lidar/lidar_detect.cfg') 
             list_data = os.listdir(navigation_path)
             print(list_data)
             lidar_baudrate = config['lidar_detect']['Lidar_sensor_baudrate'] # Getting the path data of the buffers          
             print(lidar_baudrate) #Serial baudrate  
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!") 
       def GPS(self,path_num,data_requested):
             print(navigation_path)
             config = configparser.ConfigParser()    
             config.read(navigation_path+'gps/gps.cfg') 
             list_data = os.listdir(navigation_path)
             print(list_data)
             gps_config = config['gps']['gps_serial_baudrate'] # Getting the path data of the buffers          
             print(gps_config) 
             #Write path 
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"ip_address","'"+str(data_requested.split(",")[0])+"'")
                  config.set(str(path_num),"port",data_requested.split(",")[1])
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")    
       #Sensor array 
       def Sensor_Array(self,path_num,data_requested):
             print(Sensor_array_path)
             config = configparser.ConfigParser()    
             config.read(Sensor_array_path+'sensor_array.cfg') 
             list_data = os.listdir(Sensor_array_path)
             print(list_data)
             sensor_array_config = config['sensor_array']['sensor_array_title'] # Getting the path data of the buffers          
             print(sensor_array_config) 
             #Write path   
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"width",data_requested.split(",")[0])
                  config.set(str(path_num),"height",data_requested.split(",")[1])
                  config.set(str(path_num),"display",data_requested.split(",")[2])

                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!")  
       #Logic part  
       def Multiple_node_logic(self,path_num,data_requested):
             print(Multiple_logic_path)
             config = configparser.ConfigParser()    
             config.read(Multiple_logic_path+'multiple_logic_node.cfg') 
             list_data = os.listdir(Multiple_logic_path)
             print(list_data)
             multiplenode_config = config['multiple_node_logic']['multiple_node_title'] # Getting the path data of the buffers          
             print(multiplenode_config) 
             #Write path    
             project_config_path = path_project_config+"/"+path_num  # Config path for create config file in the project 
             try:
               os.mkdir(path_project_config+"/"+path_num,mode=0o777) # Making the directory 
             except:
                print("Directory was created!")
             try:
                  print("Start writing config file......")
                  print(data_requested)
                  config = configparser.ConfigParser() 
                  config.add_section(str(path_num))
                  config.set(str(path_num), 'path',project_config_path)
                  config.set(str(path_num),"List_node_number",data_requested)
                  configfile = open(project_config_path+"/"+str(path_num)+".cfg",'w')
                  config.write(configfile)
                    
             except: 
                  print("Configfile was created!") 
#Generated code  running this function in the check found class to write the code with the json file 
class code_from_json_gen(object):       

       def pub_node(self,path_num):
             # Reading the file here to get the pub nodes config
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             pub_ip = config[path_num]['ip_address']
             port = config[path_num]['port']             
             print("Code writer read config",path_config)         
             print("pub_ip",pub_ip)
             print("port",port) 
             message_ref = {str(r):"values"} 
             text_edit = "\ndef "+str(path_num)+"_function():\n\tCreate_node_pub("+str(message_ref)+","+str(pub_ip)+","+str(port)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function") # mem threading functoin to generate the function of the threading in the code 

       def sub_node(self,path_num): 
             # Reading the file here to get the pub nodes config
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             pub_ip = config[path_num]['ip_address']
             port = config[path_num]['port']    
             buffer = config[path_num]['buffer']         
             print("Code writer read config",path_config)         
             print("pub_ip",pub_ip)
             print("port",port) 
             print("buffer",buffer)
             message_ref = {str(r):"values"} 
             text_edit = "\ndef "+str(path_num)+"_function():"+"\n\tglobal data_"+str(path_num)+";data_"+str(path_num)+" = Create_node_sub("+str(path_num.split("_")[len(path_num.split("_"))-1])+","+str(pub_ip)+","+str(buffer)+","+str(port)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       #Vision part 
       def Camera_raw(self,path_num):
             #Read path
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             camera_ip = config[path_num]['ip_address']
             port = config[path_num]['port']
             camera_number = config[path_num]['camera_number'] 
             camera_buffer = config[path_num]['Camera_buffer']
             print("Code writer read config",path_config)         
             print("Camera_ip",camera_ip)
             print("Camera_port",port) 
             print("Camera_number",camera_number)
             print("Camera_buffer",camera_buffer)
             text_edit = "\ndef "+str(path_num)+"_function():\n\tCamera_pub_node("+str(camera_number)+","+str(camera_buffer)+","+str(port)+","+str(camera_ip)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       def Multi_cache_server(self,path_num):
             #Read path
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             camera_ip = config[path_num]['ip_address']        
             camera_number = config[path_num]['camera_number']
             port = config[path_num]['port'] 
             display_width = config[path_num]['display_width']
             local_ip = config[path_num]['local_ip']
             print("Code writer read config",path_config)         
             print("Camera_cache_ip",camera_ip)
             print("Camera_port",port) 
             print("Camera_number",camera_number)
             print("Camera_display",display_width)
             print("Camera_local_ip",local_ip)
             text_edit = "\ndef "+str(path_num)+"_function():\n\tCamera_multi_cache("+str(camera_number)+","+str(local_ip)+","+str(port)+","+str(display_width)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
             list_path_dir = os.listdir(path_project_config)
             for rt in list_path_dir:
                     dt = rt.split("_")
                     dt.remove(rt.split("_")[len(rt.split("_"))-1])
                     f_join = "_".join(dt)       
                     if f_join == 'Camera_raw':
                           global camera_raw_ip;camera_raw_ip = config[rt]['ip_address']
                           break

             print("Number of cache_node",path_num.split("_")[len(path_num.split("_"))-1])
             cache_num = path_num.split("_")[len(path_num.split("_"))-1]
             text_edit = "\ndef "+"Cache_Servers_"+str(cache_num)+"_function():\n\tCache_server("+str(local_ip)+","+str(camera_ip)+","+str(port)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
             
       def face_rec(self,path_num): 
             #Read path
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             camera_ip = config[path_num]['ip_address']        
             camera_number = config[path_num]['camera_number']
             port = config[path_num]['port'] 
             port_message = config[path_num]['port_message']
             camera_buffer = config[path_num]['Buffer']
             face_path  = config[path_num]['face_path']
             message_ip = config[path_num]['message_ip']
             display = config[path_num]['display']
             print("Code writer read config",path_config)         
             print("Camera_ip",camera_ip)
             print("Camera_port",port) 
             print("Camera_number",camera_number)
             print("Camera_buffer",camera_buffer)
             print("Camera_port_message",port_message)
             print("Camera_face_path ",face_path)
             print("Camera_message_ip",message_ip)  
             print("Camera_display_ip",display)
             text_edit = "\ndef "+str(path_num)+"_function():\n\tFace_recognition("+str(face_path)+","+str(camera_number)+","+str(camera_ip)+","+str(port)+",'"+str(path_num)+"',"+str(display)+","+str(camera_buffer)+","+str(port_message)+","+str(message_ip)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       def object_rec(self,path_num): 
             #Read path
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             camera_ip = config[path_num]['ip_address']        
             camera_number = config[path_num]['camera_number']
             port = config[path_num]['port'] 
             port_message = config[path_num]['port_message']
             camera_buffer = config[path_num]['buffer']
             model_prototxt_path  = config[path_num]['model_prototxt_path']
             model_caffe_path = config[path_num]['model_caffe_path']
             object_label_path = config[path_num]['object_rec_label']
             message_ip = config[path_num]['message_ip']
             display = config[path_num]['display']
             print("Code writer read config",path_config)         
             print("Camera_ip",camera_ip)
             print("Camera_port",port) 
             print("Camera_number",camera_number)
             print("Camera_buffer",camera_buffer)
             print("Camera_port_message",port_message)
             print("Cam_object_prototxt_path ",model_prototxt_path)
             print("Cam_object_caffe_path",model_caffe_path)
             print("Cam_object_label_path",object_label_path)
             print("Camera_message_ip",message_ip)  
             print("Camera_display_ip",display)
             text_edit = "\ndef "+str(path_num)+"_function():"+"\n\t"+str(path_num+"_label")+" = "+str(object_label_path)+"\n\tCamera_yolo_pub_node("+str(camera_number)+","+str(camera_buffer)+","+str(port)+","+str(port_message)+","+str(camera_ip)+","+str(display)+","+str(path_num+"_label")+","+str(model_prototxt_path)+","+str(model_caffe_path)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
             path_model_dl = "/home/"+str(user)+"/Roboreactor_library/models"
             list_mdl = os.listdir(path_model_dl)
             print(list_mdl)
             for modl in list_mdl:
                    print(modl,path_model_dl+"/"+modl)
                    os.system("sudo cp "+path_model_dl+"/"+modl+" -t "+path_project_config)       
       def QR_code_scanner_pub(self,path_num):
             #Read path
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             camera_ip = config[path_num]['ip_address']        
             camera_number = config[path_num]['camera_number']
             port = config[path_num]['port'] 
             port_message = config[path_num]['port_message']
             camera_buffer = config[path_num]['qr_buffer']
             print("Code writer read config",path_config)         
             print("Camera_ip",camera_ip)
             print("Camera_port",port) 
             print("Camera_number",camera_number)
             print("Camera_buffer",camera_buffer)
             print("Camera_port_message",port_message)
             text_edit = "\ndef "+str(path_num)+"_function():\n\tCamera_QR_sub_node("+str(camera_number)+","+str(camera_buffer)+","+str(port)+","+str(port_message)+","+str(camera_ip)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")

       def OCR_code(self):
            
            pass 
       def Skeletal_detection(self,path_num):
            pass
        
       def Body_detection(self,path_num):
            pass 
        
       #Audio part
       def Speech_recognition(self,path_num):
             #Read path
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             speech_ip = config[path_num]['ip_address']        
             port = config[path_num]['port'] 
             destination_language = config[path_num]['destination_language']
          
             print("Code writer read config",path_config)         
             print("speech_ip",speech_ip)
             print("port",port) 
             print("destination_language",destination_language)
            
             text_edit = "\ndef "+str(path_num)+"_function():\n\tfor "+str(path_num)+" in count(0):"+"\n\t\ttry:"+"\n\t\t\tSpeech_recognition('"+str(new_order.get(destination_language))+"',"+str(speech_ip)+","+str(port)+")"+"\n\t\texcept:"+"\n\t\t\tpass"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       
       def Text_to_speech(self,path_num):
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             print("tts config file",list_file)
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             destination_language = config[path_num]['destination_language']
             speed = config[path_num]['speed']        
             loudness = config[path_num]['loudness'] 
             print("Code writer read config",path_config)         
             print("destination_language",destination_language)
             print("speech_ip",speed)
             print("loudness",loudness) 
             message = "Hello I'm your robot"
             text_edit = "\ndef "+str(path_num)+'_function():\n\tSpeaking_languages("'+str(message)+'","'+str(new_order.get(destination_language))+'",'+str(speed)+","+str(loudness)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
             
       #NLP part 
       def NLP_language_processing(self,path_num):
           pass

       def Translate_language(self,path_num):
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             ip_address = config[path_num]['ip_address']        
             port= config[path_num]['port'] 
             input_language = config[path_num]['input_language']
             destination_language = config[path_num]['destination_language']

             print("Code writer read config",path_config)  
             print("ip_address",ip_address)
             print("port",port) 
             print("input_language",input_language)      
             print("destination_language",destination_language)
             
             message = "Hello I'm your robot"
             text_edit = "\ndef "+str(path_num)+'_function():\n\tLanguage_translator("'+str(message)+'",'+str(ip_address)+","+str(port)+",'"+str(new_order.get(str(destination_language)))+"')"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       #Motion system 
       def BLDC_motor(self,path_num):
           pass

       def Stepper_motor(self,path_num):
             #Control by the g-code 
             print('Stepper motor control')
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             ip_address = config[path_num]['ip_address']        
             port= config[path_num]['port'] 
             serial_port = config[path_num]['serial_port']
             baud_rate = config[path_num]['baud_rate']
             print("Code writer read config",path_config)  
             print("ip_address",ip_address)
             print("port",port) 
             print("serial_port",serial_port)      
             print("baud_rate",baud_rate)
             number_device = path_num.split("_")[len(list(path_num.split("_")))-1]

             text_edit = "\ndef "+str(path_num)+'_function():\n\tStepper_serial_gcode('+str(number_device)+',"'+str("/dev/"+str(serial_port))+'",'+str(baud_rate)+",'"+str("G0 X0 Y0 Z0")+"')"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       def DC_motor(self,path_num):
             #motor driver 
             print('Motor_driver control')
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             ip_address = config[path_num]['ip_address']        
             port= config[path_num]['port'] 
             serial_port = config[path_num]['serial_port']
             baud_rate = config[path_num]['baud_rate']
             serial_mcu_chip = config[path_num]['serial_mcu_chip'] # Getting the serial mcu chip 
             gpior = config[path_num]['GPIOR']
             gpiol = config[path_num]['GPIOL']
             print("Code writer read config",path_config)  
             print("ip_address",ip_address)
             print("port",port) 
             print("serial_port",serial_port)      
             print("baud_rate",baud_rate)
             print("Serial_mcu",serial_mcu_chip)
             print("GPIO",gpior,gpiol)             
             mcu_selected = serial_mcu_chip 
             number_device = path_num.split("_")[len(list(path_num.split("_")))-1]
             #mcu_number, number, speed, gpiol, gpior
             text_edit = "\ndef "+str(path_num)+'_function():\n\tCreate_serial_motor_logic('+str(mcu_selected)+','+str(number_device)+','+str(0)+","+str(0)+","+str(0)+")  #microcontroller ,motor_number_id,speed of motor 0-1,logic motor right 1-0,logic motor left 1-0"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
             
       def Servo_motor(self,path_num):
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             ip_address = config[path_num]['ip_address']        
             port= config[path_num]['port'] 
             serial_port = config[path_num]['serial_port']
             pins = config[path_num]['pins']
             serial_mcu_chip = config[path_num]['servo_mcu_device'] # Getting the serial mcu chip 
             print("Code writer read config",path_config)  
             print("ip_address",ip_address)
             print("port",port) 
             print("serial_port",serial_port)      
             print("pins",pins)
                     
             mcu_selected = serial_mcu_chip 
             number_device = path_num.split("_")[len(list(path_num.split("_")))-1]
             #mcu_number, number, speed, gpiol, gpior
             data = serial_port
             if   data != "I2C":
                  
                  text_edit = "\ndef "+str(path_num)+'_function():\n\tCreate_Servo_motor('+str(mcu_selected)+','+str(number_device)+","+str(0)+")  #microcontroller ,servo number, angle"
                  print(text_edit)
                  project_writer.write(text_edit)
                  mem_thread_function.append(str(path_num)+"_function")  
             if serial_port == "I2C":
                  print("I2c found")

                  text_edit = "\ndef "+str(path_num)+'_function():\n\tCreate_i2c_Servo('+str(number_device)+',"'+str(r)+'",'+str(0)+","+str(pins)+")  #number_servo ,servo_name, angle, pin"
                  print(text_edit)
                  project_writer.write(text_edit)
                  mem_thread_function.append(str(path_num)+"_function") 
       #Serial com 
       def Serial_com(self,path_num):
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             serial_port = config[path_num]['serial_port']        
             baud_rate= config[path_num]['baud_rate'] 
             ip_address = config[path_num]['ip_address']
             port = config[path_num]['port']
             
             print("Number of cache_node",path_num.split("_")[len(path_num.split("_"))-1])
             
             print("Code writer read config",path_config)  
             print("Serial_port",serial_port)
             print("Baud_rate",baud_rate) 
             #print("Serial_decode",type(serial_decode))
             #print("Serial_code",serial_code)
             number_serial = path_num.split("_")[len(path_num.split("_"))-1]
             text_edit = "\ndef "+str(path_num)+'_function():\n\tSerial_read_multipurpose('+str(number_serial)+","+str(path_num)+","+str('True')+",'"+str('utf-8')+"',"+str(ip_address)+","+str(port)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
             text_edit = "\ndef "+str('Serial_read_sub_')+str(number_serial)+'_function():\n\tfor rt_'+str(number_serial)+' in count(0):\n\t\tglobal data_'+str(number_serial)+";data_"+str(number_serial)+' = Create_node_sub('+str(number_serial)+","+str(ip_address)+","+str(port)+")"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str('Serial_read_sub_')+str(number_serial)+'_function')
             
       #Navigation 
       def Lidar(self,path_num):
           pass 

       def GPS(self,path_num):
           pass 
       #Sensor array 
       def Sensor_Array(self,path_num):
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             print("Sensor_array config file",list_file)
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             width = config[path_num]['width']
             height = config[path_num]['height']        
             display = config[path_num]['display'] 
             print("Code writer read config",path_config)         
             print("wight",width)
             print("height",height)
             print("display",display) 
             input_list = ['example list need microcontroller data input']
             display_status = {"Non":0,'Display activate':1}
             text_edit = "\ndef "+str(path_num)+'_function():\n\tSensor_array_input("'+str(path_num)+'",'+str(display_status.get(str(display)))+','+str(input_list)+",["+str(width)+","+str(height)+"])"
             print(text_edit)
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")
       #Logic part  
       def Multiple_node_logic(self,path_num):
             project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
             list_file = os.listdir(path_project_config+"/"+path_num) # Getting the file name inside the directory 
             print("Multinode config file",list_file)
             config.read(path_project_config+"/"+path_num+"/"+list_file[0]) # getting the file inside to checking the directory config file 
             path_config = config[path_num]['path']  # Getting the path num to collect the data path in the list 
             print("Code writer read config",path_config)
             #Getting the node generate   
             list_node = config[path_num]['list_node_number'] # Getting the list node number of the 
             text_edit = "\ndef "+str(path_num)+"_function():\n\tlist_node = "+str(list_node)             
             project_writer.write(text_edit)
             mem_thread_function.append(str(path_num)+"_function")  
             

class Check_found_function(object):
         def Function_checker(self,input_function,path_num,sub_data): 

               #Iteratable function 
               read_output_dat = {"publish_data":"pub_node","subscriber_data":"sub_node","Multi_cache_server":"Multi_cache_server","Camera_raw":"Camera_raw","face_recog":"face_rec","Object_recognition_pub":"Object_rec","QR_code_scanner_pub":"QR_code_scanner_pub","Skeletal_detection":"Skeletal_detection","Body_detection":"Body_detection","tts":"Text_to_speech","Speech_recognition":"Speech_recognition","NLP_languageprocessing":"NLP_language_processing","Translate_language":"Translate_language","BLDC_motor":"Stepper_motor","DC_motor":"DC_motor","Servo_control":"Servo_motor","Serial_com_connect":"Serial_com","Lidar_publisher":"Lidar","GPS":"GPS","Sensor_array":"Sensor_Array","Multiple_node_logic":"Multiple_node_logic"}
               for r in range(0,len(list(read_current_json))):  # Adding the path num to the last parameter input from the loop 
                         #print('\nif input_function == "'+str(list(read_output_dat)[r])+'":'+"\n\t"+str(list(read_output_dat)[r])+" = config_from_keys()"+"\n\t"+str(list(read_output_dat)[r])+"."+str(read_output_dat.get(list(read_output_dat)[r]))+"('"+str(path_num)+"','"+str(sub_data)+"')")
                      try:    
                         exec('\nif input_function == "'+str(list(read_current_json)[r])+'":'+"\n\t"+str(list(read_current_json)[r])+" = config_from_keys()"+"\n\t"+str(list(read_current_json)[r])+"."+str(read_current_json.get(list(read_current_json)[r]))+"('"+str(path_num)+"','"+str(sub_data)+"')")  
                         print('\nif input_function == "'+str(list(read_current_json)[r])+'":'+"\n\t"+str(list(read_current_json)[r])+" = config_from_keys()"+"\n\t"+str(list(read_current_json)[r])+"."+str(read_current_json.get(list(read_current_json)[r]))+"('"+str(path_num)+"','"+str(sub_data)+"')")
                      except:
                          print("Error function not found")
                          if input_function == "Multiple_node_logic":
                                     Multiple_node_logic = config_from_keys()
                                     Multiple_node_logic.Multiple_node_logic(path_num,json.dumps(sub_data))
class Lib_generator_function(object):

     def intersection(self,lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3 

     def Generate_library(self):
           try:
             os.remove(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py")
           except:
               print("Project file has been removed")
           print("Generating library......")    
           #Pre-config_library
           for r in range(0,len(list(read_current_json))):
                 #print(r) # Getting the code gen keys to generate new line of the json lib matching file 
                 matching_lib[list(read_current_json)[r]] = pre_lib[r]
           #Get list of exist input command in json 
           for r in range(0,len(list(data_requested))):
          
                dt = list(data_requested)[r].split("_")
                dt.remove(list(data_requested)[r].split("_")[len(list(data_requested)[r].split("_"))-1])
                f_join = "_".join(dt)
                matching_config = matching_lib.get(f_join)
                
                print(matching_config,f_join)
                Library_mem.append(str(matching_config)+",")
                if r == len(list(data_requested))-1:          
                       Library_mem.append(matching_config)
                lib_combined = pre_lib_config+' '.join(Library_mem)
                print(lib_combined)          
           project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
           #add the loop of the intersect lib  in the function and get all contain lib into one single string of library 
           
           text_edit = "import pyfirmata"+"\nimport serial"+"\nimport configparser"+"\nimport threading"+"\nimport os"+"\nfrom roboreactmaster import Create_node_pub"
           project_writer.write(lib_combined) # Getting the lib geneerated from the command input    
     def Thread_gen_function(self):
            project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') # Createing the file with the preconfig library and control function  
            for r in range(0,len(mem_thread_function)):
                        project_writer.write("\nt"+str(r)+" = threading.Thread(target="+mem_thread_function[r]+")")
            for r in range(0,len(mem_thread_function)):
                    
                        project_writer.write("\nt"+str(r)+".start()")   
class Writing_code_function(object):
          def Write_code_function(self,input_function,path_num):
                    #print("Generating code base on config file...",input_function,path_num) # Generate code from the directory input 
                    # Gerating the code from the matching loop in the function
                    #read_output_dat = {"publish_data":"pub_node","subscriber_data":"sub_node","Multi_cache_server":"Multi_cache_server","Camera_raw":"Camera_raw","face_recog":"face_rec","QR_code_scanner_pub":"QR_code_scanner_pub","Skeletal_detection":"Skeletal_detection","Body_detection":"Body_detection","tts":"Text_to_speech","Speech_recognition":"Speech_recognition","NLP_languageprocessing":"NLP_language_processing","Translate_language":"Translate_language","BLDC_motor":"Stepper_motor","DC_motor":"DC_motor","Servo_control":"Servo_motor","Serial_com_connect":"Serial_com","Lidar_publisher":"Lidar","GPS":"GPS","Sensor_array":"Sensor_Array","Multiple_node_logic":"Multiple_node_logic"}
                    
                    print('\nif "'+str(path_num)+'" in '+str(list(read_current_json))+":"+"\n\t\t"+str(input_function)+" = code_from_json_gen()"+"\n\t\t"+str(input_function)+"."+str(read_current_json.get(path_num))+"('"+str(input_function)+"')")
                    exec('\nif "'+str(path_num)+'" in '+str(list(read_current_json))+":"+"\n\t\t"+str(input_function)+" = code_from_json_gen()"+"\n\t\t"+str(input_function)+"."+str(read_current_json.get(path_num))+"('"+str(input_function)+"')")
                      
def Writing_serial_port_config():
        project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') 
        list_file = os.listdir(path_project_config+"/")
        print(list_file)
        for r in list(list_file):
            dt = r.split("_")
            dt.remove(r.split("_")[len(r.split("_"))-1])
            f_join = "_".join(dt)
            serial_detect = ['Serial_com_connect','DC_motor_control','Servo_control'] 
            if f_join == serial_detect[0]: # Serial_com_connect 
                       get_config_serial = os.listdir(path_project_config+"/"+str(r)+"/") 
                       print("Serial_com_connect",get_config_serial[0])
                       # Getting the path of the serial config 
                       config.read(path_project_config+"/"+str(r)+"/"+get_config_serial[0]) # getting the file inside to checking the directory config file 
                      
                       path_config = config[r]['path']  # Getting the path num to collect the data path in the list 
                       serial_port = config[r]['serial_port']
                       baud_rate = config[r]['baud_rate']
                       serial_code = "\n"+str(r)+" = serial.Serial('/dev/"+serial_port+"')"
                       print(serial_code)
                       project_writer.write(serial_code) 
            if f_join == serial_detect[1]:
                       get_config_serial = os.listdir(path_project_config+"/"+str(r)+"/") 
                       print("DC motor control",get_config_serial[0])
                       config.read(path_project_config+"/"+str(r)+"/"+get_config_serial[0]) # getting the file inside to checking the directory config file 
                       path_config = config[r]['path']  # Getting the path num to collect the data path in the list 
                       serial_port = config[r]['serial_port']
                       baud_rate = config[r]['baud_rate']
                       serial_code = "\n"+str(r)+" = pyfirmata.ArduinoMega('/dev/"+serial_port+"')"
                       print(serial_code)
                       project_writer.write(serial_code) 
            if f_join == serial_detect[2]:
                       get_config_serial = os.listdir(path_project_config+"/"+str(r)+"/") 
                       print("Servo motor control",get_config_serial[0])
                       config.read(path_project_config+"/"+str(r)+"/"+get_config_serial[0]) # getting the file inside to checking the directory config file 
                       path_config = config[r]['path']  # Getting the path num to collect the data path in the list 
                       serial_port = config[r]['serial_port']
                       baud_rate = config[r]['baud_rate']
                       if str(serial_port) !="I2C": 
                            serial_code = "\n"+str(r)+" = pyfirmata.ArduinoMega('/dev/"+serial_port+"')"
                            print(serial_code)
                            project_writer.write(serial_code)
                       if str(serial_port) =='I2C':
                            print("No code append in the list") 
                            #Add the I2C code control for the PCM board 16 Channel PWM driver 
                            #serial_code = "\n"+str(r)+" = pyfirmata.ArduinoMega('/dev/"+serial_port+"')"
                            #print(serial_code)
                            #project_writer.write(serial_code)     
def Pins_mcu_config(): 
        project_writer = open(path_project_config+"/"+path_project_config.split("/")[len(path_project_config.split("/"))-1]+".py",'a') 
        list_file = os.listdir(path_project_config+"/")
        print(list_file)
        for r in list(list_file):
            dt = r.split("_")
            dt.remove(r.split("_")[len(r.split("_"))-1])
            f_join = "_".join(dt)
            serial_detect = ['Serial_com_connect','DC_motor_control','Servo_control'] 
            if f_join == serial_detect[1]: # Serial_com_connect 
                       get_config_serial = os.listdir(path_project_config+"/"+str(r)+"/") 
                       print("DC motor control",get_config_serial[0])
                       config.read(path_project_config+"/"+str(r)+"/"+get_config_serial[0]) # getting the file inside to checking the directory config file 
                       path_config = config[r]['path']  # Getting the path num to collect the data path in the list 
                       serial_port = config[r]['serial_port']
                       baud_rate = config[r]['baud_rate']
                       mcu_selected = config[r]['serial_mcu_chip']
                       gpior = config[r]['GPIOR']
                       gpiol = config[r]['GPIOL']
                       number_device = r.split("_")[len(r.split("_"))-1]
                       serial_code = '\nCreate_serial_motor('+str(mcu_selected)+','+str(number_device)+','+str([int(gpior),int(gpiol)])+','+str(r)+")"
                       print(serial_code)
                       project_writer.write(serial_code) 
            if f_join == serial_detect[2]: # Serial_com_connect 
                       get_config_serial = os.listdir(path_project_config+"/"+str(r)+"/") 
                       print("Servo motor control",get_config_serial[0])
                       config.read(path_project_config+"/"+str(r)+"/"+get_config_serial[0]) # getting the file inside to checking the directory config file 
                       path_config = config[r]['path']  # Getting the path num to collect the data path in the list 
                       serial_port = config[r]['serial_port']
                       baud_rate = config[r]['baud_rate']
                       gpio_pin = config[r]['pins']
                       mcu_selected = config[r]['servo_mcu_device']
                       print("Check serial",'"'+str(serial_port)+'"')
                       number_device = r.split("_")[len(r.split("_"))-1]
                       check_serial = serial_port
                       if serial_port != "I2C": 
                           serial_code = '\nCreate_serial_Servo('+str(number_device)+','+str(r)+','+str(mcu_selected)+','+str(gpio_pin)+")"
                           print(serial_code)
                           project_writer.write(serial_code)            
                       
lib_gen = Lib_generator_function() 
lib_gen.Generate_library()



for r in list(data_requested):
       
       print(r,r.split("_")[len(r.split("_"))-1],data_requested.get(r))# getting the data to classify value after loop process 
       dt = r.split("_")
       dt.remove(r.split("_")[len(r.split("_"))-1])
       f_join = "_".join(dt)
       print(f_join)
       sub_data = data_requested.get(r)
       check_scan = Check_found_function()
       check_scan.Function_checker(f_join,r,sub_data)
      # Found multi_cache server then mem the optical version to generate the function   
       # Running the code generater input the parameter from the config file input 
       if f_join == "Multi_cache_server": 
                mem_multi_cache.append(r) # Getting the multi cache found in the list 
                
print("Found mem_multi_cache",mem_multi_cache)    

#Generate the serial port and constant data setting function 
Writing_serial_port_config()   
#Generate pin config 
Pins_mcu_config()
for r in list(data_requested):
           dt = r.split("_")
           dt.remove(r.split("_")[len(r.split("_"))-1])
           f_join = "_".join(dt)
           # Gerating the code from the matching loop in the function 
           code_writer = Writing_code_function()
           code_writer.Write_code_function(r,f_join)
#print(pre_lib_config)          
print(' '.join(Library_mem))           
lib_combined = pre_lib_config+' '.join(Library_mem)
print(lib_combined) 
#Thread gen of library 
thread_gen = Lib_generator_function()
thread_gen.Thread_gen_function()
