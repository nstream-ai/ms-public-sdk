import json
import httpx
from types import FunctionType
from utils.logger import logger
from utils.welcome import welcome
from typing import Dict, Optional


class NsSocket(object):

    def __init__(
            self,
            grpc_endpoint: str = "api.cloud.nstream.ai:50031",
            api_server_url: str = "http://localhost:8000",
            headers: dict = {},
            dashboard_server: str = "http://localhost:8000/graphql") -> None:
        self.grpc_endpoint = grpc_endpoint
        self.http_client = httpx.Client()
        self.api_server = api_server_url
        self.dashboard_server = dashboard_server
        self.status = False
        self.headers = headers

    def call_grpc_endpoint(self, method: FunctionType):
        self.status = True

        return self.status

    def call_rest_endpoint(self,
                           payload: Optional[Dict] = {},
                           params: Optional[Dict] = None,
                           method: str = "GET",
                           route: str = "/"):
        endpoint = "{0}/{1}".format(self.api_server, route)
        if method == "GET":
            response = self.http_client.get(headers=self.headers,
                                            url=endpoint,
                                            params=params)
        elif method == "POST":
            response = self.http_client.post(headers=self.headers,
                                             url=endpoint,
                                             json=payload)
        elif method == "PUT":
            response = self.http_client.put(headers=self.headers,
                                            url=endpoint,
                                            data=payload)
        elif method == "DELETE":
            response = self.http_client.delete(headers=self.headers,
                                               url=endpoint)
        else:
            response = httpx.Response(status_code=500,
                                      content=None,
                                      text=json.dumps({
                                          "status":
                                          "failed",
                                          "reason":
                                          "No method allowed"
                                      }))
        return response

    def terminate_client(self):
        self.http_client.close()


class NsInit(object):

    def __init__(self, api_key="", username="", password="") -> None:
        welcome()
        self.api_key = api_key
        self.username = username
        self.password = password
        self.socket = NsSocket()
        self.headers = {}
        self.params = {}

    def connect(self) -> NsSocket:
        try:
            result = self.socket.call_rest_endpoint(method="POST",
                                                    route="sign-in",
                                                    payload={
                                                        "email": self.username,
                                                        "password":
                                                        self.password
                                                    })
            oauth_token = result.json().get("access_token")
            self.headers = {
                "Authorization": "Bearer {0}".format(oauth_token),
                'Content-Type': 'application/json'
            }
            self.socket = NsSocket(headers=self.headers)
            logger.info(msg="Authorization Token Received")
            result = self.socket.call_rest_endpoint(
                route="get-api-key/{}".format(self.api_key))
            result = result.json()
            api_secret = result.get("api_secret")
            if api_secret:
                logger.debug(msg="API Key approved")
                return self.socket
            else:
                logger.exception(
                    msg="API Key {0} Invalid, please check if API Key exists".
                    format(self.api_key))
                raise Exception("API Does not exist")
        except Exception as e:
            logger.exception(msg=e)
            raise Exception("Unknown Exception Occurred - {0} ".format(e))
