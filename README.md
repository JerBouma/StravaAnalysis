## StravaAnalysis
With limitations to Strava's free version, it becomes increasingly difficult to properly analyse your data. Next to
that, being able to fully "own" your data can be very valuable. This package makes that possible.

The goal of this package is to obtain all of your sports data from Strava so you are able to perform your own
personal analysis. With the amount of data you should be able to (visually) compare any activity and calculate any
metric you might require. Therefore, you do not have to rely on 3rd party software or Strava. As you can have a
variety goals, the collection of data via Strava's API can prove to be of help to translate these goals to numbers
and see actual progression over time between activities (that might not even be linked to each other via Strava).

![](Examples/StravaAnalysis.png)

## Initial Setup
To get started you need to install the package via PyPi and obtain a Strava API (free). The steps below you only have
to do once. Afterwards, the API is linked to your account and you can start using this package.

### Install the package
1. `pip install StravaAnalysis`
    - Alternatively, download this repository
2. (within Python) `import StravaAnalysis as se`

### Create your own Strava API
1. Go to https://www.strava.com/settings/api and create an API.
    - Enter application name, category and authorisation. The authorisation should be *localhost*
    which makes it a local app for just you. 
2. Press Submit
3. Copy and save the following:
    - Client ID
    - Client Secret
    
Note that the client secret should be kept to yourself. Do not share this code with anyone otherwise you risk others
abusing your API requests limit. For detailed info on the application please see
[the official documentation by Strava](https://developers.strava.com/docs/getting-started/).

## Example
When running the `initilize_client` (or `data_aggregator`) function for the first time, it will ask if you wish to
download the latest Chrome Driver. This is required to obtain the authentication key used to collect your data. For
more info, have a look [here](https://chromedriver.chromium.org/getting-started). You can also provide your own
Chrome Driver file by adding the path to the parameter `chrome_driver_path`.

What the Chrome Driver does is open an automated Chrome Browser, go to the Strava link that your API creates, log-in
and obtain the authentication code. With this code, you gain access to your data.

**Note:** the package *does not* store your log-in credentials in any way. It merely uses these credentials to 
be able to collect data from Strava. The source code is available in the repository if you have any doubts.

**Collect all of your data and export it to json files**
```
import StravaAnalysis as se

USERNAME = <your Strava e-mail here>
PASSWORD = <your Strava password here>
CLIENT_ID = <your API Client ID here>
CLIENT_SECRET = <your API Client Secret here>

# Inititalize Client and Collect all General Data and Streams Data
general_data, streams_data = se.data_aggregator(USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET)

# Export all Data to JSON Files
se.data_exporter(general_data, streams_data)
```
**Collect general data and collect from a specific activity**
```
import StravaAnalysis as se

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

# Export Data
se.export_general_data(general_data)
se.export_streams_data(streams_data)
```
**Import general data and import a specific activity**
```
import StravaAnalysis as se

# Import General Data & Streams Data
se.import_general_data()
se.import_streams_data("554237255.json")
```

## Support
**No package is perfect.** Therefore, in case you wish to contribute I highly appreciate pull requests and/or creation
of issues. 