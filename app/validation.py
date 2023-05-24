'''
import requests

# Define the endpoint
url = "http://api.aviationstack.com/v1/flights"

# Define the header parameters. In this case, you only need your access key.
params = {
    # replace with your actual access key
    "access_key": "c9f0cf7dd54b33ad111029bada9c934e",
    "flight_iata": "FI115"
}

# Make the request
response = requests.get(url, params=params)

# Parse the response
data = response.json()

# Now you can use the data object which contains the parsed JSON from the API.
print(data)
'''
