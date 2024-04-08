from core.nsinit import NsInit
from core.nsnode import NsNode, NsLink, NsProvider
from core.nsneuron import NsNeuron, NstreamLLM
from core.nsgraph import NsGraph
import sys

if __name__ == "__main__":
    try:
        conn = NsInit(api_key="PICKTSB4IFW", username="piyush@nstream.ai", password="nstream.cloud").connect()
    except Exception as e:
        print(e)
        sys.exit()
    ns_node_1 = NsNode(
        prompt=NsLink(
            provider=NsProvider(type="SINK").mongodb(), 
            prompt_text="Hi my name is deepak"),
        context=NsLink(
            provider=NsProvider(type="SINK").postgresql(), 
            context_tranform_prompt_text="Deepak is lover boy"), 
        neuron=NsNeuron(NstreamLLM.mistral_7b())
        )

    ns_node_2 = NsNode(
        prompt=NsLink(
            provider=NsProvider(type="SINK").mongodb(), 
            prompt_text="Hi my name is deepak", 
            ),
        context=ns_node_1.output(prompt_text=None, context_tranform_prompt_text="What is my name"),
        neuron=NsNeuron(NstreamLLM.llama2_7b())
    )

    ns_graph_sink = NsLink(
        provider=NsProvider(type="SINK").terminal(), 
    )

    ns_graph = NsGraph(conn).start(ns_node_1).end(ns_node_2).submit(ns_graph_sink)
    
    # ns_node_3 = NsNode(
    #     prompt=NsLink(provider=NsProvider(type="SINK").nsnode(ns_node_2.output()), prompt_text="Hi my name is deepak", context_tranform_prompt_text="Deepak is lover boy"),
    #     context=NsLink(provider=NsProvider(type="SINK").postgresql(), prompt_text="Hi my name is deepak", context_tranform_prompt_text="Deepak is lover boy"), 
    #     neuron=NsNeuron(NstreamLLM.llama2_7b()))
    



    # ns_node_2 = NsNode(prompt=NsLink(), context=ns_node_1.output(), neuron=NsNeuron(NstreamLLM.mistral_7b()))
    # ns_node_3 = NsNode(prompt=ns_node_2.output(), context=NsLink(), neuron=NsNeuron(NstreamLLM.mistral_7b()))

    # ns_graph_sink = NsLink()

    

    # ns_graph.terminate()
