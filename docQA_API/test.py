# example to upload a pdf file
import requests


url = 'http://127.0.0.1:8000/upload'
file = {'file': open('example.pdf', 'rb')}
resp = requests.post(url=url, files=file) 
print(resp.json())

# example post request to query
# curl -X POST "http://127.0.0.1:8000/query/" \
# -H "Content-Type: application/json" \
# -d '{"query":{"username":"John","password":"abc123","querytext":"What is the backdoor mechanism?"}}'

