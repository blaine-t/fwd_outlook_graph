# Azure Setup

This doc will explain how to setup the Azure App to use with FOG

## Step by step

1. Go to the [Azure Portal](https://portal.azure.com/#home)
2. Go to [App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)
3. Create a New Registration
4. Use any name that you would like. It has no effect on the script
5. You can pick any of the account types but I recommend the first Single Tenant option. If you want to use the app across multiple ADs you can choose a Multitenant or Multitenant and personal option if you also have a personal account. If you have multiple personal accounts you could choose the personal only option.
6. Leave the redirect URI blank as it is not used in this script.
7. Now go to the Authentication tab
8. Enable Allow public client flows and save as our app uses Device Code Flow
9. Then go to the API permissions tab
10. Click Add a permission
11. Then click through Microsoft Graph > Delegated Permissions
12. Now search for and add the following permissions:
    1. offline_access
    2. Mail.Read
    3. Mail.Send
13. Now you should have 4 Microsoft Graph Permissions since User.Read is in by default and required for the application to work
14. You now should be ready to go back to Overview and pull the `Application (client) ID` to put in your `config.py` and if you selected single tenant the `Directory (tenant) ID` as well
