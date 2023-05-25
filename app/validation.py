import requests
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Now you can access the variables
api_key = os.getenv("API_KEY")


# Define the endpoint
url = "http://api.aviationstack.com/v1/flights"

# Define the header parameters. In this case, you only need your access key.
params = {
    # replace with your actual access key
    "access_key": api_key,
    #'flight_date': '2023-05-25',
    'aircraft_registration': 'TF-ISV'
}

# Make the request
response = requests.get(url, params=params)

# Parse the response
data = response.json()

# Now you can use the data object which contains the parsed JSON from the API.
print(data)
