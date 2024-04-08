import httpx

# Create an httpx client
http_client = httpx.Client()

# Define the headers
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Define the URL and payload
url = "http://localhost:8000/sign-in"
payload = '{"email": "deepak@nstream.ai", "password": "nstream.cloud"}'

# Make the POST request
response = http_client.post(url=url, headers=headers, data=payload)

# Check the response
if response.status_code == 200:
    print("Sign-in successful")
    # Process the response data as needed
else:
    print(f"Sign-in failed with status code {response.status_code}")
