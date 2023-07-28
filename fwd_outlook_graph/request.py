import datetime

import requests

def format_recipient(recipient):
    return {
        'emailAddress': {
            'address': recipient
        }
    }

def get_time_str():
    time = datetime.datetime.now() + datetime.timedelta(minutes = 4230)
    return str(time).replace(" ", "T") + "0Z"

def get_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}

def forward_email(access_token, message_id, to_recipients):
    # Calling graph using the access token
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/forward'
    json = {
        'Comment': "",
        'ToRecipients': [
            ]
        }
    for recipient in to_recipients:
        json['ToRecipients'].append(format_recipient(recipient))
    graph_data = requests.post(url, headers=get_headers(access_token), json=json)
    print("Graph API call result: %s" % graph_data.text)
    print(graph_data.status_code)

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
    print("Subscription call result: %s" % subscribe_data.text)
    print(subscribe_data.status_code)

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
    print("Unsubscription call result: %s" % unsubscribe_data.text)
    print(unsubscribe_data.status_code)