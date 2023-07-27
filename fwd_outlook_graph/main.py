#!/usr/bin/env python3

"""
The configuration file (default config.json) would look like this:
{
    "authority": "https://login.microsoftonline.com/common",
    "client_id": "your_client_id",
    "scope": ["User.ReadBasic.All"],
    "endpoint": "https://graph.microsoft.com/v1.0/users"
}
    # You can find the other permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    # To restrict who can login to this app, you can find more Microsoft Graph API endpoints from Graph Explorer
    # https://developer.microsoft.com/en-us/graph/graph-explorer

You can then run this script:
    ./main.py
"""

import sys
import json
import logging

import requests
import msal
import msal_extensions

config_file_path = "config.json"  # Update the file path if the config file is in a different location
cache_file_path = "token_cache.bin" # Update the file path if the cache is in a different location

# Optional logging
# logging.basicConfig(level=logging.DEBUG)

def msal_persistence():
    """Build a suitable persistence instance based your current OS"""
    if sys.platform.startswith('win'):
        return msal_extensions.FilePersistenceWithDataProtection(cache_file_path)
    if sys.platform.startswith('darwin'):
        return msal_extensions.KeychainPersistence(cache_file_path, "my_service_name", "my_account_name")
    return msal_extensions.FilePersistence(cache_file_path)

persistence = msal_persistence()
cache = msal_extensions.PersistedTokenCache(persistence)

with open(config_file_path) as config_file:
    config = json.load(config_file)


def auth():
    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.PublicClientApplication(
        config["client_id"], authority=config["authority"], token_cache=cache
        )

    # The pattern to acquire a token looks like this.
    result = None

    # Note: If your device-flow app does not have any interactive ability, you can
    # completely skip the following cache part. But here we demonstrate it anyway.
    # We now check the cache to see if we have some end users signed in before.
    accounts = app.get_accounts()
    if accounts:
        logging.info("Account(s) exists in cache, probably with token too. Let's try.")
        print("Pick the account you want to use to proceed:")
        for a in accounts:
            print(a["username"])
        # Assuming the end user chose this one
        chosen = accounts[0]
        # Now let's try to find a token in cache for this account
        result = app.acquire_token_silent(config["scope"], account=chosen)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")

        flow = app.initiate_device_flow(scopes=config["scope"])
        if "user_code" not in flow:
            raise ValueError(
                "Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

        print(flow["message"])
        sys.stdout.flush()  # Some terminal needs this to ensure the message is shown

        # Ideally you should wait here, in order to save some unnecessary polling
        # input("Press Enter after signing in from another device to proceed, CTRL+C to abort.")

        result = app.acquire_token_by_device_flow(flow)  # By default it will block
            # You can follow this instruction to shorten the block time
            #    https://msal-python.readthedocs.io/en/latest/#msal.PublicClientApplication.acquire_token_by_device_flow
            # or you may even turn off the blocking behavior,
            # and then keep calling acquire_token_by_device_flow(flow) in your own customized loop.
    
    return result

result = auth()

if "access_token" in result:
    # Calling graph using the access token
    graph_data = requests.get(  # Use token to call downstream service
        config["endpoint"],
        headers={'Authorization': 'Bearer ' + result['access_token']},).json()
    print("Graph API call result: %s" % json.dumps(graph_data, indent=2))
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug