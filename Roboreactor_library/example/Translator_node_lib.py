import threading 
from itertools import count
from roboreactmaster import Language_translator,Create_node_sub 


def Translang_pub():
       print("Text: hello translate to thai")
       Language_translator('Hello','127.0.0.1',5060,'th')

def Translang_sub():
       for r in count(0):
               global data_out;data_out = Create_node_sub(1,"127.0.0.1",4096,5060)
               print(data_out)

t1 = threading.Thread(target=Translang_pub) 
t2 = threading.Thread(target=Translang_sub)
t1.start()
t2.start()
