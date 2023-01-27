import requests

result = requests.get("https://reqres.in/api/users", params={"page": 2})
print(result.json())