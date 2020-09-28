import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json

url = jiraConfig.slackWebhookUrl

headers = {
    "Content-Type": "application/json"
}

def sendToSlack(name, storyPoint):
    payload = json.dumps({
        "text": name + " has "+ storyPoint + " incomplete story sprints"
    })
    requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )

