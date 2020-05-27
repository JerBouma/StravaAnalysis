from stravalib.client import Client
from selenium import webdriver
import pyderman
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os


def initialize_client(username, password, client_id, client_secret):
    """
    Description
    ----
    Initializes the client from Stravalib (https://github.com/hozn/stravalib) by using
    Selenium. This does the following:
        - Opens up a custom browser (chromedriver.exe)
        - Browses over to the authorization url
        - Enters your log-in details you provided (username and password) and logs in
        - When log-in is succesful, grabs the url and closes the browser.

    Within this url is a "token" that is used to activate your session. This makes it so that data
    can be collected.

    Note: this function requests your username and password. Note that this is merely used
    to obtain the required token to access your Strava data. Therefore, always keep this
    information private.

    Input
    ----
    username (string)
        Your Strava username which you use to log-in to Strava.
    password (string)
        Your Strava password which you use to log-in to Strava.
    client_id (string or integer)
        Your API ID which you can obtain by creating a Strava API.
    client_secret (string)
        Your API Secret which you can obtain by creating a Strava API.

    Output
    ----
    client (object)
        Creates a client that can be used to collect athlete data from your account.
    """

    if not os.path.exists('lib'):
        print("You do not currently have the required Chromedriver from Selenium. "
              "Do you wish to automatically download the driver?")
        input("Press ENTER to Continue.")
        pyderman.install(pyderman.chrome)

    client = Client()

    authorize_url = client.authorization_url(client_id=client_id,
                                             redirect_uri='http://localhost/authorized')

    driver = webdriver.Chrome("lib//" + os.listdir('lib')[0])
    driver.get(authorize_url)

    login_id = driver.find_element_by_name("email")
    login_id.send_keys(username)

    password_id = driver.find_element_by_name("password")
    password_id.send_keys(password)

    button = driver.find_element_by_id('login-button')
    button.click()

    WebDriverWait(driver, 15).until(EC.url_changes(driver.current_url))

    code = driver.current_url[40:80]
    driver.quit()

    client.exchange_code_for_token(
        client_id=client_id,
        client_secret=client_secret,
        code=code)

    return client


def collect_general_data(client, mile=1.609344):
    """
    Description
    ----
    Collects all data from your Strava account and returns it in the variable "General Data"
    which contains all general statistics including average heartrate pace, distance and more.

    This function also calculates pace, distance and speed in both km and miles.

    Input
    ----
    client (object)
        The client object obtained from the initialize_client() function.
    mile (float)
        Used to calculate the pace, distance and speed in miles. Is set on an
        exact value by default.

    Output
    ----
    general_data (dataframe)
        A collection of all the general data for each activity.
    """
    data = []
    for activity in client.get_activities():
        data_dict = activity.to_dict()
        data.append(data_dict)

    df = pd.DataFrame(data)
    df['date'] = df['start_date_local'].str[0:10]
    df = df.drop('start_date_local', axis=1)
    df = df.set_index('date')

    average_speed = []
    max_speed = []

    for average in df['average_speed']:
        try:
            average_speed.append(int(1000 / (average * 60)) * 100 +
                                 int(1000 / (average * 60) % 1 * 60))
        except ZeroDivisionError:
            average_speed.append(0)

    for max in df['max_speed']:
        try:
            max_speed.append(int(1000 / (max * 60)) * 100 +
                             int(1000 / (max * 60) % 1 * 60))
        except ZeroDivisionError:
            max_speed.append(0)

    # Calculate Pace
    df['average_pace_km'] = average_speed
    df['max_pace_km'] = max_speed
    df['average_pace_mile'] = df['average_pace_km'] / mile
    df['max_pace_mile'] = df['max_pace_km'] / mile

    # Distance
    df['distance_km'] = df['distance'] / 1000
    df['distance_mile'] = df['distance_km'] / mile
    df = df.drop('distance', axis=1)

    # Calculate Speed
    df['average_speed_km'] = df['average_speed'] * 3.6
    df['max_speed_km'] = df['max_speed'] * 3.6
    df['average_speed_mile'] = df['average_speed_km'] / mile
    df['max_speed_mile'] = df['max_speed_km'] / mile

    # Clean up NaNs
    general_data = df.fillna(0)

    return general_data


def collect_streams_data(client, activity_id,  types="All"):
    """
    Description
    ----
    Collects all streams data from your Strava activity and returns it in the variable "Streams Data"
    which contains specific statistics per activity including distance, heart rate, velocity,
    altitude and more.

    Input
    ----
    client (object)
        The client object obtained from the initialize_client() function.
    activity_id (float or string)
        The activity_id which can be obtained by clicking on any of your activities and
        copying the digits after "activities/".
    types (string)
        Gives the option to select a subset of the data, for example only heartrate data.
        By default this option is set to "All" which means it includes all the available
        type.

    Output
    ----
    streams_data (dictionary)
        A collection of all the streams data for the activity.
    """
    if types is "All":
        types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth',
                 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']

    raw_data = client.get_activity_streams(activity_id, types=types)

    streams_data = {}
    for key in raw_data.keys():
        streams_data[key] = raw_data[key].data

    return streams_data

client = initialize_client("jer.bouma@gmail.com", "u@b9Fon#CBgnl@Y50O", "36132", "00fafa27165459ae7035cbead81956e192a0bc30")