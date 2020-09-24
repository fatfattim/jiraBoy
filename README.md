# Abstraction

I want to be a python developer.

To shape python skill by developing open source project.

This project integrates Jira's API, and give some threshold to fire alarm on slack message or e-mail system.

## Requirement

1. python
2. confluence account (Need authentication)

## Get Started
### Step 1
Please take a glace about [basic authentication](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#version) , this tutorial from link give many samples codes. such as
1. curl
2. Node.js
3. Java
4. Python
5. PHP

We select the easiest way to request jira api.

"Basic authentication is also available, but you should only use it for tools such as personal scripts or bots. See Security for other integrations for details."

### Step 2
Prepare your [API token](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) here

### Step 3
To modify jiraConfig.py file

### Step 4
python personalStoryPoint.py

## Slack App
please refer to slackApp/app.py, this file contains slack's event api. you could get more detail information
from [python-slackclient](https://github.com/slackapi/python-slackclient)
### Requirements
1. python app.py
2. ngrok http 3000
3. to modify the "Request URL" in Slack App, such as https://xxxxxx.ngrok.io/slack/events