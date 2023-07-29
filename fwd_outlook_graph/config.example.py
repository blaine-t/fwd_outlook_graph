# ================
# fwd_outlook_graph Config
# ================


# ----------------
# Azure Settings
# ----------------

# If you are using a multi-tenant app then the authority can be common. If it is single tenant you will use your tenant ID instead of common
AUTHORITY = "https://login.microsoftonline.com/common"
# Listed as "Application (client) ID in the Azure App Registration Overview"
CLIENT_ID = "Application-Client-ID-On-Azure"
# Username can be used if you only want to allow a specific user to login. I would recommend leaving it on none and then looking at the bin for what the username is before setting it
USERNAME = None
# Update the file path if you want the cache file in a different location
CACHE_FILE_PATH = "token_cache.bin"
# Scopes if they differ from default. The required scopes are Mail.Read and Mail.Send. If these are not the default then you can declare them here otherwise use .default
SCOPES = ["https://graph.microsoft.com/.default"]
# SCOPES = ["https://graph.microsoft.com/Mail.Read", "https://graph.microsoft.com/Mail.Send"]


# ----------------
# Subscription Settings
# ----------------

# The webhook URL you will send to the Graph notification service. This needs to be the same endpoint listed in @app.route("/sub", methods=["POST"]) including the sub. NO ENDING SLASH
SUBSCRIPTION_URL = "https://example.com/sub"
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
# If you would not like to use the catch all feature then set it to an empty string and the program will use TO_RECIPIENTS.
CATCH_ALL = ".outlook@example.com"
