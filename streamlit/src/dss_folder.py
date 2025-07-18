import dataiku
import pandas as pd
import json
import warnings





def write_folder_output(folder_name, path, data, data_type="DF"):
    folder = get_folder(folder_name)
    if data_type == "DF":
        with folder.get_writer(path) as w:
            w.write(data.to_csv(index=False).encode("utf-8"))
    elif data_type == "JSON":
        with folder.get_writer(path) as w:
            w.write(str.encode(json.dumps(data, indent=4)))


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


if __name__ == "__main__":
    main()