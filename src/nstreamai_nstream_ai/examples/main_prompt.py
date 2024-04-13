from core.nsinit import NsInit
from core.nsnode import NsNode, NsLink, NsProvider, NsProviderType, Nstream
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

    #  Node 1: User Interaction Summarization and Insight Generation
    #  Objective: 

    prompt_event = Nstream.event()
    #  Prompt for insight generation
    ns_node_1_prompt_text = f"Generate a general insight using a input user's data - {prompt_event}" 

    ns_node_1 = NsNode(
        node_name="GraphNode1",
        prompt=NsLink(
            socket=conn,
            provider=NsProvider(type=NsProviderType().Source).mongodb(),
            prompt_text=ns_node_1_prompt_text
        ),
        neuron=NsNeuron(NstreamLLM.mistral_7b()),
        socket=conn)
    logger.info("GraphNode1 configured")

    
    ns_graph_sink = NsLink(
        socket=conn,
        provider=NsProvider(type=NsProviderType().Sink).terminal(),
    )
    logger.info("Graph sink configured")

    ns_graph = NsGraph(conn).start(ns_node_1).submit(ns_graph_sink)
    logger.info("Graph execution started")

    ns_graph.terminate(run_time=6)
    logger.info("Graph execution terminated")

    print("Execution Completed")
    logger.info("Main execution completed")
