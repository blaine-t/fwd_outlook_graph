import datetime

import requests

def format_recipient(recipient):
    return {
        'emailAddress': {
            'address': recipient
        }
    }

def forward_email(access_token, message_id, to_recipients):
    # Calling graph using the access token
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/forward'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    json = {
        'Comment': "",
        'ToRecipients': [
            ]
        }
    for recipient in to_recipients:
        json['ToRecipients'].append(format_recipient(recipient))
    graph_data = requests.post(url, headers=headers, json=json)
    print("Graph API call result: %s" % graph_data.status_code)

def subscribe(access_token, notificationUrl):
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    headers = { 'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json' }
    time = datetime.datetime.now() + datetime.timedelta(minutes = 4230)
    timeStr = str(time).replace(" ", "T") + "0Z"
    json = {
        "changeType": "created",
        "notificationUrl": notificationUrl,
        "resource": "me/mailFolders('Inbox')/messages",
        "expirationDateTime": timeStr,
    }
    subscribe_data = requests.post(url, headers=headers, json=json)
    print("Subscription call result: %s" % subscribe_data.text)
    print(subscribe_data.status_code)