import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import informProjectTeam

url = jiraConfig.httpResource["url"]

headers = {
    "Authorization": jiraConfig.httpResource["authorization"],
    "Content-Type": "application/json"
}

payload = json.dumps({
    "jql": "project = OTP AND issuetype = Release AND Sprint in openSprints() AND Sprint not in futureSprints() ORDER BY created DESC",
    "fields": [
        "fixVersions"
    ],
    "startAt": 0,
    "maxResults": 20
})

response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers
)

jsonText = json.loads(response.text)
jsonArray = jsonText['issues']
fixVersionsList = []

# you can print the response from below codes
for item in jsonArray:
  name = item['fields']['fixVersions'][0]['name']
  fixVersionsList.append(name)

informProjectTeam.informByReleaseVersionList(fixVersionsList)