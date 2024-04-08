from typing import List, Dict, Optional #LiteralString
from core.nsneuron import NsNeuron
from utils.template import (
    create_node_detail_mutation,
    create_data_detail_mutation
)
import random
import json
from utils.variables import send_graphql_request, url, headers

class NsProviderType():
    Sink: str
    Source = str
    def __init__(self) -> None:
        self.Sink = "SINK"
        self.Source = "SOURCE"

class NsDataObject():
    NsProviderName: str
    NsProviderMeta: Dict
    NsProviderType: str
    def __init__(self, ns_provider_name, ns_provider_meta, ns_provider_type) -> None:
        self.NsProviderName = ns_provider_name
        self.NsProviderMeta = ns_provider_meta
        self.NsProviderType = ns_provider_type
        pass
    def get(self):
        return self

class NsProvider(object):
    def __init__(self, type:str) -> None:
        self.type = type
        
    def mongodb(self, **kwargs):
        return NsDataObject(ns_provider_meta=kwargs, ns_provider_name="MONGODB", ns_provider_type=self.type)
    def postgresql(self, **kwargs):
        return NsDataObject(ns_provider_meta=kwargs, ns_provider_name="POSTGRESQL", ns_provider_type=self.type)
    def terminal(self, **kwargs):
        return NsDataObject(ns_provider_meta=kwargs, ns_provider_name="TERMINAL", ns_provider_type=self.type)
    def nsnode(self, **kwargs):
        return NsDataObject(ns_provider_meta=kwargs, ns_provider_name="NODE", ns_provider_type=self.type)

class Nstream(object):
    def __init__(self, provider:NsProvider) -> None:
        self.provider = provider
        self.event = "EVENT"
        pass

class NsLink(Nstream):
    def __init__(self, 
                 provider: NsProvider, 
                 prompt_text:Optional[str]=None, 
                 context_tranform_prompt_text: Optional[str]=None
                 ) -> None:
        self.provider = provider
        self.prompt_text = prompt_text
        self.context_prompt_text = context_tranform_prompt_text
        return super().__init__(provider=self.provider)
    def define_prompt(self):
        return "{}: \n {}".format(self.prompt_text, self.event)
    def define_context(self):
        return "{}: \n {}".format(self.context_prompt_text, self.event)
    def process_sink(self, node_id)->None:
        #  datasink - prompt
        avg_throughput = random.uniform(300, 500)
        provider_name = self.provider.NsProviderName
        link_metadata = {provider_name: "value"}
        data_input = self.provider.NsProviderType
        role = "output"
        prompt_mutation = create_data_detail_mutation(data_input, node_id, avg_throughput, link_metadata, role)
        _ = send_graphql_request(url, headers, prompt_mutation)
        
class NsNode(object):
    def __init__(self, node_name:str, prompt:NsLink, context: NsLink, neuron: NsNeuron) -> None:
        self.node_name = node_name
        self.prompt = prompt
        self.context = context
        self.neuron = neuron
        pass

    def output(self, context_tranform_prompt_text:Optional[str]):
        out = NsLink(
            provider=NsProvider("SOURCE").nsnode(), 
            context_tranform_prompt_text=context_tranform_prompt_text
            )
        return out
    
    def process(self)->None:
        prompt_size = random.uniform(20, 80)
        context_size = random.uniform(70, 120)
        total_data_processed = random.randint(5, 20)
        node_mutation = create_node_detail_mutation(
            self.node_name,
            context_size,
            prompt_size,
            total_data_processed,
            self.neuron.llm
            )
        response = send_graphql_request(url, headers, node_mutation)
        self.node_id = json.loads(response.text).get("data").get("createNodeDetail").get("id")
        

        #  datasource - prompt
        avg_throughput = random.uniform(300, 500)
        provider_name = self.prompt.provider.NsProviderName
        link_metadata = {provider_name: "value"}
        data_input = self.prompt.provider.NsProviderType
        role = "prompt"
        prompt_mutation = create_data_detail_mutation(data_input, self.node_id, avg_throughput, link_metadata, role)
        response = send_graphql_request(url, headers, prompt_mutation)

        #  datasource - context
        avg_throughput = random.uniform(300, 500)
        provider_name = self.context.provider.NsProviderName
        link_metadata = {provider_name: "value"}
        data_input = self.context.provider.NsProviderType
        role = "context"
        context_mutation = create_data_detail_mutation(data_input, self.node_id, avg_throughput, link_metadata, role)
        response = send_graphql_request(url, headers, context_mutation)

        return None

