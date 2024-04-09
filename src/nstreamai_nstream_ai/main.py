from core.nsinit import NsInit
from core.nsnode import NsNode, NsLink, NsProvider, NsProviderType
from core.nsneuron import NsNeuron, NstreamLLM
from core.nsgraph import NsGraph
import sys

if __name__ == "__main__":
    try:
        conn = NsInit(api_key="", username="", password="").connect()
    except Exception as e:
        print(e)
        sys.exit()

    ns_node_1 = NsNode(
        node_name="GraphNode1",
        prompt=NsLink(
            socket=conn,
            provider=NsProvider(type=NsProviderType().Source).mongodb(),
            prompt_text="list all the illegal messages related to bank account"
        ),
        context=NsLink(
            socket=conn,
            provider=NsProvider(type=NsProviderType().Source).postgresql(),
            context_tranform_prompt_text=
            "fetch all the bank details from the messages"),
        neuron=NsNeuron(NstreamLLM.mistral_7b()),
        socket=conn)

    ns_node_2 = NsNode(
        node_name="GraphNode2",
        prompt=NsLink(
            socket=conn,
            provider=NsProvider(type=NsProviderType().Source).mongodb(),
            prompt_text="what is the name of user",
        ),
        context=ns_node_1.output(
            context_tranform_prompt_text="process name and address"),
        neuron=NsNeuron(NstreamLLM.llama2_7b()),
        socket=conn)

    ns_graph_sink = NsLink(
        socket=conn,
        provider=NsProvider(type=NsProviderType().Sink).terminal(),
    )
    ns_graph = NsGraph(conn).start(ns_node_1).end(ns_node_2).submit(
        ns_graph_sink)

    ns_graph.terminate(run_time=1)
    print("Execution Completed")
