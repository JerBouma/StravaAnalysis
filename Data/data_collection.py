from stravalib.client import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def initialize_client(username, password, client_id, client_secret):
    client = Client()

    authorize_url = client.authorization_url(client_id=client_id,
                                             redirect_uri='http://localhost/authorized')

    driver = webdriver.Chrome("chromedriver.exe")
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
    df = df.fillna(0)

    return df


def collect_streams_data(client, activity_id,  types="All"):
    if types is "All":
        types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth',
                 'heartrate', 'cadence', 'watts', 'temp', 'moving', 'grade_smooth']

    data = client.get_activity_streams(activity_id, types=types)

    return data
