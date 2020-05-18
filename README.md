## Initial Setup
These two steps you only have to do *once*. After setting this up, you can simply start collecting Strava data with
ease. These steps are designed to be very user-friendly meaning that even without a programming background you
should be able to set this up.

### Create your own Strava API
1. Go to https://www.strava.com/settings/api and create an API.
    - Enter application name, category and authorisation. The authorisation should be *localhost*
    which makes it a local app for just you. 
2. Press Submit
3. Copy and save the following:
    - Client ID
    - Client Secret
    
Note that client secret should be kept to yourself. Do not share this code. For detailed info on the application
please see [the official documentation by Strava](https://developers.strava.com/docs/getting-started/).

### Create your own Google Sheets API
1. Go to https://console.developers.google.com/
2. Click "Create a new project" and enter any name (i.e. "Strava Dashboard")
3. Click "Enable APIs and Services" and search for "Google Sheets API". Select the first result and press "Enable".
4. Look or another API ("Google Drive API"), Select the first result (which has a Google Drive logo) and press "Enable"
5. Click on "Create Credentials"
    - **Which API are you using?** Select "Google Drive API"
    - **Where will you be calling the API from?** Select "Web server (e.g. node.js, Tomcat)"
    - **What data will you be accessing?** Select "Application data"
    - **Are you planning to use this API with App Engine or Compute Engine?** Select "No, I'm not using them."
6. Click on "What credentials do I need?"
    - Enter account name (can be anything) and select the role of Editor (Project > Editor)
    - Select JSON as Key Type
9. Press "Continue", rename the downloaded file to **client_secret.json** and store it at an appropriate location
(for example inside the application's folder)

Keep the contents of the file to yourself just like the client secret obtained from the
Strava API. For a complete guide, including images, please check [this blogpost](
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html).

## Collect Data
1. Open the application (or run the function *data_collection* from within Python)
2. Enter the following in the application:
    - Strava Username (your email) & Password
    - Client ID & Client Secret (which you have gathered above)
3. Press "Collect Data". It will open a custom Chrome Browser which uses your info to log-in to Strava and collect
the access code. Then it will paste all data in the corresponding Google Sheet.

**Note:** the application *does not* store your log-in credentials in any way. It merely uses these credentials to 
be able to collect data from Strava. The source code is available in this repository if you have any doubts. 
