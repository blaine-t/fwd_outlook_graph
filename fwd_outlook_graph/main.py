#!/usr/bin/env python3

import flask
import threading
from werkzeug.middleware.proxy_fix import ProxyFix

from config import CLIENT_STATE, DEVELOPMENT, PROXY
from forward import forward_email
from subscription import init_subscriptions, list_subscriptions, resubscribe, subscribe, unsubscribe, get_user, get_subscriptions

# Initialize Flask server with static_url_path / to allow for favicon support
# NOTE: THIS IS DIFFERENT THAN THE AUTH APP
app = flask.Flask(__name__, static_url_path='/')

# If Flask is behind Reverse Proxy let it know
if PROXY:
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=PROXY['FOR'], x_proto=PROXY['PROTO'], x_host=PROXY['HOST'], x_prefix=PROXY['PREFIX']
    )

# Initialize subscriptions before and in the background of web server starting
threading.Thread(target=init_subscriptions).start()


@app.route('/sub', methods=['POST'])
def handle_sub_post():
    """Handle POST request sent to the server by Microsoft for different subscription notifications"""
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
                            # Acknowledge receipt of the notification or failure to handle the notification
                            status_code = forward_email(message_id)
                            return "", status_code
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
                                # Never received subscriptionRemoved so I can't test if this works. Adding a notification print for more info.
                                print(notification)
                                subscribe()
                            case "missed":
                                # Delta support could be added here but I cannot even when I try to force it get a missed lifecycleEvent
                                # Until I receive one there is no way for me to test an implementation so I will leave this for the future for now
                                print(notification)
                                print("Missing notifications. Possible ratelimit")
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


# If application is under development expose admin panel and functions
if DEVELOPMENT:
    @app.route('/sub', methods=['GET'])
    def handle_sub_get():
        """Subscribe to new notification when GET /sub"""
        response = subscribe()
        response_text = response[0]
        response_code = response[1]
        return response_text, response_code

    @app.route('/unsub', methods=['GET'])
    def handle_unsub():
        """Unsubscribe to new notification when GET /unsub with a query of the subId"""
        response = unsubscribe(flask.request.args['subId'])
        response_text = response[0]
        response_code = response[1]
        return response_text, response_code

    @app.route('/resub', methods=['GET'])
    def handle_resub():
        """Resubscribe to new notification when GET /resub with a query of the subId"""
        response = resubscribe(flask.request.args['subId'])
        response_text = response[0]
        response_code = response[1]
        return response_text, response_code

    @app.route('/list', methods=['GET'])
    def handle_list():
        """A GET request to /list sends a list of all the current subscriptions for this instance"""
        response = list_subscriptions()
        response_text = response[0]
        response_code = response[1]
        return response_text, response_code

    @app.route('/admin', methods=['GET'])
    def handle_admin_get():
        """Render the admin panel to the user at /admin"""
        return flask.render_template("admin.html", subscriptions=list_subscriptions()[0], user=get_user())


if __name__ == "__main__":
    # Host the flask app on port 5000 accessible from any local device for development
    # For production deployment use the command `gunicorn main:app` for quick setup
    # For more info about production deployment read the README
    app.run(host="0.0.0.0", port=5000)
