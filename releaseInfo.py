import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

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

print(fixVersionsList)

#jql = "project = OTP AND fixVersion = \""+fixVersionsList[0]+"\""
jql = "project = OTP AND fixVersion = \"Release Template\""
payload = json.dumps({
    "jql": jql,
    "fields": [
        "issuelinks"
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
projectTeam = []

for item in jsonArray:
  issueLinks = item['fields']['issuelinks']
  if len(issueLinks) == 0:
    continue
  for issue in issueLinks:
      if issue['outwardIssue'] != None:
          if issue['outwardIssue']['key'].find('MM-') != -1:
              print("Release version: " ++ "Player: "+item['key']+" Live Product: "+issue['outwardIssue']['key'])


#print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))

