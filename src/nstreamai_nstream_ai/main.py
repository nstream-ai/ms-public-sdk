from core.nsinit import NsInit
from core.nsnode import NsNode, NsLink, NsProvider, NsProviderType
from core.nsneuron import NsNeuron, NstreamLLM
from core.nsgraph import NsGraph
from utils.logger import logger
import sys

if __name__ == "__main__":
    try:
        logger.info("Starting main execution")
        conn = NsInit(api_key="NZ4RPFAF3M0", username="admin@nstream.ai", password="nstream.cloud").connect()
        logger.info("Connected to NsInit")
    except Exception as e:
        logger.exception("Exception occurred while initializing NsInit")
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
            context_tranform_prompt_text="fetch all the bank details from the messages"),
        neuron=NsNeuron(NstreamLLM.mistral_7b()),
        socket=conn)
    logger.info("GraphNode1 configured")

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
    logger.info("GraphNode2 configured")

    ns_graph_sink = NsLink(
        socket=conn,
        provider=NsProvider(type=NsProviderType().Sink).terminal(),
    )
    logger.info("Graph sink configured")

    ns_graph = NsGraph(conn).start(ns_node_1).end(ns_node_2).submit(ns_graph_sink)
    logger.info("Graph execution started")

    ns_graph.terminate(run_time=100)
    logger.info("Graph execution terminated")

    print("Execution Completed")
    logger.info("Main execution completed")
