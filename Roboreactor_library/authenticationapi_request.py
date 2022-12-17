import os 
import json 
import jwt
import requests 

class Authentication_function(object): 
        def request_authentication_API(self,Email,token,secret,Project):
                Authentication_data = {'Email':Email,'project_name':Project}
                res = requests.post('https://roboreactor.com/API/endpoint_request', json=Authentication_data)
                #print(res.json()) 
                #return logic to the authentication to check the status of the hardware connection 
                q_res = res.json().get(Authentication_data.get('Email'))
                #print(q_res[0],q_res[1])
                #print(type(q_res[1]))
               
                token_data = str(q_res[0])+'.'+str(token)
                decode_Data = jwt.decode(q_res[0]+'.'+str(token),str(q_res[1]) ,algorithm=["HS512"])
                #print(decode_Data)
                return decode_Data 
                               
 
def Authentication_system(Email,token,secret,Project): 
      authen = Authentication_function() 
      data_out = authen.request_authentication_API(Email,token,secret,Project)
      return data_out


