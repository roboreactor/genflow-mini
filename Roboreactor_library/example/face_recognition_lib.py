import requests
from roboreactmaster import Face_recognition ,Camera_pub_node,Speech_recognition,Create_node_sub,Speaking_languages
import threading
from itertools import count 
def Camera_raw():
        Camera_pub_node(0,65536,5609,'127.0.0.1')

def Fr_recognition():
        Face_recognition("Face_db",0,'127.0.0.1',5070,"Face_recognition_1",0,65536,5609,'127.0.0.1')
        
def speech_recog():
     for rt in count(0):
        try:
          Speech_recognition('th','en','127.0.0.1',5630)
        except:
            pass 

def Speech_node():
     
        for rt in count(0):
            global data_out;data_out = Create_node_sub(1,"127.0.0.1",4096,5630)
            print("speech_to_text ",data_out)
            speech_key = list(data_out)[0]
            if speech_key != " ":
                 Speaking_languages(speech_key,'th','1.04',100) 
def face_rec_sub_node(): 
            for rt in count(0):
                   global data_out_1;data_out_1 = Create_node_sub(1,"127.0.0.1",4096,5070)
                   print(data_out_1)
                   #try:
                      #res = requests.post("http://127.0.0.1:4060/Multiple_node_2",json=data_out_1)
                      #print(res.json())
                   #except:
                   #   print("Server multinode not found")  
t1 = threading.Thread(target=speech_recog)
#t2 = threading.Thread(target=Speech_node)
t3 = threading.Thread(target=Camera_raw)
t4 = threading.Thread(target=Fr_recognition)
t5 = threading.Thread(target=face_rec_sub_node)
t1.start() 
#t2.start() 
t3.start() 
t4.start()           
t5.start()
