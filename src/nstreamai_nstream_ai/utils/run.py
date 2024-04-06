import requests
import random
import string
import json
from template import (
    create_node_detail_mutation,
    create_token_detail_mutation, 
    create_io_throughput_mutation, 
    create_inference_latency_mutation
)

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_json():
    return json.dumps({random_string(5): random_string(5) for _ in range(random.randint(1, 1))})

def generate_synthetic_data():
    model_names = ["Mistral-7B", "LLAMA2-7B"]  # List of model names
    model_name = random.choice(model_names)
    tokens = random.randint(50, 500)
    input_throughput = random.uniform(50, 1000)
    output_throughput = random.uniform(50, 1000)
    llm_inference_speed = random.uniform(10, 5000)
    context_retrieval_speed = random.uniform(10, 5000)
    total_node_inference_speed = llm_inference_speed + context_retrieval_speed + random.uniform(10, 100)

    return {
        "model_name": model_name,
        "tokens": tokens,
        "input_throughput": input_throughput,
        "output_throughput": output_throughput,
        "llm_inference_speed": llm_inference_speed,
        "context_retrieval_speed": context_retrieval_speed,
        "total_node_inference_speed": total_node_inference_speed
    }


def send_graphql_request(url, headers, mutation):
    payload = json.dumps({"query": mutation})
    response = requests.post(url, headers=headers, data=payload)
    return response

url = "http://0.0.0.0:8000/graphql"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWVwYWtAbnN0cmVhbS5haSIsImV4cCI6MTcxNzYwOTU2N30.0idoJ50sN4LnmPiiV6N5xFDGdYdO0mi2Oxaeh-Nk7i4'
}

node_id_list = []

node_name = f"Node 1"
datasource = {"S3": "value"}
datasink = {"Node 2": "value"}
mutation = create_node_detail_mutation(node_name, datasource, datasink)
response = send_graphql_request(url, headers, mutation)
node_id_list.append(json.loads(response.text).get("data").get("createNodeDetail").get("id"))

node_name = f"Node 2"
datasource = {"Node 1": "value"}
datasink = {"S3": "value"}
mutation = create_node_detail_mutation(node_name, datasource, datasink)
response = send_graphql_request(url, headers, mutation)
node_id_list.append(json.loads(response.text).get("data").get("createNodeDetail").get("id"))

try:
    while True:
        # Generate synthetic data
        data = generate_synthetic_data()
        data["node_id"] = random.choice(node_id_list)
        
        mutation = create_token_detail_mutation(data["model_name"], data["tokens"], data["node_id"])
        response = send_graphql_request(url, headers, mutation)

        mutation = create_io_throughput_mutation(data["node_id"], data["input_throughput"], data["output_throughput"])
        response = send_graphql_request(url, headers, mutation)

        mutation = create_inference_latency_mutation(data["node_id"], 
                                                     data["llm_inference_speed"], 
                                                     data["context_retrieval_speed"], 
                                                     data["total_node_inference_speed"]
                                                    )
        response = send_graphql_request(url, headers, mutation)

except KeyboardInterrupt:
    print("Loop interrupted by user.")


