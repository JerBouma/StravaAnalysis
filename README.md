## Initial Setup
To get started you need a Strava API. The steps below you only have to do <u>once</u>. Afterwards, the API is linked
to your account and you can start using this package.

### Create your own Strava API
1. Go to https://www.strava.com/settings/api and create an API.
    - Enter application name, category and authorisation. The authorisation should be *localhost*
    which makes it a local app for just you. 
2. Press Submit
3. Copy and save the following:
    - Client ID
    - Client Secret
    
Note that the client secret should be kept to yourself. Do not share this code. For detailed info on the application
please see [the official documentation by Strava](https://developers.strava.com/docs/getting-started/).

## Example
When running the the `initilize_client` (or `data_aggregator`) function for the first time, it will ask if you wish to download
the latest Chrome Driver. This is required to obtain the authentication key used to collect your data. For
more info, have a look [here](https://chromedriver.chromium.org/getting-started). You can also provide your own
Chrome Driver file by adding the path to the parameter `chrome_driver_path`.

**Note:** the package *does not* store your log-in credentials in any way. It merely uses these credentials to 
be able to collect data from Strava. The source code is available in this repository if you have any doubts.

**Collect all of your data and export it to .json files**
```
import StravaExporter as se

USERNAME = <your Strava e-mail here>
PASSWORD = <your Strava password here>
CLIENT_ID = <your API Client ID here>
CLIENT_SECRET = <your API Client Secret here>

# Inititalize Client and Collect all General Data and Streams Data
general_data, streams_data = se.data_aggregator(USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET)

# Export all Data to JSON Files
se.data_exporter(general_data, streams_data)
```
**Collect general data and/or collect from a specific activity**
```
import StravaExporter as se

USERNAME = <your Strava e-mail here>
PASSWORD = <your Strava password here>
CLIENT_ID = <your API Client ID here>
CLIENT_SECRET = <your API Client Secret here>

# Inititalize Client
client = se.initialize_client(USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET)

# Collect General Data
general_data = se.collect_general_data(client)

# Collect Streams Data
# Activity id is found by clicking on any activity in Strava and copying the code in the url
streams_data = se.collect_streams_data(client, "1234567890")

# Optional Export (uncomment to run)
# se.export_general_data(general_data)
# se.export_streams_data(streams_data)
```
