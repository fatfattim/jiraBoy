import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json
import slackWebhook

url = jiraConfig.httpResource["url"]
# It indicates "Story Points"
storyPointsField = "customfield_10005"
userlist = jiraConfig.userlist

headers = {
    "Authorization": jiraConfig.httpResource["authorization"],
    "Content-Type": "application/json"
}

for user in userlist:
    payload = json.dumps({
        "jql": "project = OTP AND assignee in ("+user+") AND Sprint in openSprints() AND Sprint not in futureSprints() AND Sprint != 1445 ORDER BY priority DESC",
        "fields": [
            "assignee",
            "status",
            storyPointsField
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
    storyPoint = 0.0
	# you can print the response from below codes
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=8, separators=(",", ": ")))
    for item in jsonArray:
        itemStoryPointsField = item['fields'][storyPointsField]
        status = item['fields']['status']['statusCategory']['key']
        if itemStoryPointsField != None and status != "done":
            storyPoint += itemStoryPointsField

    # story point > 13, print alert to slack
    if storyPoint >= 13.0:
      print("Name " + item['fields']['assignee']['displayName'] + ", incomplete story points:" + str(storyPoint))
      slackWebhook.sendToSlack(item['fields']['assignee']['displayName'], str(storyPoint))
    else:
      print("Name " + user)
