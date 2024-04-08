from core.nsinit import NsInit
from core.nsnode import NsNode, NsLink
from core.nsneuron import NsNeuron, NstreamLLM
import sys

if __name__ == "__main__":
    try:
        conn = NsInit(api_key="PICKTSB4IFW", username="piyush@nstream.ai", password="nstream.cloud").connect()
    except Exception as e:
        print(e)
        sys.exit()
    # ns_node_1 = NsNode(prompt=NsLink(), context=NsLink(), neuron=NsNeuron(NstreamLLM.mistral_7b()))
    # ns_node_2 = NsNode(prompt=NsLink(), context=ns_node_1.output(), neuron=NsNeuron(NstreamLLM.mistral_7b()))
    # ns_node_3 = NsNode(prompt=ns_node_2.output(), context=NsLink(), neuron=NsNeuron(NstreamLLM.mistral_7b()))

    # ns_graph_sink = NsLink()

    # ns_graph = NsGraph(conn).start(ns_node_1).next_node(ns_node_2).end(ns_node_3).submit(ns_graph_sink)

    # ns_graph.terminate()
