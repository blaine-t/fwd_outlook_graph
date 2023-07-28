#!/usr/bin/env python3

"""
The configuration file (default config.json) would look like this:
{
    "authority": "https://login.microsoftonline.com/common",
    "client_id": "your_client_id",
}
    # You can find the other permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    # To restrict who can login to this app, you can find more Microsoft Graph API endpoints from Graph Explorer
    # https://developer.microsoft.com/en-us/graph/graph-explorer

You can then run this script:
    ./main.py
"""

from auth import get_access_token
from cache import get_cache
from config import load_config
from request import forward_email, subscribe

config_file_path = "config.json"  # Update the file path if the config file is in a different location
cache_file_path = "token_cache.bin" # Update the file path if the cache is in a different location

# Optional logging
# logging.basicConfig(level=logging.DEBUG)

import flask

# Initialize Flask server
app = flask.Flask(__name__)

# Callback endpoint to process incoming notifications
@app.route("/sub", methods=["POST"])
def handle_notification():
    print("Got notif!")
    print(flask.request.content_type)
    if "text/plain" in flask.request.content_type:
        # Respond to Microsoft's validation request during webhook setup
        print(flask.request.args['validationToken'])
        response = app.response_class(
                response=flask.request.args['validationToken'],
                status=200,
                mimetype='text/plain'
            )
        return response
    elif 'application/json' in flask.request.content_type:
        notification = flask.request.get_json()
        # Handle the new message notification here
        if notification["value"]:
            for item in notification["value"]:
                if item["resourceData"]["@odata.type"] == "#Microsoft.Graph.Message":
                    # Retrieve the message ID from the notification
                    message_id = item["resourceData"]["id"]
                    config = load_config(config_file_path)
                    cache = get_cache(cache_file_path)
                    forward_email(get_access_token(cache, config), message_id, config["to_recipients"])
                    # Now you can fetch the message content using the message_id and forward the email

    return "", 204  # Acknowledge receipt of the notification

@app.route("/", methods=["GET"])
def main():
    config = load_config(config_file_path)
    cache = get_cache(cache_file_path)
    access_token = get_access_token(cache, config)
    subscribe(access_token, config["subscription_url"])
    # send_email(access_token, config['to_recipients'])
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)