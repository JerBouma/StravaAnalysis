import json
import os


def export_general_data(general_data, general_data_name="general_data.json", activities_list=None,
                        activities_data_name="activities_list.json"):
    """
    Description
    ----
    Exports General Data to one json file. It does so by creating the folder "General Data" and placing the
    json file in it.

    Furthermore, it also adds an activities list by default to be used to be used to obtain activity ids.
    This is separated from the collect_general_data because it is only relevant

    Input
    ----
    general_data (DataFrame)
        Data obtained from the collect_general_data() function.
    general_data_name (string)
        The name of the json file created for the general data.
        By default this is set to "general_data.json"
    activities_list (Dictionary)
        Contains the activities_list created by collect_general_data.
        By default this variable is set to None which means it is not exported.
    activities_data_name (string)
        Contains the name you wish to give to the activities list json file.
        Default is set to "activities_list.json"

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

    if activities_list:
        with open(("General Data/" + str(activities_data_name)), 'w') as file:
            json_string = json.dumps(data, indent=4, sort_keys=True)
            file.write(json_string)


def export_streams_data(streams_data, json_name="streams_data.json"):
    """
    Description
    ----
    Exports Streams Data to a json file per activity. It does so by creating the folder "Streams Data" and placing
    all json files in this folder.

    Input
    ----
    streams_data (dictionary)
        Data obtained from the collect_general_data() function. If it has keys other than the types
        listed in collect_streams_data() it assumes you are supplying multiple activities.
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
