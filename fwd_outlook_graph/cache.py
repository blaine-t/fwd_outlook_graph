import sys
import msal_extensions

def build_persistence(cache_file_path):
    """Build a suitable persistence instance based your current OS"""
    if sys.platform.startswith('win'):
        return msal_extensions.FilePersistenceWithDataProtection(cache_file_path)
    if sys.platform.startswith('darwin'):
        return msal_extensions.KeychainPersistence(cache_file_path, "FOG", "FOG")
    return msal_extensions.FilePersistence(cache_file_path)

def get_cache(cache_file_path):
    return msal_extensions.PersistedTokenCache(build_persistence(cache_file_path))