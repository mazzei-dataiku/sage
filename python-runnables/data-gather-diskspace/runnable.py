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
        cmd = "find . -maxdepth 3 -type d"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        directories = result.stdout.split("\n")
        directories.remove(".")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        