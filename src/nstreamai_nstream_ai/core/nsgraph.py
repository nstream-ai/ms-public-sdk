from typing import List, Dict, Optional
from types import FunctionType
from core.nsinit import NsSocket
from core.nsnode import NsNode, NsLink
from utils.variables import generate_synthetic_data, send_graphql_request, url, headers
import time
import random
from utils.template import (
    create_token_detail_mutation,
    create_io_throughput_mutation,
    create_inference_latency_mutation
    )

class NsGraph(object):
    def __init__(self, socket:NsSocket) -> None:
        self.graph = list(dict())
        self.socket = socket
        self.current_node = None
        self.last_node = None
        self.list_node_id = []
        pass

    def start(self, node:NsNode):
        self.current_node = node
        node.process()
        self.list_node_id.append(node.node_id)
        return self
    
    def next_node(self,node:NsNode):
        self.last_node = self.current_node
        self.current_node = node
        self.graph.append(self.node_to_dict(self.current_node))
        node.process()
        self.list_node_id.append(node.node_id)
        return self
    
    def end(self, node:NsNode):
        self.last_node = self.current_node
        self.current_node = node
        self.graph.append(self.node_to_dict(self.current_node))
        node.process()
        self.list_node_id.append(node.node_id)
        return self
    
    
    def submit(self, sink:NsLink):
        self.graph.append({"sink": sink})
        self.socket.call_grpc_endpoint(method=(lambda x: x))
        sink.process_sink(self.list_node_id[-1])
        return self

    def terminate(self, run_time):
        if run_time:
            self.run_data_out(run_time=run_time)
        self.socket.call_grpc_endpoint(method=(lambda x : x))
        return self

    
    @staticmethod
    def node_to_dict(node:NsNode)->Dict:
        return dict()
    
    def run_data_out(self, run_time)->None:
        st = time.time()
        while (time.time() - st)<run_time:
            time.sleep(0.1)
            # Generate synthetic data
            data = generate_synthetic_data()
            data["node_id"] = random.choice(self.list_node_id)
            
            mutation = create_token_detail_mutation(data["tokens"], data["node_id"])
            _ = send_graphql_request(url, headers, mutation)

            mutation = create_io_throughput_mutation(data["node_id"], data["input_throughput"], data["output_throughput"])
            _ = send_graphql_request(url, headers, mutation)

            mutation = create_inference_latency_mutation(
                data["node_id"],
                data["llm_inference_speed"],
                data["context_retrieval_speed"],
                data["total_node_inference_speed"]
            )
            _ = send_graphql_request(url, headers, mutation)

