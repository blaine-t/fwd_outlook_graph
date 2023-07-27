import json

import requests

def format_recipient(recipient):
    return {
        'EmailAddress': {
            'Address': recipient
        }
    }

def send_email(access_token, to_recipients):
    # Calling graph using the access token
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    json = {
        'Message': {
            'Subject': "TEST EMAIL",
            'Body': {
                'ContentType': 'Text',
                'Content': "TEST BODY"
            },
            'ToRecipients': [
            ]
        }
        }
    for recipient in to_recipients:
        json['Message']['ToRecipients'].append(format_recipient(recipient))
    graph_data = requests.post(url, headers=headers, json=json)
    print("Graph API call result: %s" % graph_data.text)