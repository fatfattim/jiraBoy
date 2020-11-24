import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

url = "https://xxx.atlassian.net//rest/agile/1.0/issue/OTP-2576"

headers = {
    "Authorization": jiraConfig.httpResource["authorization"],
    "Accept": "application/json"
}

response = requests.request(
    "GET",
    url,
    headers=headers
)

jsonText = json.loads(response.text)
#jsonArray = jsonText['issues']
# you can print the response from below codes
print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))
