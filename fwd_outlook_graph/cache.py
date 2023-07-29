from msal_extensions import build_encrypted_persistence, FilePersistence, PersistedTokenCache

from config import CACHE_FILE_PATH, FALLBACK_TO_PLAINTEXT

def build_persistence():
    """Build a suitable persistence instance based your current OS"""
    try:
        # UNTESTED
        return build_encrypted_persistence(CACHE_FILE_PATH)
    except:
        if not FALLBACK_TO_PLAINTEXT:
            raise
        # Store persistance unencrypted if FALLBACK_TO_PLAINTEXT is allowed
        # TESTED with Debian 12 Python 3.11.2
        return FilePersistence(CACHE_FILE_PATH)

# Export cache to be usable in other parts of script
cache = PersistedTokenCache(build_persistence())
print("Type of persistence: {}".format(cache.__class__.__name__))
print("Is this persistence encrypted?", cache.is_encrypted)