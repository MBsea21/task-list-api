from flask import Blueprint, request, jsonify
import requests
import os

# Initialize the Blueprint
slack_bp = Blueprint('slack_bp', __name__)

# Slack Bot Token from environment variable

def send_message(slack_url, message):
    slack_api_token = os.getenv("SLACK_BOT_TOKEN")
    headers = {
        "Authorization" : f"Bearer {slack_api_token}",
        "Content-Type": "application/json"
        }
    response = requests.post(url=slack_url, headers=headers, json=message)
    return response
    
    
    # if not channel or not message:
    #     return jsonify({"error": "Channel and message are required"}), 400
    # try:
    #     # Make the chat.postMessage API call
    #     response = client.chat_postMessage(channel=channel, text=message)
    #     response = requests.post(webhook_url, data=dson)
    #     return jsonify({"ok": response["ok"], "message": "Message sent successfully!"}), 200
    # except SlackApiError as e:
    #     # Handle Slack API error and print more details for debugging
    #     error_message = e.response["error"]
    #     print(f"Slack API Error: {error_message}")
    #     return jsonify({"ok": False, "error": error_message}), 400



    