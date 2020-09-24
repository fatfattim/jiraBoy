import os
import logging
import json

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    """Update the onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    event = payload.get("event", {})
    
    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")
    print(json.dumps(payload, sort_keys=True, indent=8, separators=(",", ": ")))


# ============== Message Events ============= #
# Subscribe to only the message events that mention your app or bot
@slack_events_adapter.on("app_mention")
def message(payload):

    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    event = payload.get("event", {})
    text = event.get("text")
    print(json.dumps(payload, sort_keys=True, indent=8, separators=(",", ": ")))

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
