import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

def queryCommentsCount(startAt, maxResult):
    url = jiraConfig.httpResource["url"]

    headers = {
        "Authorization": jiraConfig.httpResource["authorization"],
        "Content-Type": "application/json"
    }

    # To list tickets that do not have assignee
    payload = json.dumps({
        "jql": "project = OTP AND issuekey >= OTP-1999 AND status in (\"In Progress\", Open, Pending, Verifying) order by created DESC",
        "fields": [
            "comment"
        ],
        "startAt": startAt,
        "maxResults": maxResult
    })
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )
    jsonText = json.loads(response.text)
    jsonArray = jsonText['issues']

    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))
    for item in jsonArray:
        commentTotal = item['fields']['comment']['total']
        if commentTotal > 0:
            print("Name " + item['key'] + " comments count: " + str(commentTotal))
    return jsonText['total']


maxResult = 20
startAt = 0

totalCount = queryCommentsCount(startAt, maxResult)

while startAt + maxResult < totalCount:
    startAt += maxResult 
    queryCommentsCount(startAt, maxResult)
# slackWebhook.sendToSlack(slackMessage)
