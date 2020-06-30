import json
import pandas as pd


def import_general_data(file="general_data.json", location="General Data\\", convert_to_df=True):
    """
    Description
    ----
    imports General Data from the chosen location. By default it looks into the folder created by the
    export_general_data function. It also transforms the data into a DataFrame if convert_to_df is True.

    Input
    ----
    file (string)
        The file the function has to read, by default this is "general_data.json".
    location (string)
        The location the function has to read, by default this is "General Data\\".
    convert_to_df (boolean)
        Whether it has to convert the data into a DataFrame, by default this is True.

    Output
    ----
    The data as either a Dictionary or as a DataFrame.
    """
    with open(location + file) as json_file:
        json_data = json.load(json_file)

        if convert_to_df:
            return pd.DataFrame(json_data)
        else:
            return json_data


def import_streams_data(file="streams_data.json", location="Streams Data\\", convert_to_df=True):
    """
    Description
    ----
    imports Streams Data from the chosen location. By default it looks into the folder created by the
    export_streams_data function. It also transforms the data into a DataFrame if convert_to_df is True.

    Input
    ----
    file (string)
        The file the function has to read, by default this is "streams_data.json".
    location (string)
        The location the function has to read, by default this is "Streams Data\\".
    convert_to_df (boolean)
        Whether it has to convert the data into a DataFrame, by default this is True.

    Output
    ----
    The data as either a Dictionary or as a DataFrame.
    """
    with open(location + file) as json_file:
        json_data = json.load(json_file)

        if convert_to_df:
            return pd.DataFrame(json_data)
        else:
            return json_data
