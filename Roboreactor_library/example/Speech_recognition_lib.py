import threading
from roboreactmaster import Speech_recognition,Create_node_sub
from itertools import count

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
t1 = threading.Thread(target=speech_recog)
t2 = threading.Thread(target=Speech_node)
t1.start() 
t2.start() 


