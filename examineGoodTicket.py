import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

# Purpose
# 1. 
def queryCommentsCount(startAt, maxResult):
    url = jiraConfig.httpResource["url"]

    headers = {
        "Authorization": jiraConfig.httpResource["authorization"],
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "jql": "project = OTP AND issuekey >= OTP-13 order by created DESC",
        "fields": [
            "description"
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
    issueArray = jsonText['issues']

    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))
    for issue in issueArray:
        description = issue['fields']['description']
        if description == None:
            print("Empty description: " + issue['key'])
            continue
        contentArray = description['content']
        
        if len(contentArray) < 3:
            print("Less information: " + issue['key'])
    return jsonText['total']

maxResult = 100
startAt = 0

totalCount = queryCommentsCount(startAt, maxResult)

while startAt + maxResult < totalCount:
    startAt += maxResult 
    queryCommentsCount(startAt, maxResult)

# slackWebhook.sendToSlack(slackMessage)
