#########################################
########################################################
import requests
import json
import random
import string


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
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwaXl1c2hAbnN0cmVhbS5haSIsImV4cCI6MTcxNzgwMjkxMX0.I5DNqBEsTXe3YaSOJ8GHQlhlIMYoM2qrpSYXXskKI9k'
}