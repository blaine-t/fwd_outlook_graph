import requests

from config import CLIENT_STATE, SUBSCRIPTION_URL
from util import get_headers, get_time_str


def get_subscriptions():
    """Gets all current subscriptions"""
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()['value'], response.status_code
    else:
        error_string = f"[{response.status_code}] Get subscriptions result: {response.text}"
        return [{'id': error_string}], response.status_code


def get_user():
    """Gets all current subscriptions"""
    url = "https://graph.microsoft.com/v1.0/me"
    response = requests.get(url, headers=get_headers())
    user = None
    if response.status_code == 200:
        json = response.json()
        user = {
            'name': json['displayName'],
            'mail': json['mail']
        }
    else:
        print(
            f"[{response.status_code}] Get user result: {response.text}")
        user = {
            'name': f"[{response.status_code}] Get user error",
            'mail': response.text
        }
    return user

# Could implement DRY with this and init_subscriptions but abstracts the functions too much


def list_subscriptions():
    """List all current subscriptions"""
    subscriptions = []
    response = get_subscriptions()
    response_json = response[0]
    response_status = response[1]
    if response_status != 200:
        print(
            f"[{response_status}] Failed to list subscriptions. Result: {response_json}")
        return [], response_status
    for sub in response_json:
        subscriptions.append(sub['id'])
    return subscriptions, response_status


def init_subscriptions():
    """DESTRUCTIVE Initialize program so it can have a sole subscription DESTRUCTIVE"""
    # Remove all other subscriptions
    response = get_subscriptions()
    response_json = response[0]
    response_status = response[1]
    if response_status != 200:
        print(
            f"[{response_status}] Failed to initialize subscriptions. Result: {response_json}")
        return [], response_status
    for sub in response_json:
        unsubscribe(sub['id'])
    # Create a single new subscription
    subscribe()
    print("Initialized subscriptions")


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
        response_text = f"Successfully subscribed. ID: {response.json()['id']}"
    else:
        response_text = f"[{response.status_code}] Unsuccessfully subscribed. Result: {response.text}"
    print(response_text)
    return (response_text, response.status_code)


def resubscribe(subscription_id):
    """Resubscribe to notification"""
    url = f"https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}"
    json = {
        'expirationDateTime': get_time_str()
    }

    response = requests.patch(url, headers=get_headers(), json=json)

    if response.status_code == 200:
        response_text = f"Successfully resubscribed. ID: {subscription_id}"
    else:
        response_text = f"[{response.status_code}] Unsuccessfully resubscribed. Result: {response.text}"
    print(response_text)
    return (response_text, response.status_code)


def unsubscribe(subscription_id):
    """Unsubscribe from subscription"""
    url = f"https://graph.microsoft.com/v1.0/subscriptions/{subscription_id}"

    response = requests.delete(url, headers=get_headers())

    if response.status_code == 204:
        response_text = f"Successfully unsubscribed. ID: {subscription_id}"
        response_status = 200
    else:
        response_text = f"[{response.status_code}] Unsuccessfully unsubscribed. Result: {response.text}"
        response_status = response.status_code
    print(response_text)
    # Need to convert status because 204 is no content
    return (response_text, response_status)
