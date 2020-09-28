import requests
import jiraConfig
from requests.auth import HTTPBasicAuth
import json

url = jiraConfig.slackWebhookUrl

headers = {
    "Content-Type": "application/json"
}

def sendToSlack(text):
    payload = json.dumps({
        "text": text
    })
    requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )

