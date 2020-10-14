import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

# Purpose: You can find a ticket not have any "description" or issue links, it means that ticket's content is not a good story and clearly mission
# To modify jql that adapt to your project setting

userDictionary = { }

def queryCommentsCount(startAt, maxResult):
    url = jiraConfig.httpResource["url"]

    headers = {
        "Authorization": jiraConfig.httpResource["authorization"],
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "jql": "project = OTP AND issuekey >= OTP-1999 AND status not in (Done, RESOLVED, \"Won't Fix\", Close) order by created DESC",
        "fields": [
            "description",
            "issuelinks",
            "reporter"
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
        fields = issue['fields']
        key = issue['key']
        reporterDisplayName = fields['reporter']['displayName']
        description = fields['description']
        if description == None:
            issuelinks = fields['issuelinks']
            if issuelinks == None or len(issuelinks) == 0:
                if userDictionary.get(reporterDisplayName) == None:
                    userDictionary[reporterDisplayName] = [key]
                else:
                    userDictionary[reporterDisplayName].append(key)
            continue
        contentArray = description['content']
        
        if len(contentArray) < 1:
            print("Less information: " + key)
    return jsonText['total']

maxResult = 100
startAt = 0

totalCount = queryCommentsCount(startAt, maxResult)

while startAt + maxResult < totalCount:
    startAt += maxResult 
    queryCommentsCount(startAt, maxResult)

slackMessage = "Please enhance the ticket's description or give links which help reviewer get more information \n " 

for key, value in userDictionary.items():
  appendStr = key + ": " + ', '.join(value) + "\n"
  slackMessage += appendStr

print(slackMessage)
#slackWebhook.sendToSlack(slackMessage)
