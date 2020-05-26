import time
from data_collection import (initialize_client, collect_general_data, collect_streams_data)
from data_export import (export_general_data, export_streams_data)
from tqdm import tqdm


def data_aggregator(username, password, client_id, client_secret):
    client = initialize_client(username, password, client_id, client_secret)

    general_data = collect_general_data(client)

    streams_data = {}
    for activity_id in tqdm(general_data['map']):
        id = activity_id['id'][1:]

        try:
            streams_data[id] = collect_streams_data(client, id)
        except Exception as e:
            print("Maximum callbacks reached (600).. waiting 15 minutes.")
            for seconds in tqdm(range(901), position=0, leave=True):
                time.sleep(1)
            print("Ready! Collecting data..")
            streams_data[id] = collect_streams_data(client, id)

    return general_data, streams_data


def data_exporter(general_data, streams_data):
    export_general_data(general_data)

    for id in tqdm(streams_data.keys()):
        try:
            export_streams_data(streams_data[id], json_name=str(id + ".json"))
        except AttributeError:
            continue
