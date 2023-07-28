import flask

# Initialize Flask server
app = flask.Flask(__name__)

# Callback endpoint to process incoming notifications
@app.route("/sub", methods=["POST"])
def handle_notification():
    notification = flask.request.get_json()
    if notification["validationToken"]:
        # Respond to Microsoft's validation request during webhook setup
        return flask.jsonify({"validationToken": notification["validationToken"]})

    # Handle the new message notification here
    if notification["value"]:
        for item in notification["value"]:
            if item["resourceData"]["@odata.type"] == "#Microsoft.Graph.Message":
                # Retrieve the message ID from the notification
                message_id = item["resourceData"]["id"]
                print(message_id)
                # Now you can fetch the message content using the message_id and forward the email

    return "", 204  # Acknowledge receipt of the notification