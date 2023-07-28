#!/usr/bin/env python3

# Other script imports

from auth import get_access_token
from cache import get_cache
from config import load_config
from request import forward_email, subscribe, resubscribe, unsubscribe

import flask
import logging

# Update the file path if the cache or config file is in a different location
cache_file_path = "token_cache.bin"
config_file_path = "config.json"

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

# Initialize Flask server
app = flask.Flask(__name__)

# Initialize cache and config
cache = get_cache(cache_file_path)
config = load_config(config_file_path)

# Callback endpoint to process incoming notifications
@app.route("/sub", methods=["POST"])
def handle_sub_post():
    # Subscription verification confirmation
    if "text/plain" in flask.request.content_type:
        response = app.response_class(
                response=flask.request.args['validationToken'],
                status=200,
                mimetype='text/plain'
            )
        return response
    # Handle subscription event
    elif 'application/json' in flask.request.content_type:
        notification = flask.request.get_json()
        # Read the notification
        if notification["value"]:
            # Access the list in the notification
            for item in notification["value"]:
                # Check to make sure the client state matches the one provided
                if item["clientState"] == config["client_state"]:
                    if item["changeType"] == "created":
                        if item["resourceData"]["@odata.type"] == "#Microsoft.Graph.Message":
                            # Retrieve the message ID from the notification
                            message_id = item["resourceData"]["id"]
                            # Now you can fetch the message content using the message_id and forward the email
                            forward_email(get_access_token(cache, config), message_id, config)
                            # Acknowledge receipt of the notification
                            return "", 204
                        else:
                            print("Unexpected odata.type")
                            print(f'odata.type: {item["resourceData"]["@odata.type"]}')
                    elif item["changeType"] == "reauthorizationRequired":
                        resubscribe()
                        # Acknowledge receipt of the notification
                        return "", 204
                    else:
                        print ("Unknown changeType")
                        print(f'changeType: {item["changeType"]}')
                else:
                    print("Mismatched clientState")
                    print(f'clientState: {item["clientState"]}')
                print(f'Notification: {notification}')
                return "", 501

@app.route("/sub", methods=["GET"])
def handle_sub_get():
    subscribe(get_access_token(cache, config), config)
    return "", 200

@app.route("/unsub", methods=["GET"])
def handle_unsub():
    unsubscribe(get_access_token(cache, config), flask.request.args['subscriptionId'])
    return "", 200

@app.route("/resub", methods=["GET"])
def handle_resub():
    resubscribe(get_access_token(cache, config), flask.request.args['subscriptionId'])
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)