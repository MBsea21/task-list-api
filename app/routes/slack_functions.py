from flask import request, jsonify, abort, make_response
import requests
import os


def send_message(message):
    slack_channel = os.environ.get("SLACK_CHANNEL")
    slack_url = os.environ.get("SLACK_URL")

    slack_api_token = os.getenv("SLACK_BOT_TOKEN")
    payload = {
        "channel": slack_channel,
        "token": slack_api_token,
        "text": message
        }
        
    response = requests.post(slack_url, data=payload)
    message_sent = check_response(response)
    if message_sent is True:
        return make_response({"message":"Slack message has been sent"}, 200)
    else: 
        abort(make_response({"error":"something else broke, line 22 was met"}, 400))

def check_response(response):

    if response.status_code == 200:
        return True
    else:
        error_message = "could not post to slack, was unable to call slack api. Check slack url, token, and request body"
        abort(make_response({"error": error_message},400))



    