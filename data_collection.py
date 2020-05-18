from stravalib.client import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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


client = initialize_client("jer.bouma@gmail.com", "u@b9Fon#CBgnl@Y50O",
                           36132, "00fafa27165459ae7035cbead81956e192a0bc30")


def collect_general_strava_data(client, columns=None):
    if not columns:
        columns = ['name', 'description', 'type', 'distance', 'moving_time',
                   'elapsed_time', 'average_speed', 'max_speed', 'average_heartrate',
                   'max_heartrate', 'start_date_local']

    data = []
    for activity in client.get_activities():
        data_dict = activity.to_dict()
        data.append([data_dict.get(x) for x in columns])

    df = pd.DataFrame(data, columns=columns)
    df['date'] = df['start_date_local'].str[0:10]
    df = df.drop('start_date_local', axis=1)
    df = df[['date'] + columns[:-1]]

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

    mile = 1.609344

    # Calculate Pace
    df['average_pace_km'] = average_speed
    df['max_pace_km'] = max_speed
    df['average_pace_mile'] = df['average_pace_km'] / mile
    df['max_pace_mile'] = df['max_pace_km'] / mile

    # Distance
    df['distance'] = df['distance'] / 1000

    # Calculate Speed
    df['average_speed_km'] = df['average_speed'] * 3.6
    df['max_speed_km'] = df['max_speed'] * 3.6
    df['average_speed_mile'] = df['average_speed_km'] / mile
    df['max_speed_mile'] = df['max_speed_km'] / mile

    # Clean up NaNs
    df = df.fillna(0)

    return df


# data = collect_strava_data(client)


def initialize_spreadsheet(credentials_file, google_sheet_name, sheet_name='Data'):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(credentials)

    sheet = client.open(google_sheet_name)

    try:
        sheet.add_worksheet(sheet_name, rows=1000,
                            cols=26)
    except Exception as e:
        None

    return sheet.worksheet(sheet_name)


def send_data_to_spreadsheet(spreadsheet, data):
    columns = [data.columns.values.tolist()]
    values = data.values.tolist()

    spreadsheet.update(columns + values)


# sheet = initialize_spreadsheet("client_secret.json", "Strava Dashboard")
#
# send_data_to_spreadsheet(sheet, data)








# client.access_token = token_response['access_token']
# client.refresh_token = token_response['refresh_token']
# client.token_expires_at = token_response['expires_at']