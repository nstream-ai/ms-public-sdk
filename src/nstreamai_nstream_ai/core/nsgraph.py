from typing import List, Dict, Optional
from types import FunctionType
from core.nsinit import NsSocket
from core.nsnode import NsNode
import httpx
import json 

class NsGraph(object):
    def __init__(self, socket:NsSocket) -> None:
        self.graph = list(dict())
        self.socket = socket
        self.current_node = None
        self.last_node = None
        pass

    def start(self, node:NsNode):
        self.current_node = node
        return self
    
    def next_node(self,node:NsNode):
        self.last_node = self.current_node
        self.current_node = node
        self.graph.append(self.node_to_dict(self.current_node))
        return self
    
    def end(self, node:NsNode):
        self.last_node = self.current_node
        self.current_node = node
        self.graph.append(self.node_to_dict(self.current_node))
        return self
    
    
    def submit(self, sink:NsLink):
        self.graph.append({"sink": sink})
        self.socket.call_grpc_endpoint(method=(lambda x: x))
        return self

    def terminate(self):
        self.socket.call_grpc_endpoint(method=(lambda x : x))
        return self

    
    @staticmethod
    def node_to_dict(node:NsNode)->Dict:
        return dict()