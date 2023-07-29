import requests

from config import CLIENT_STATE, SUBSCRIPTION_URL
from util import get_headers, get_time_str

def subscribe():
    """Subscribe to notification when new email is found in users Outlook Inbox"""
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    json = {
        'changeType': "created",
        'notificationUrl': SUBSCRIPTION_URL,
        'lifecycleNotificationUrl': SUBSCRIPTION_URL,
        'resource': "me/mailFolders('Inbox')/messages",
        'expirationDateTime': get_time_str(),
        'clientState': CLIENT_STATE
    }

    response = requests.post(url, headers=get_headers(), json=json)
    
    if response.status_code == 201:
        print(f"New subscription ID: {response.json()['id']}")
    else:
        print(f"[{response.status_code}] Subscription call result: {response.text}")

def resubscribe(subscription_id):
    """Resubscribe to notification"""
    url = f'https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}'
    json = {
        'expirationDateTime': get_time_str()
    }

    response = requests.patch(url, headers=get_headers(), json=json)
    
    if response.status_code == 200:
        print(f"Resubscribed ID: {response.json()['id']}")
    else:
        print(f"[{response.status_code}] Resubscription call result: {response.text}")

def unsubscribe(subscription_id):
    """Unsubscribe from subscription"""
    url = f'https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}'

    response = requests.delete(url, headers=get_headers())

    if response.status_code == 204:
        print(f"Successfully unsubscribed: {subscription_id}")
    else:
        print(f"[{response.status_code}] Unsubscription call result: {response.text}")

def list_subscriptions():
    """List all current subscriptions"""
    url = f'https://graph.microsoft.com/v1.0/subscriptions'
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        print("Listed IDs:")
        for sub in response.json()['value']:
            print(sub['id'])
    else:
        print(f"[{response.status_code}] List call result: {response.text}")