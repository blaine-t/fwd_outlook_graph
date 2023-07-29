import json
import logging
import sys

import msal

from config import CLIENT_ID, AUTHORITY
from cache import cache

def get_auth():
    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=AUTHORITY, token_cache=cache
        )

    # The pattern to acquire a token looks like this.
    result = None

    # Note: If your device-flow app does not have any interactive ability, you can
    # completely skip the following cache part. But here we demonstrate it anyway.
    # We now check the cache to see if we have some end users signed in before.
    accounts = app.get_accounts()
    if accounts:
        logging.info("Account(s) exists in cache, probably with token too. Let's try.")
        # Now let's try to find a token in cache for this account
        result = app.acquire_token_silent(["https://graph.microsoft.com/.default"], account=accounts[0])

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")

        flow = app.initiate_device_flow(scopes=["https://graph.microsoft.com/.default"])
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

        print(flow["message"])
        sys.stdout.flush()  # Some terminal needs this to ensure the message is shown

        result = app.acquire_token_by_device_flow(flow)
    
    return result

def get_access_token():
    result = get_auth()
    if "access_token" in result:
        return result['access_token']
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug
