import json
import os
import random

import requests

directory: str = "data/spawner/mock_smard_api_data"
base_url: str = "https://www.smard.de/app/chart_data/1223/50Hertz"
index_url: str = f"{base_url}/index_quarterhour.json"
data_url: str = r"{base_url}/1223_50Hertz_quarterhour_{timestamp}.json"

response: requests.Response = requests.get(index_url)
indices: dict = response.json()
indices["timestamps"] = indices["timestamps"][0:10]
filename: str = os.path.join(directory, "index.json")
with open(filename, "w") as file:
    json.dump(indices, file)
timestamps: list[int] = indices["timestamps"]

for idx, timestamp in enumerate(timestamps):
    url: str = data_url.format(base_url=base_url, timestamp=timestamp)
    response = requests.get(url)
    data: list[list[int, float]] = response.json()

    series = [
        (timestamp, random.random() if value else None)
        for timestamp, value in data["series"]
    ]
    data["series"] = series

    filename = os.path.join(directory, f"data_{timestamp}.json")
    with open(filename, "w") as file:
        json.dump(data, file)
    print(f"{idx + 1}/{len(timestamps)}: {timestamp}")
