from __future__ import print_function

import time

import tqdm

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

api_default = client.DefaultApi(client.ApiClient(configuration))

# Check we can access the API by getting the version number
api_response = api_default.version_get()
print("------ API version -----")
print(api_response)
