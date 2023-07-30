import datetime

from auth import get_access_token
from config import CATCH_ALL, TO_RECIPIENTS


def get_headers():
    """Returns an authorization header with an access token to make requests with"""
    return {'Authorization': f"Bearer {get_access_token()}"}


def get_time_str():
    """Gets the expiry time string for new and resubscribing subscriptions"""
    # Add 4230 minutes to the current time to enable the longest subscription expiry GRAPH allows
    # TODO: Make robust
    time = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(minutes=4230)
    return str(time).replace(" ", "T").replace("+00:00", "0Z")


def format_recipient(recipient):
    """Formats a recipient in Graph JSON format"""
    return {
        'emailAddress': {
            'address': recipient
        }
    }


def handle_to_recipients():
    """Handles to_recipients for traditional formatting and return proper json format"""
    return_list = []
    for recipient in TO_RECIPIENTS:
        return_list.append(format_recipient(recipient))
    return return_list


def handle_catch_all(message):
    """ Return the original sender plus the catch all suffix in proper json format"""
    return [format_recipient(f"{str(message['sender']['emailAddress']['address']).split('@')[0]}{CATCH_ALL}")]


def handle_attachments(attachments):
    """Organizes received message attachments into json format to send them outbound"""
    return_list = []
    for attachment in attachments['value']:
        return_list.append({
            '@odata.type': attachment['@odata.type'],
            'name': attachment['name'],
            'contentType': attachment['contentType'],
            'contentBytes': attachment['contentBytes']
        })
    return return_list
