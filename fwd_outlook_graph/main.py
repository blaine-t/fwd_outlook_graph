#!/usr/bin/env python3

"""
The configuration file (default config.json) would look like this:
{
    "authority": "https://login.microsoftonline.com/common",
    "client_id": "your_client_id",
}
    # You can find the other permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    # To restrict who can login to this app, you can find more Microsoft Graph API endpoints from Graph Explorer
    # https://developer.microsoft.com/en-us/graph/graph-explorer

You can then run this script:
    ./main.py
"""

from auth import get_access_token
from cache import get_cache
from config import load_config
from request import send_email

config_file_path = "config.json"  # Update the file path if the config file is in a different location
cache_file_path = "token_cache.bin" # Update the file path if the cache is in a different location

# Optional logging
# logging.basicConfig(level=logging.DEBUG)

def main():
    config = load_config(config_file_path)
    cache = get_cache(cache_file_path)
    access_token = get_access_token(cache, config)
    send_email(access_token, config['to_recipients'])


if __name__ == '__main__':
    main()