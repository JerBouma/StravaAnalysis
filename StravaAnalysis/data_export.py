import json


def export_general_data(general_data, general_data_name="general_data.json",
                        activities_data_name="activities_list.json", include_activities_list=True):
    """
    Description
    ----
    Exports General Data to one json file. It does so by creating the folder "General Data".
    Furthermore, it also adds an activities list by default to be used to be used to obtain activity ids.

    Input
    ----
    general_data (dataframe)
        Data obtained from the collect_general_data() function.
    general_data_name (string)
        The name of the json file created for the general data. By default this is set to
        "general_data.json"
    activities_data_name (string)
        The name of the json file created for the activities data. By default this is set to
        "activities_list.json"
    include_activities_list (boolean)
        A switch that allows you to turn off the creation of the activities list. Default is True.

    Output
    ----
    One or two json files stored in the folder "General Data".
    """
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
    """
    Description
    ----
    Exports Streams Data to a json file per activity. It does so by creating the folder "Streams Data".

    Input
    ----
    streams_data (dictionary)
        Data obtained from the collect_general_data() function. If it has keys other than the types
        listed in collect_streams_data() it assumes you are supplying multiple activites.
    json_name (string)
        The name of the json file when only one activity is given as input. Default is
        set to "streams_data.json"

    Output
    ----
    One or more json files stored in the folder "Streams Data".
    """
    try:
        os.mkdir("Streams Data")
    except FileExistsError:
        None

    with open(("Streams Data/" + str(json_name)), 'w') as file:
        json_string = json.dumps(streams_data, indent=4, sort_keys=True)
        file.write(json_string)