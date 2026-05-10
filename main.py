import requests
import json

url="https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata"
res = requests.get(url)
data = res.json()

print(json.dumps(data, indent=4, ensure_ascii=False))