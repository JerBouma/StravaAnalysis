from stravalib.client import Client
from selenium import webdriver
import pyderman
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import os


def initialize_client(username, password, client_id, client_secret, chrome_driver_path=None):
    """
    Description
    ----
    Initializes the client from Stravalib (https://github.com/hozn/stravalib) by using
    Selenium. This does the following:
        - Opens up a custom browser (Selenium)
        - Browses over to the authorization url
        - Enters your log-in details you provided (username and password) and logs in
        - When log-in is successful, grabs the url and closes the browser.

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
    chrome_driver_path (string)
        Add your own Chrome Driver path if you already have the .exe
        file required for Selenium.

    Output
    ----
    client (object)
        Creates a client that can be used to collect athlete data from your account.
    """
    if not os.path.exists('lib') and not chrome_driver_path:
        print("You do not currently have the required Chrome Driver from Selenium. "
              "Do you wish to automatically download the driver?")
        input("Press ENTER to Continue.")
        pyderman.install(pyderman.chrome)

    if not chrome_driver_path:
        driver = webdriver.Chrome("lib//" + os.listdir('lib')[0])
    else:
        driver = webdriver.Chrome(chrome_driver_path)

    client = Client()
    authorize_url = client.authorization_url(client_id=client_id,
                                             redirect_uri='http://localhost/authorized')
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


def collect_general_data(client, mile=1.609344, include_activities_list=False):
    """
    Description
    ----
    Collects all data from your Strava account and returns it in the variable "general_data"
    which contains all general statistics including average heart rate, pace, distance and more.
    This function also calculates pace, distance and speed in both km and miles.

    It also has the option to display an activities list by setting include_activities_list to True.

    Input
    ----
    client (object)
        The client object obtained from the initialize_client() function.
    mile (float)
        Used to calculate the pace, distance and speed in miles.
        Default is set on an exact value by default.
    include_activities_list (boolean)
        A boolean that creates an activities list when set on True.
        Default is set on False.

    Output
    ----
    general_data (DataFrame)
        A collection of the general data for each activity.

    activities_list (Dictionary)
        A collection of activities with as keys the Time + Name and as value
        the activity id. Is only returned when include_activities_list is True.
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

    for maximum in df['max_speed']:
        try:
            max_speed.append(int(1000 / (maximum * 60)) * 100 +
                             int(1000 / (maximum * 60) % 1 * 60))
        except ZeroDivisionError:
            max_speed.append(0)

    df['distance_km'] = df['distance'] / 1000
    df['distance_mile'] = df['distance_km'] / mile
    df = df.drop('distance', axis=1)

    df['average_speed_km'] = df['average_speed'] * 3.6
    df['max_speed_km'] = df['max_speed'] * 3.6
    df['average_speed_mile'] = df['average_speed_km'] / mile
    df['max_speed_mile'] = df['max_speed_km'] / mile

    df['average_pace_km'] = average_speed
    df['max_pace_km'] = max_speed
    df['average_pace_mile'] = (df['average_pace_km'] * mile).astype(int)
    df['max_pace_mile'] = (df['max_pace_km'] * mile).astype(int)

    general_data = df.fillna(0)

    if include_activities_list:
        activities_list = {}

        for index, row in general_data.iterrows():
            activities_list[index + " - " + row['name']] = row['map']['id'][1:]

        return general_data, activities_list

    return general_data


def collect_streams_data(client, activity_id, types="All", mile=1.609344):
    """
    Description
    ----
    Collects all streams data from your Strava activity and returns it in the variable "streams_data"
    which contains specific statistics per activity including distance, heart rate, velocity,
    altitude and more. Furthermore, it also calculates distance, pace and speed (in km and miles).

    Input
    ----
    client (object)
        The client object obtained from the initialize_client() function.
    activity_id (float or string)
        The activity_id which can be obtained by clicking on any of your activities and
        copying the digits after "activities/".
    types (string)
        Gives the option to select a subset of the data, for example only heart rate data.
        By default this option is set to "All" which means it includes all the available
        types. These are 'time', 'latlng', 'distance', 'altitude', 'velocity_smooth',
        heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth'.
    mile (float)
        An accurate measurement of the definition of 1 mile in kilometers.

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

    time_in_minutes = pd.Series(streams_data['time']) / 60

    try:
        streams_data['distance_km'] = pd.Series(streams_data['distance']) / 1000
        streams_data['distance_mile'] = streams_data['distance_km'] / mile

        streams_data['speed_km'] = (streams_data['distance_km'] / (time_in_minutes / 60)).fillna(method='backfill')
        streams_data['speed_mile'] = streams_data['speed_km'] / mile

        pace_int = time_in_minutes / pd.Series(streams_data['distance_km'])
        pace_int = pace_int.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        pace_remaining = (time_in_minutes / pd.Series(streams_data['distance_km']) - pace_int.astype(int)) * 60
        pace_remaining = pace_remaining.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')

        streams_data['pace_km'] = pace_int.astype(int) * 100 + pace_remaining.astype(int)
        streams_data['pace_mile'] = (streams_data['pace_km'] * mile).astype(int)
    except (KeyError, RuntimeWarning):
        None

    for key in streams_data.keys():
        streams_data[key] = list(streams_data[key])

    return streams_data
