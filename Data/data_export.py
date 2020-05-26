import json
import os


def export_general_data(general_data, general_data_name="general_data.json",
                        activities_data_name="activities_list.json", include_activities_list=True):
    try:
        os.mkdir("General Data")
    except FileExistsError:
        None

    with open(("General Data/" + str(general_data_name)), 'w') as file:
        json_string = json.dumps(general_data.to_dict(), indent=4, sort_keys=True)
        file.write(json_string)

    if include_activities_list:
        data = {}

        for index, row in general_data.iterrows():
            data[index + " - " + row['name']] = row['map']['id'][1:]

        with open(("General Data/" + str(activities_data_name)), 'w') as file:
            json_string = json.dumps(data, indent=4, sort_keys=True)
            file.write(json_string)


def export_streams_data(streams_data, json_name="streams_data.json"):
    data = {}

    for key in streams_data.keys():
        data[key] = streams_data[key].data

    try:
        os.mkdir("Streams Data")
    except FileExistsError:
        None

    with open(("Streams Data/" + str(json_name)), 'w') as file:
        json_string = json.dumps(data, indent=4, sort_keys=True)
        file.write(json_string)