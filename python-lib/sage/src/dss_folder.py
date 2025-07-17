import dataiku
import pandas as pd
import json
import warnings


# ---------- DATAIKU REMOTE FOLDERS ----------------------------
def write_remote_folder(self, client, df):
    projet_handle = client.get_project(project_key=self.sage_project_key)
    fid = None
    for f in projet_handle.list_managed_folders():
        if f["name"] == "partitioned_data":
            fid = f["id"]
            break
    if not fid:
        raise Exception()
    folder = projet_handle.get_managed_folder(odb_id=fid)
    r = folder.put_file("/testing_again.csv", df.to_csv(index=None))
    return