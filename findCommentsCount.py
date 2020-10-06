import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

userDictionary = { }

def queryCommentsCount(startAt, maxResult):
    url = jiraConfig.httpResource["url"]

    headers = {
        "Authorization": jiraConfig.httpResource["authorization"],
        "Content-Type": "application/json"
    }

    # To list tickets that do not have assignee
    payload = json.dumps({
        "jql": "project = OTP AND issuekey >= OTP-13 order by created DESC",
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

    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))
    for item in jsonArray:
        commentJson = item['fields']['comment']
        commentTotal = commentJson['total']
        if commentTotal > 0:
            for comment in commentJson['comments']:
                count = 1
                displayName = comment['author']['displayName']
                if userDictionary.get(displayName) != None:
                    count = userDictionary.get(displayName)
                    count += 1

                userDictionary[displayName] = count
                
    return jsonText['total']

maxResult = 20
startAt = 0

totalCount = queryCommentsCount(startAt, maxResult)

while startAt + maxResult < totalCount:
    startAt += maxResult 
    queryCommentsCount(startAt, maxResult)

print(userDictionary)
# slackWebhook.sendToSlack(slackMessage)
