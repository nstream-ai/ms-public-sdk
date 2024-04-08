from typing import List, Dict, Optional #LiteralString
from core.nsneuron import NsNeuron

class NsProviderType():
    Sink: str
    Source = str
    def __init__(self) -> None:
        self.Sink = "SINK"
        self.Source = "SOURCE"

class NsDataObject():
    NsProviderName: str
    NsProviderMeta: Dict
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

class NsNodeOutput(Nstream):
    def __init__(self) -> None:
        self.provider = NsProvider("SINK").nsnode()
        return super().__init__(provider=self.provider)
        
class NsNode(object):
    def __init__(self, prompt:NsLink|NsNodeOutput, context: NsLink|NsNodeOutput, neuron: NsNeuron) -> None:
        self.prompt = prompt
        self.context = context
        self.neuron = neuron
        pass

    def output(self):
        out = NsNodeOutput()
        print(out.__dict__,"++++++))))))))))))))))))))))))))))")
        return out