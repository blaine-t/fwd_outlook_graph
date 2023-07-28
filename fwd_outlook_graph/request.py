import datetime

import requests

def format_recipient(recipient):
    return {
        'emailAddress': {
            'address': recipient
        }
    }

def handle_recipients(json, config):
    for recipient in config['to_recipients']:
        json['ToRecipients'].append(format_recipient(recipient))
    return json


def get_time_str():
    time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = 4230)
    return str(time).replace(" ", "T").replace("+00:00", "0Z")

def get_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}

def get_message(access_token, message_id):
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}'
    return requests.get(url, headers=get_headers(access_token)).json()

def get_attachments(access_token, message_id):
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments'
    return requests.get(url, headers=get_headers(access_token)).json()

def handle_attachments(json, attachments):
    for attachment in attachments["value"]:
        json["message"]["attachments"].append({
            "@odata.type": attachment["@odata.type"],
            "name": attachment["name"],
            "contentType": attachment["contentType"],
            "contentBytes": attachment["contentBytes"]
        })
    return json

def send_message(access_token, message, config):
    url = f'https://graph.microsoft.com/v1.0/me/sendMail'
    json = {
        "message": {
            "subject": message['subject'],
            "body": message['body'],
            "toRecipients": [],
            "attachments": []
        },
        "saveToSentItems": "false"
    }
    # Handle attachments
    if message['hasAttachments']:
        attachments = get_attachments(access_token, message['id'])
        json = handle_attachments(json, attachments)
    catch_all = config["transparent_config"]["catch_all"]
    if catch_all:
        # Add the original sender plus the catch all suffix to the toRecipients
        json["message"]["toRecipients"].append(format_recipient(f"{str(message['sender']['emailAddress']['address']).split('@')[0]}{catch_all}"))
    else:
        json = handle_recipients(json, config)

    graph_data = requests.post(url, headers=get_headers(access_token), json=json)
    if graph_data.status_code == 202:
        print(f"Successfully sent: {message['id']}")
    else:
        print(f"[{graph_data.status_code}] Send call result: {graph_data.text}")
    

def forward_email(access_token, message_id, config):
    if config["transparent_config"]["enabled"]:
        transparent_forward_email(access_token, message_id, config)
    else:
        # Calling graph using the access token
        url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/forward'
        json = {
            'Comment': "",
            'ToRecipients': [
                ]
            }
        json = handle_recipients(json, config)
        graph_data = requests.post(url, headers=get_headers(access_token), json=json)
        if graph_data.status_code == 202:
            print(f"Successfully forwarded: {message_id}")
        else:
            print(f"[{graph_data.status_code}] Forward call result: {graph_data.text}")

def transparent_forward_email(access_token, message_id, config):
    # Calling graph using the access token
    message = get_message(access_token, message_id)
    send_message(access_token, message, config)

def subscribe(access_token, config):
    # Calling graph using the access token
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    # Add 4230 minutes to the current time to enable the longest subscription expiry GRAPH allows
    json = {
        "changeType": "created",
        "notificationUrl": config["subscription_url"],
        "resource": "me/mailFolders('Inbox')/messages",
        "expirationDateTime": get_time_str(),
        "clientState": config["client_state"]
    }
    subscribe_data = requests.post(url, headers=get_headers(access_token), json=json)
    if subscribe_data.status_code == 201:
        print(f"New subscription ID: {subscribe_data.json()['id']}")
    else:
        print(f"[{subscribe_data.status_code}] Subscription call result: {subscribe_data.text}")

def resubscribe(access_token, subscription_id):
    # Calling graph using the access token
    url = f'https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}'
    json = {
        "expirationDateTime": get_time_str()
    }
    resubscribe_data = requests.patch(url, headers=get_headers(access_token), json=json)
    print("Resubscription call result: %s" % resubscribe_data.text)
    print(resubscribe_data.status_code)

def unsubscribe(access_token, subscription_id):
    # Calling graph using the access token
    url = f'https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}'
    unsubscribe_data = requests.delete(url, headers=get_headers(access_token))
    if unsubscribe_data.status_code == 204:
        print(f"Successfully unsubscribed: {subscription_id}")
    else:
        print(f"[{unsubscribe_data.status_code}] Unsubscription call result: {unsubscribe_data.text}")