#!/usr/bin/env python3

import flask
import threading
from werkzeug.middleware.proxy_fix import ProxyFix

from config import CLIENT_STATE, PROXY
from forward import forward_email
from subscription import init_subscriptions, list_subscriptions, resubscribe, subscribe, unsubscribe

# Initialize Flask server
# NOTE: THIS IS DIFFERENT THAN THE AUTH APP
app = flask.Flask(__name__)

# If Flask is behind Reverse Proxy let it know
if PROXY:
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=PROXY['FOR'], x_proto=PROXY['PROTO'], x_host=PROXY['HOST'], x_prefix=PROXY['PREFIX']
    )

# Initialize subscriptions before and in the background of web server starting
threading.Thread(target=init_subscriptions).start()


@app.route('/sub', methods=['POST'])
# Callback endpoint to process incoming notifications
def handle_sub_post():
    # Subscription verification confirmation
    if "text/plain" in flask.request.content_type:
        return flask.request.args['validationToken']

    # Handle subscription event
    elif "application/json" in flask.request.content_type:
        notification = flask.request.get_json()
        # Read the notification
        if notification['value'] and len(notification['value']) > 0:
            # Access the list in the notification
            for item in notification['value']:
                # Check to make sure the client state matches the one provided in config
                if item['clientState'] == CLIENT_STATE:
                    # Check to make sure the notification is about a new item
                    if 'changeType' in item and item['changeType'] == "created":
                        # Check to make sure the notification is about an email
                        if item['resourceData']['@odata.type'] == "#Microsoft.Graph.Message":
                            # Retrieve the message ID from the notification
                            message_id = item['resourceData']['id']
                            # Forward the email using the message_id (Standard forward or Transparent based on config)
                            forward_email(message_id)
                            # Acknowledge receipt of the notification
                            # TODO: Add error coming back through chain
                            return "", 202
                        else:
                            print("Unexpected odata.type")
                            print(
                                f"odata.type: {item['resourceData']['@odata.type']}")
                    elif 'lifecycleEvent' in item and item['lifecycleEvent']:
                        lifecycleEvent = item['lifecycleEvent']
                        match lifecycleEvent:
                            case "reauthorizationRequired":
                                resubscribe(item['subscriptionId'])
                            case "subscriptionRemoved":
                                subscribe()
                            case "missed":
                                print("Missing notifications. Possible ratelimit")
                                # TODO: Delta support
                            case _:
                                # If unknown lifecycleEvent return error
                                return "", 501
                        # If known lifecycleEvent return good status
                        return "", 202
                    else:
                        print("Unknown changeType and no lifecycleEvent")
                        if 'changeType' in item:
                            print(f"changeType: {item['changeType']}")
                else:
                    print("Mismatched clientState")
                    print(f"clientState: {item['clientState']}")
        else:
            print("Notification didn't seem to have valid content")
        # If any error return 501 and print notification content to terminal
        print(f"Notification: {notification}")
        return "", 501


@app.route('/sub', methods=['GET'])
def handle_sub_get():
    subscribe()
    return "", 200


@app.route('/unsub', methods=['GET'])
def handle_unsub():
    unsubscribe(flask.request.args['subscriptionId'])
    return "", 200


@app.route('/resub', methods=['GET'])
def handle_resub():
    resubscribe(flask.request.args['subscriptionId'])
    return "", 200


@app.route('/list', methods=['GET'])
def handle_list():
    list_subscriptions()
    return "", 200


if __name__ == "__main__":
    # Host the flask app on port 5000 accessible from any local device for development
    # For production deployment use the command `gunicorn main:app` for quick setup
    # For more info about production deployment read the README
    app.run(host="0.0.0.0", port=5000)
