# bls_client.py

import requests
import json
from config import BLS_API_KEY

BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Example: Oranges, Navel, per lb. (Series ID from your list)
series_id = "APU0000711311"

payload = {
    "seriesid": [series_id],
    "startyear": "2020",
    "endyear": "2025",
    "registrationkey": BLS_API_KEY
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(BLS_API_URL, headers=headers,
                         data=json.dumps(payload))

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print("Error:", response.status_code, response.text)
