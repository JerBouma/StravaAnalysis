import time
from tqdm import tqdm
from .data_collection import (initialize_client, collect_general_data, collect_streams_data)
from .data_export import (export_general_data, export_streams_data)
import os


def data_aggregator(username, password, client_id, client_secret, chrome_driver_path=None, overwrite=False):
    """
    Description
    ----
    Collects all data from your Strava account and returns it in two variables:
        - General Data contains all general statistics including average heartrate
            pace, distance and more.
        - Streams Data contains specific statistics per activity including distance,
            heart rate, velocity, altitude and more.

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
    overwrite (boolean)
        Whether you wish to overwrite already created json files. Default is False.

    Output
    ----
    general_data (DataFrame)
        A collection of all the general data for each activity.
    streams_data (dictionary)
        A collection of all the streams data for each activity.
    """

    if not chrome_driver_path:
        client = initialize_client(username, password, client_id, client_secret)
    else:
        client = initialize_client(username, password, client_id, client_secret, chrome_driver_path)

    general_data = collect_general_data(client)

    streams_data = {}
    for activity_id in tqdm(general_data['map']):
        id = activity_id['id'][1:]

        if not overwrite:
            try:
                if str(id + '.json') in os.listdir("Streams Data"):
                    continue
            except FileNotFoundError:
                os.mkdir("Streams Data")
        try:
            streams_data[id] = collect_streams_data(client, id)
        except AttributeError:
            continue
        except RuntimeError:
            print("Maximum callbacks reached (600).. waiting 15 minutes.")
            for seconds in tqdm(range(901), position=0, leave=True):
                time.sleep(1)
            print("Ready! Collecting data..")
            streams_data[id] = collect_streams_data(client, id)

    return general_data, streams_data


def data_exporter(general_data, streams_data):
    """
    Description
    ----
    Exports General Data to one json file and exports the Stream Data to a json
    file for each activity. It does so by creating two folders:
        - General Data
        - Streams Data
    If you only have streams_data for one activity it creates a file
    named "streams_data.json"

    Input
    ----
    general_data (DataFrame)
        Data obtained from the collect_general_data() function.
    streams_data (dictionary)
        Data obtained from either data_aggregator() or collect_streams_data() depending
        on how many activities you wish to export.

    Output
    ----
    A series of json files stored in the folders "General Data" and "Streams Data".
    """
    export_general_data(general_data)

    if "time" in streams_data.keys():
        export_streams_data(streams_data, json_name="streams_data.json")
    else:
        for id in tqdm(streams_data.keys()):
            try:
                export_streams_data(streams_data[id], json_name=str(id + ".json"))
            except AttributeError:
                continue
