import msal

from config import AUTHORITY, CLIENT_ID, SCOPES, USERNAME
from cache import cache

# Create a preferably long-lived app instance which maintains a token cache.
# NOTE: THIS IS DIFFERENT THAN THE FLASK APP
app = msal.PublicClientApplication(
    CLIENT_ID, authority=AUTHORITY, token_cache=cache
)


def get_access_token():
    """Use cache and device flow method as backup to retrieve the Bearer access_token to send with Graph API requests"""

    # Create a variable to store the result of auth flow
    result = None

    # Check the cache to see if some end users signed in before. Filter by username if provided
    accounts = app.get_accounts(username=USERNAME)

    # If there is a successful cache hit
    if accounts:
        # If there is more than one account warn the user
        if len(accounts) > 1:
            print("Found multiple accounts:")
            for account in accounts:
                print(account['username'])
            print(f"Using this account: {accounts[0]['username']}")

        # Try and use a cached token
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if not result:
        # If using a cached token failed or no accounts were found use device auth
        flow = app.initiate_device_flow(scopes=SCOPES)
        if 'user_code' not in flow:
            raise ValueError(
                f"Fail to create device flow. Err: {flow}")

        # Prints out the authentications message for the user to login with
        print(flow['message'])

        # Poll Microsoft servers to receive the access token
        result = app.acquire_token_by_device_flow(flow)

    # Handle extracting the access token from the result
    if 'access_token' in result:
        return result['access_token']
    else:
        print("Error when extracting access token:")
        print(result)
