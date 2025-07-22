from sage.src import dss_funcs
from sage.src import dss_init

import pandas as pd

from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)
        self.sage_project_url = plugin_config.get("sage_project_url", None)
        self.sage_project_api = plugin_config.get("sage_project_api", None)
        self.sage_worker_key  = plugin_config.get("sage_worker_key", None)
        self.ignore_certs     = plugin_config.get("ignore_certs", False)
        self.update_github    = plugin_config.get("update_github", False)
        self.repo = "https://github.com/mazzei-dataiku/sage.git"
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        results = []
        for api_config in self.plugin_config["api_configs"]:
            # Create a remote client
            worker_url = api_config["worker_url"]
            worker_api = api_config["worker_api"]
            remote_client = dss_funcs.build_remote_client(worker_url, worker_api, self.ignore_certs)
            
            # Install/Update Plugin if not found
            cont = True
            if self.sage_project_url != worker_url:
                import logging
                logging.error(self.sage_project_url, worker_url)
                try:
                    dss_init.install_plugin(self, remote_client)
                    results.append([worker_url, "Plugin Configured", True, None])
                except Exception as e:
                    results.append([worker_url, "Plugin Configured", False, e])
                    cont = False
            continue
        return
            
            # Create the Sage Worker Project
            if cont:
                try:
                    project_handle = dss_init.create_worker(remote_client, self.sage_worker_key)
                    results.append([worker_url, "Sage Worker Created", True, None])
                except Exception as e:
                    results.append([worker_url, "Sage Worker Created", False, e])
                    cont = False

            # Create the DSS Commit Table
            if cont:
                try:
                    dss_init.get_dss_commits(project_handle)
                    results.append([worker_url, "Load DSS Commits Table", True, None])
                except Exception as e:
                    cont = False
                    results.append([worker_url, "Load DSS Commits Table", False, e])
            
            # Create the Phone Home Scenarios
            if cont:
                try:
                    dss_init.create_scenarios(project_handle, "WORKER")
                    results.append([worker_url, "Update Scenarios", True, None])
                except Exception as e:
                    cont = False
                    results.append([worker_url, "Update Scenarios", False, e])
        
        # return results
        if results:
            df = pd.DataFrame(results, columns=["worker_url", "step", "results", "message"])
            html = df.to_html()
            return html      