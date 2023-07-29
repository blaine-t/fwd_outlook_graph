#!/usr/bin/env python3

import logging

import flask

from auth import get_access_token
from config import CLIENT_STATE
from request import forward_email, subscribe, resubscribe, unsubscribe, list_subscriptions

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

# Initialize Flask server
app = flask.Flask(__name__)

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
                if item["clientState"] == CLIENT_STATE:
                    if "changeType" in item and item["changeType"] == "created":
                        if item["resourceData"]["@odata.type"] == "#Microsoft.Graph.Message":
                            # Retrieve the message ID from the notification
                            message_id = item["resourceData"]["id"]
                            # Now you can fetch the message content using the message_id and forward the email
                            forward_email(get_access_token(), message_id)
                            # Acknowledge receipt of the notification
                            return "", 204
                        else:
                            print("Unexpected odata.type")
                            print(f'odata.type: {item["resourceData"]["@odata.type"]}')
                    elif "lifecycleEvent" in item and item["lifecycleEvent"]:
                        lifecycleEvent = item["lifecycleEvent"]
                        if lifecycleEvent == "reauthorizationRequired":
                            resubscribe(get_access_token(), item["subscriptionId"])
                            return "", 202
                        elif lifecycleEvent == "subscriptionRemoved":
                            subscribe(get_access_token())
                            return "", 202
                        elif lifecycleEvent == "missed":
                            print("Missing notifications. Possible ratelimit")
                            # TODO: Delta support
                            return "", 202
                        # If unknown lifecycleEvent return error
                        return "", 501
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
    subscribe(get_access_token())
    return "", 200

@app.route("/unsub", methods=["GET"])
def handle_unsub():
    unsubscribe(get_access_token(), flask.request.args['subscriptionId'])
    return "", 200

@app.route("/resub", methods=["GET"])
def handle_resub():
    resubscribe(get_access_token(), flask.request.args['subscriptionId'])
    return "", 200

@app.route("/list", methods=["GET"])
def handle_list():
    list_subscriptions(get_access_token())
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)