import pyfirmata 
import threading
from itertools import count
from roboreactmaster import Create_node_sub,Sensor_anaiter,Sensor_anasetpins,Sensor_anafirmserial
sensor_1 = pyfirmata.ArduinoMega("/dev/ttyUSB0")
Sensor_anaiter("force_sensor",1,sensor_1)
Sensor_anasetpins("force_sensor",1,sensor_1,[0,7])
def Analog_tx_node():
    for rt in count(0):
       Sensor_anafirmserial("force_sensor",1,sensor_1,0,'127.0.0.1',5604)
       Sensor_anafirmserial("Proxemity_sensor",1,sensor_1,1,'127.0.0.1',5605)
       
def Sub_node():
        for rt in count(0):
            global data_out;data_out = Create_node_sub(1,"127.0.0.1",4096,5604)
            global data_out_1;data_out_1 = Create_node_sub(1,"127.0.0.1",4096,5605)
            list_sensor = list((data_out.get('force_sensor'),data_out_1.get('Proxemity_sensor')))
            print(list_sensor)
t1 = threading.Thread(target=Analog_tx_node)
t2 = threading.Thread(target=Sub_node)
t1.start() 
t2.start() 
