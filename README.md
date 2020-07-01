## StravaAnalysis
With limitations to Strava's free version, it becomes increasingly difficult to properly analyse your data. Next to
that, being able to fully "own" your data can be very valuable. This package makes that possible.

The goal of this package is to obtain all of your sports data from Strava so you are able to perform your own
personal analysis. With the amount of data you should be able to (visually) compare any activity and calculate any
metric you might require. Therefore, you do not have to rely on 3rd party software or Strava. As you can have a
variety goals, the collection of data via Strava's API can prove to be of help to translate these goals to numbers
and see actual progression over time between activities (that might not even be linked to each other via Strava).

![](Examples/StravaAnalysis.png)

## Data Collected
General Data refers to all data obtained for each activity. This package returns a DataFrame that gives all these
metrics per activity.

| General Data Variables | Description |
| -----------------------| ----------- |
| achievement_count | The amount of achievements obtained during the specific workout. |
| athlete | General information about the Athlete if available. |
| athlete_count | The amount of athletes who contributed to the workout. |
| average_cadence | Average cadence of the workout. |
| average_heartrate | Average heartrate of the workout. |
| average_pace_km | Average pace (km) listed as "542" meaning 5:42 per km. | 
| average_pace_mile | Average pace (mile) listed as "730" meaning 7:30 per mile. |  
| average_speed_km | Average speed (km) of the workout in km/h. |
| average_speed_mile | Average speed (km) of the workout in miles/h. |
| average_temp | Average tempo of the workout if available. |
| average_watts | Average watts of the workout if available. |
| best_efforts | Best efforts recorded during the workout. |
| calories | Amount of calories burned if applicable. |
| comment_count | Amount of comments on the Strava activity. |
| commute | Whether the activity is listed as a commute. |
| description | Whether the activity includes a description. |
| device_name | Whether the activity includes a device name. |
| device_watts | Whether the device returns watts. |
| distance_km | The distance in kilometers. |
| distance_mile | The distance in miles. |
| elapsed_time | The total time of the run. |
| elev_high | The highest elevation. |
| elev_low | The lowest elevation. | 
| embed_token | Whether there is an embed token given out. |
| end_latlng | Last latitude and longitude.  |
| external_id | The id, usually contains the name of the device you uploaded on. |
| flagged | Whether your activity is flagged for specific reasons. |
| from_accepted_tag | Whether you accepted to be included in a specific activity. |
| gear | Whether you used specific gear. |
| gear_id | The id of the gear. |
| has_heartrate | Tracks whether you monitor heart rate during the activity. |
| has_kudoed | Tracks if you obtained kudos. |
| highlighted_kudosers | Tracks if you highlighted kudo'ers. |
| instagram_primary_photo | In case put on Instagram, which photo was selected. |
| kilojoules | The kilojoules burned if applicable. |
| kudos_count | The amount of kudos received. |
| laps | The amount of laps you have done. |
| location_city | The location of the city your are in during the workout. |
| location_country |The country you are in during the workout. |
| location_state | The state you are in during the workout. |
| manual | Whether the activity is manually submitted. |
| map | The map which you can recreate with this data. |
| max_heartrate | If your max heartrate is reached. |
| max_pace_km | Max pace in kilometer where "430" means 4:30. |
| max_pace_mile | Max pace in miles where "530" means 5:30. |
| max_speed_km | Max speed in kilometer. |
| max_speed_mile | Max speed in miles. |
| max_watts | Max watts is applicable. |
| moving_time | The time you moved which differs from elapsed time. |
| name | The name of the activity. |
| partner_brand_tag | Whether you have a Brand attached to your activity. |
| partner_logo_url | Brand logo. |
| photo_count | Amount of photos added. |
| photos | Whether you added photos or not. |
| pr_count | The amount of Personal Records. |
| private | Whether the activity is private or not. |
| segment_efforts | Whether you have new segment efforts. |
| segment_leaderboard_opt_out | Whether you opted out of the segment leaderboards. |
| splits_metric | Metric Splits if applicable.
| splits_standard |Standard splits if applicable.
| start_date | The exact starting date.
| start_latitude | The start latitude.
| start_latlng | The start latitude and longitude. | 
| start_longitude | The start longitude. |
| suffer_score | The suffer score if applicable. | 
| timezone | The timezone you are in. |
| total_elevation_gain | The total elevation gained. |
| total_photo_count | The total amount of photos. | 
| trainer | Whether you used a training program. |
| type | The activity type (i.e. Run, Ride, Swim). |
| upload_id | The id included when uploaded. |
| utc_offset | UTC Offset to calculate time. |
| weighted_average_watts | Weighted value of the average watts. |
| workout_type | Listed as a number. For example Ride = 10. |

Streams data refers to data obtained per timestamp for an activity. Thus it contains a long lists depicting for
example your pace at a specific time window. With this data you can, among other things, recreate the graph displayed
on the Activity overview on Strava.

| Streams Data Variables | Description |
| -----------------------| ----------- |
| altitude | The altitude over time. |
| cadence | The cadence over time. |
| distance | The distance in meters over time. |
| distance_km | The distance in kilometers over time. |
| distance_mile | The distance in miles over time. |
| grade_smooth | The grade smooth applied over time. | 
| heartrate | The heart rate over time. |
| latlng | The latitude and altitude over time. |
| moving | Whether you are moving or not. |
| pace_km | The pace in km over time where "540" refers to 5:40. |
| pace_mile | The pace in miles over time where "740" refers to 7:40. |
| speed_km | The speed in kilometers over time. |
| speed_mile | The speed in miles over time. |
| time | The actual time in seconds. |
| velocity_smooth | Smoothing for velocity over time. |


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