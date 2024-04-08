from typing import List, Dict, Optional
from types import FunctionType
from utils.logger import logger
import httpx
import json 
from utils.welcome import welcome


class NsSocket(object):
    def __init__(self, grpc_endpoint:str="api.cloud.nstream.ai:50031", api_server_url:str="http://localhost:8000") -> None:
        self.grpc_endpoint = grpc_endpoint
        self.http_client = httpx.Client()
        self.api_server = api_server_url
        self.status = False
        pass

    def call_grpc_endpoint(self, method: FunctionType):
        self.status = True
        
        return self.status
    
    def call_rest_endpoint(self, payload: Optional[Dict], headers:Optional[Dict]=None, params: Optional[Dict]=None, method: str="GET", route: str="/"):
        endpoint = "{0}/{1}".format(self.api_server, route)
        if method=="GET":
            response = self.http_client.get(headers=headers, url=endpoint, params=params)
        elif method=="POST":
            response = self.http_client.post(headers=headers, url=endpoint, json=payload)
        elif method=="PUT":
            response = self.http_client.put(headers=headers, url=endpoint, data=payload)
        elif method=="DELETE":
            response = self.http_client.delete(headers=headers, url=endpoint)
        else:
            response = httpx.Response(status_code=500, content=None, text=json.dumps({"status":"failed", "reason":"No method allowed"}))
        return response
    
    def terminate_client(self):
        self.http_client.close()

class NsInit(object):
    def __init__(self, api_key="", username="", password="") -> None:
        welcome()
        self.api_key = api_key
        self.username = username
        self.password =password
        self.headers = {}
        self.socket = NsSocket()
        self.params = {}
        pass
    
    def connect(self)->NsSocket:
        try:
            result = self.socket.call_rest_endpoint(method="POST",
                                                    route="sign-in", 
                                                    payload={"email":self.username, "password": self.password}
                                                    )
            oauth_token = result.json().get("access_token")
            self.headers["Authorization"] = "Bearer {0}".format(oauth_token)
            logger.debug(msg="Authorization Token Recieved")
            result = self.socket.call_rest_endpoint(headers=self.headers, payload = {},route="get-api-key/{}".format(self.api_key))
            result = result.json()
            api_secret = result.get("api_secret")
            if api_secret:
                logger.debug(msg="API Key approved")
                return self.socket
            else:
                logger.error(msg="API Key {0} Invalid, please check if API Key exists".format(self.api_key))
                raise Exception("API Does not exist")
        except Exception as e: 
            logger.exception(msg=e)
            raise Exception("Unknown Exception Occured - {0} ".format(e))
        
        
            