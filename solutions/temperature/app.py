
import requests
import json

url = "https://api-service-player1.apps.cluster-cq44p.cq44p.sandbox766.opentlc.com/api/v1/temperature"

response = requests.get(url)

data = response.json()

temperatures = [room['temperature'] for room in data['rooms']]
average_temperature = sum(temperatures) / len(temperatures)
print(average_temperature)
