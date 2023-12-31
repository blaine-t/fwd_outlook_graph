# ================
# fwd_outlook_graph Config
# ================

# ----------------
# Development Settings
# ----------------

# VERY IMPORTANT TO HAVE FALSE IF SERVER IS IN PRODUCTION TO AVOID MISUSE
# When enabled allows certain endpoints and admin panel to work for testing
DEVELOPMENT = False


# ----------------
# Proxy Settings
# ----------------

# If you are behind a proxy you need to comment None and uncomment the PROXY object
# You need to set the value of how many times the specific X-Forwarded header has been set
# For example if you are just behind NGINX then 1 on all values is sufficient
# But if you have Cloudflare and NGINX then you'll want 2 for FOR and PROTO
# Flask NGINX config: https://flask.palletsprojects.com/en/2.3.x/deploying/nginx/
# Flask Proxy config: https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
# Cloudflare config: https://developers.cloudflare.com/fundamentals/get-started/reference/http-request-headers/
PROXY = None
# PROXY = {
# 'FOR': 1,
# 'PROTO': 1,
# 'HOST': 1,
# 'PREFIX': 1
# }


# ----------------
# Auth Settings
# ----------------

# If you are using a multi-tenant app then the authority can be common. If it is single tenant you will use your tenant ID instead of common
AUTHORITY = "https://login.microsoftonline.com/common"
# Listed as "Application (client) ID in the Azure App Registration Overview"
CLIENT_ID = "Application-Client-ID-On-Azure"
# Username can be used if you only want to allow a specific user to login. I would recommend leaving it on none and then looking at the cache for the username before setting it
USERNAME = None
# The required scopes are Mail.Read and Mail.Send. If these are not the default then you can uncomment them otherwise use .default
SCOPES = ["https://graph.microsoft.com/.default"]
# SCOPES = ["https://graph.microsoft.com/Mail.Read", "https://graph.microsoft.com/Mail.Send"]


# ----------------
# Cache Settings
# ----------------

# Update the file path if you want the cache file in a different location
CACHE_FILE_PATH = "token_cache.bin"
# Allow fallback to plain text token cache if your system doesn't support encryption (Mine doesn't even after debugging so I have to use True to fallback)
FALLBACK_TO_PLAINTEXT = True


# ----------------
# Subscription Settings
# ----------------

# The webhook URL you will send to the Graph notification service. This needs to be the same endpoint listed in @app.route("/sub", methods=["POST"]) including the sub. MUST HAVE ENDING SLASH
SUBSCRIPTION_URL = "https://example.com/sub/"
# The secret that is used to confirm that the same application that asked for the notification gets it and that Microsoft is the one posting to /sub and not another actor
# DO NOT LEAVE THIS DEFAULT. Please use a random string of anything. It can be 1-128 characters. I recommend Bitwarden for generating a random string if you need a tool
CLIENT_STATE = "aRandom128CharacterStringThatIsUsedToVerifyThatTheRequestCameFromMicrosoftAndNotABadActorThatWantsToAttackYouIRecommendBitwarden"


# ----------------
# Forwarding Settings
# ----------------

# Transparent forward forwards the message by copying the content over to another message that way to the end user there isn't an apparent forward
# This is most similar to how inboxes usually do auto-forwarding when support so I recommend it being enabled
TRANSPARENT_FORWARD = True
# Only used when TRANSPARENT_FORWARD is True
# Decides whether to put the transparent forward outbound email in the send mailbox or not
ADD_TO_SEND = False
# The recipients that you would like to send the mail to. This can be set from 1 address to as many as you want. Used if CATCH_ALL is an empty string.
TO_RECIPIENTS = ["email@example.com", "email2@example.com"]
# If you would like to copy the username before the @ in the senders email and append that to a suffix for situations like a catch all inbox set that suffix here
# If you would not like to use the catch all feature then set it to an empty string and the script will use TO_RECIPIENTS.
CATCH_ALL = [".outlook@example.com", ".outlookOtherCatchAll@example.org"]
# If you would like to include the domain of the sender in the catch all append than you can toggle this to True. Most will want this on false.
CATCH_ALL_INCLUDE_DOMAIN = False
