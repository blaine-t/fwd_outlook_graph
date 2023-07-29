import sys

import msal_extensions

from config import CACHE_FILE_PATH

def build_persistence():
    """Build a suitable persistence instance based your current OS"""
    if sys.platform.startswith('win'):
        return msal_extensions.FilePersistenceWithDataProtection(CACHE_FILE_PATH)
    if sys.platform.startswith('darwin'):
        return msal_extensions.KeychainPersistence(CACHE_FILE_PATH, "FOG", "FOG")
    return msal_extensions.FilePersistence(CACHE_FILE_PATH)

# Export cache to be usable in other parts of script
cache = msal_extensions.PersistedTokenCache(build_persistence())
