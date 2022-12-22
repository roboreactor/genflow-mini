import os 
import json 
import jwt
import requests 

class Authentication_function(object): 
        def request_authentication_API(self,Email,token,secret,Project):
                try:
                     Authentication_data = {'Email':Email,'project_name':Project}
                     res = requests.post('https://roboreactor.com/API/endpoint_request', json=Authentication_data)
                     q_res = res.json().get(Authentication_data.get('Email'))
                     token_data = str(q_res[0])+'.'+str(token)
                     decode_Data = jwt.decode(q_res[0]+'.'+str(token),str(q_res[1]) ,algorithms=["HS512"])
                     return decode_Data 
                except:
                     print("Test_mode_initilizing.....")
                     Authentication_datas = {'Email':Email,'project_name':Project}
                     res_sandbox = requests.post('https://roboreactor.com/API/sandbox_request', json=Authentication_datas)
                     q_res_sb = res_sandbox.json().get(Authentication_data.get('Email'))
                     token_data = str(q_res_sb[0].split(".")[0])+"."+str(q_res_sb[0].split(".")[1])+'.'+str(token)
                     decode_Data = jwt.decode(token_data,str(secret) ,algorithms=["HS512"])
                     #print(decode_Data) 
                     return decode_Data

class Authentication_function_sandbox(object):
        def request_authentication_Sandbox_API(self,Email,token,secret,Project): 
                     Authentication_datas = {'Email':Email,'project_name':Project}
                     res_sandbox = requests.post('https://roboreactor.com/API/sandbox_request', json=Authentication_datas)
                     q_res_sb = res_sandbox.json().get(Authentication_data.get('Email'))
                     token_data = str(q_res_sb[0].split(".")[0])+"."+str(q_res_sb[0].split(".")[1])+'.'+str(token)
                     decode_Data = jwt.decode(token_data,str(secret) ,algorithms=["HS512"])
                     return decode_Data

def Authentication_system(Email,token,secret,Project):
      try:    
         authen = Authentication_function() 
         data_out = authen.request_authentication_API(Email,token,secret,Project)
         return data_out 
      except:
          print("Error authenticating services")



