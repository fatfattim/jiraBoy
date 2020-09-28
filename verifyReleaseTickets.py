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

# To list tickets that do not have assignee
payload = json.dumps({
    "jql": "project = OTP AND issuetype = Release AND status in (\"In Progress\", Open, Pending, Verifying) order by created DESC",
    "fields": [
        "assignee",
        "status"
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
ticketNotVerified = []

# you can print the response from below codes
for item in jsonArray:
  assignee = item['fields']['assignee']
  if assignee == None:
    ticketNotVerified.append(item['key'])
    print("Name " + item['key'])

slackMessage = "Please give assignees to these release tickets, " + ', '.join(ticketNotVerified) 
# slackWebhook.sendToSlack(slackMessage)
