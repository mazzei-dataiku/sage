from sage.src import dss_funcs

import os
import subprocess
import pandas as pd
from datetime import date, timedelta

from dataiku.runnables import Runnable

def get_size(d):
    try:
        result = subprocess.run(f"du -sc {d}", shell=True, capture_output=True, text=True, check=True)
        size = result.stdout.split("\t")[0]
        size = int(size)
    except:
        size = 0
    return size


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)
        self.sage_project_url = plugin_config.get("sage_project_url", None)
        self.sage_project_api = plugin_config.get("sage_project_api", None)
        self.dt = datetime.utcnow()
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Get local client and name
        local_client = build_local_client()
        instance_name = dss_funcs.get_dss_name(local_client)
        
        # change directory and get audit logs
        root_path = local_client.get_instance_info().raw["dataDirPath"]
        os.chdir(root_path)
        
        # Find directories maxdepth
        results = []
        cmd = "find . -maxdepth 3 -type d"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        directories = result.stdout.split("\n")
        directories.remove(".")
        
        # turn into a df
        df = pd.DataFrame(directories, columns=["directory"])
        
        # remove jupyter-run / .git -- permission issues with sudo stuff
        df = df[~df["directory"].str.contains("jupyter-run")]
        df = df[~df["directory"].str.contains(".git")]

        # Explode directory
        cols = ["dot", "level_1", "level_2", "level_3"]
        df[cols] = df["directory"].str.split("/",  expand=True)

        # remove columns
        del df["dot"]
        del df["directory"]
        
        # Get details on sizes - level_1
        df["level_1_size"] = 0
        for i,g in df.groupby(by=["level_1"]):
            d = "/".join(i)
            size = get_size(d)
            df.loc[df["level_1"] == i[0], "level_1_size"] = size
            
        # Filter size on a base number (1gb / adjustable)
        gb = 1000000 * self.config.get("min_disk_space", 1)
        df = df[df["level_1_size"] >= gb]

        # Get details on sizes - level_2
        df["level_2_size"] = 0
        for i,g in df.groupby(by=["level_1", "level_2"]):
            d = "/".join(i)
            size = get_size(d)
            df.loc[
                (df["level_1"] == i[0])
                & (df["level_2"] == i[1]), "level_2_size"] = size

        # Get details on sizes - level_3
        df["level_3_size"] = 0
        for i,g in df.groupby(by=["level_1", "level_2", "level_3"]):
            d = "/".join(i)
            size = get_size(d)
            df.loc[
                (df["level_1"] == i[0])
                & (df["level_2"] == i[1])
                & (df["level_3"] == i[2]), "level_3_size"] = size
            
        results.append([path, module_name, "read/parse", False, None])
        
        # loop topics and save data
        remote_client = build_remote_client(self.sage_project_url, self.sage_project_api)
        dt_year  = str(self.dt.year)
        dt_month = str(f'{self.dt.month:02d}')
        dt_day   = str(f'{self.dt.day:02d}')
        try:
            write_path = f"/{instance_name}/disk_space/diskspace/{dt_year}/{dt_month}/{dt_day}/data.csv"
            dss_folder.write_remote_folder_output(self, remote_client, write_path, df)
            results.append([path, module_name, "write/save", False, None])
        except Exception as e:
            results.append([path, module_name, "write/save", True, e])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["path", "module_name", "step", "result", "message"])
            html = df.to_html()
            return html
        raise Exception("FAILED TO RUN INSTANCE CHECKS")
        
        
        
        
        
        
        