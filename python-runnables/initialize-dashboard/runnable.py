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
        
        source_path = None
        path_install = f"{root_path}/plugins/installed/sage/streamlit"
        path_dev = f"{root_path}/plugins/dev/sage/streamlit"

        if os.path.isdir(path_install):
            source_path = path_install
        elif os.path.isdir(path_dev):
            source_path = path_dev
        else:
            raise Exception("CANNOT FIND PLUGIN")
                
        return source_path
                
        try:
            shutil.copytree("./streamlit", destination_directory)
            print(f"Directory '{source_directory}' and its contents copied to '{destination_directory}' successfully.")
        except FileExistsError:
            print(f"Error: Destination directory '{destination_directory}' already exists. Please choose a non-existent directory.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return os.getcwd()