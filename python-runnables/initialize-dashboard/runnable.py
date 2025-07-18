from sage.src import dss_funcs
import os

from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config

    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Get local client and name
        local_client = dss_funcs.build_local_client()
        instance_name = dss_funcs.get_dss_name(local_client)
        
        # change directory and get audit logs
        root_path = local_client.get_instance_info().raw["dataDirPath"]
        try:
            path = f"{root_path}/plugins/installed/sage"
            os.chdir(path)
        except:
            try:
                path = f"{root_path}/plugins/installed/sage"
                os.chdir(path)
            except:
                raise Exception("CANNOT FIND PLUGIN")
        
        return os.getcwd()