from sage.src import dss_funcs

import os
import pandas as pd
from datetime import date, timedelta

from dataiku.runnables import Runnable


# Run Macro
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

        os.chdir("/data/dataiku/dss_data/run/audit")
        directory_path = "./"
        logs = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        df = pd.DataFrame()
        for log in logs:
            tdf = pd.read_json(log, lines=True)
            if df.empty:
                df = tdf
            else:
                df = pd.concat([df, tdf], ignore_index=True)

        today = date.today()
        yesterday = today - timedelta(days=1)
        df = df[
            (df["timestamp"].dt.date < today)
            & (df["timestamp"].dt.date >= yesterday)
        ]