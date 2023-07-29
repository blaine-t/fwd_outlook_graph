import datetime

from auth import get_access_token
from config import CATCH_ALL, TO_RECIPIENTS

def get_headers():
    return {'Authorization': f'Bearer {get_access_token()}'}

def get_time_str():
    # Add 4230 minutes to the current time to enable the longest subscription expiry GRAPH allows
    time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = 4230)
    return str(time).replace(" ", "T").replace("+00:00", "0Z")

def format_recipient(recipient):
    return {
        'emailAddress': {
            'address': recipient
        }
    }

def handle_to_recipients(json):
    for recipient in TO_RECIPIENTS:
        json['ToRecipients'].append(format_recipient(recipient))
    return json

def handle_catch_all(json, message):
    # Add the original sender plus the catch all suffix to the toRecipients
    json["message"]["toRecipients"].append(format_recipient(f"{str(message['sender']['emailAddress']['address']).split('@')[0]}{CATCH_ALL}"))

def handle_attachments(json, attachments):
    for attachment in attachments["value"]:
        json["message"]["attachments"].append({
            "@odata.type": attachment["@odata.type"],
            "name": attachment["name"],
            "contentType": attachment["contentType"],
            "contentBytes": attachment["contentBytes"]
        })
    return json