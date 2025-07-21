import dataiku
import pandas as pd
import json
import warnings


def get_folder(folder_name):
    folder = dataiku.Folder(
        lookup = folder_name,
        project_key = dataiku.default_project_key(),
        ignore_flow = True
        )
    try:
        folder.get_id()
    except:
        folder = create_folder(folder_name)
    return folder


def read_folder_input(folder_name, path, data_type="DF"):
    folder = get_folder(folder_name)
    if data_type == "DF":
        with folder.get_download_stream(path) as reader:
            data = pd.read_csv(reader)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")  # Ignore all warnings within this block
                data = function_with_warning(data)
    elif data_type == "JSON":
        with folder.get_download_stream(path) as reader:
            data = json.loads(reader.data)
    return data


def function_with_warning(df):
    for c in df.columns:
        if df[c].dtype == "object":
            temp_col = pd.to_datetime(df[c],  errors='coerce')
            if temp_col.notna().all():
                df[c] = temp_col
    return df