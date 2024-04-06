import json

def create_node_detail_mutation(name, datasource, datasink):
    datasource_str = json.dumps(datasource).replace('"', '\\"')
    datasink_str = json.dumps(datasink).replace('"', '\\"')
    return f"""
    mutation {{
      createNodeDetail(
        name: "{name}"
        datasource: "{datasource_str}"
        datasink: "{datasink_str}"
      ) {{
        ... on NodeType {{
          id
          name
          orgId
          userId
          datasource
          datasink
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def update_node_detail_mutation(id, name, datasource, datasink):
    datasource_str = json.dumps(datasource).replace('"', '\\"')
    datasink_str = json.dumps(datasink).replace('"', '\\"')
    return f"""
    mutation {{
      updateNodeDetail(
        id: "{id}"
        name: "{name}"
        datasource: "{datasource_str}"
        datasink: "{datasink_str}"
      ) {{
        ... on NodeType {{
          id
          name
          orgId
          userId
          datasource
          datasink
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def create_token_detail_mutation(model_name, tokens, node_id):
    return f"""
    mutation {{
      createTokenDetail(
        modelName: "{model_name}"
        tokens: {tokens}
        nodeId: {node_id}
      ) {{
        ... on TokenDetailType {{
          id
          orgId
          userId
          modelName
          tokens
          nodeId
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def update_token_detail_mutation(id, model_name, tokens):
    return f"""
    mutation {{
      updateTokenDetail(
        id: "{id}"
        modelName: "{model_name}"
        tokens: {tokens}
      ) {{
        ... on TokenDetailType {{
          id
          orgId
          userId
          modelName
          tokens
          nodeId
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def create_io_throughput_mutation(node_id, input_throughput, output_throughput):
    return f"""
    mutation {{
      createIoThroughput(
        nodeId: {node_id}
        inputThroughput: {input_throughput}
        outputThroughput: {output_throughput}
      ) {{
        ... on IOThroughputType {{
          id
          nodeId
          orgId
          userId
          inputThroughput
          outputThroughput
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def update_io_throughput_mutation(id, input_throughput, output_throughput):
    return f"""
    mutation {{
      updateIoThroughput(
        id: "{id}"
        inputThroughput: {input_throughput}
        outputThroughput: {output_throughput}
      ) {{
        ... on IOThroughputType {{
          id
          nodeId
          orgId
          userId
          inputThroughput
          outputThroughput
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def create_inference_latency_mutation(node_id, llm_inference_speed, context_retrieval_speed, total_node_inference_speed):
    return f"""
    mutation {{
      createInferenceLatency(
        nodeId: {node_id}
        llmInferenceSpeed: {llm_inference_speed}
        contextRetrievalSpeed: {context_retrieval_speed}
        totalNodeInferenceSpeed: {total_node_inference_speed}
      ) {{
        ... on InferenceLatencyType {{
          id
          nodeId
          orgId
          userId
          llmInferenceSpeed
          contextRetrievalSpeed
          totalNodeInferenceSpeed
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """

def update_inference_latency_mutation(id, llm_inference_speed, context_retrieval_speed, total_node_inference_speed):
    return f"""
    mutation {{
      updateInferenceLatency(
        id: "{id}"
        llmInferenceSpeed: {llm_inference_speed}
        contextRetrievalSpeed: {context_retrieval_speed}
        totalNodeInferenceSpeed: {total_node_inference_speed}
      ) {{
        ... on InferenceLatencyType {{
          id
          nodeId
          orgId
          userId
          llmInferenceSpeed
          contextRetrievalSpeed
          totalNodeInferenceSpeed
        }}
        ... on ErrorType {{
          message
        }}
      }}
    }}
    """
