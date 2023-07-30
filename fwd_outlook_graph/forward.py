import requests

from config import ADD_TO_SEND, CATCH_ALL, TRANSPARENT_FORWARD
from util import get_headers, handle_attachments, handle_catch_all, handle_to_recipients


def get_attachments(message_id):
    """Retrieve the list of attachments of a single message"""
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments'
    return requests.get(url, headers=get_headers()).json()


def get_message(message_id):
    """Retrieve a single message"""
    url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}'
    return requests.get(url, headers=get_headers()).json()


def transparent_forward_email(message_id):
    """Transparent forward a given message"""
    # Retrieve data from the message
    message = get_message(message_id)

    url = f'https://graph.microsoft.com/v1.0/me/sendMail'
    json = {
        "message": {
            "subject": message['subject'],
            "body": message['body'],
            "toRecipients": [],
            "attachments": []
        },
        "saveToSentItems": ADD_TO_SEND
    }

    # Handle attachments
    if message['hasAttachments']:
        attachments = get_attachments(message['id'])
        json = handle_attachments(json, attachments)

    # Handle forwards if TO_RECIPIENTS or CATCH_ALL
    if CATCH_ALL:
        json = handle_catch_all(json, get_message(message_id))
    else:
        json = handle_to_recipients(json)

    response = requests.post(url, headers=get_headers(), json=json)

    if response.status_code == 202:
        print(f"Successfully sent: {message['id']}")
    else:
        print(f"[{response.status_code}] Send call result: {response.text}")


def forward_email(message_id):
    """Forward normally or transparently based on config"""
    if TRANSPARENT_FORWARD:
        transparent_forward_email(message_id)
    else:
        # Normal Forwarding
        url = f'https://graph.microsoft.com/v1.0/me/messages/{message_id}/forward'
        json = {
            'Comment': "",
            'ToRecipients': [
            ]
        }

        # Handle forwards if TO_RECIPIENTS or CATCH_ALL
        if CATCH_ALL:
            json = handle_catch_all(json, get_message(message_id))
        else:
            json = handle_to_recipients(json)

        response = requests.post(url, headers=get_headers(), json=json)

        if response.status_code == 202:
            print(f"Successfully forwarded: {message_id}")
        else:
            print(f"[{response.status_code}] Forward call result: {response.text}")
