from sage.src import dss_funcs, dss_folder
import os
import shutil

from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)

    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # Get local client and name
        local_client = dss_funcs.build_local_client()
        instance_name = dss_funcs.get_dss_name(local_client)
        
        # Get plugin directory
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
            
        # Get Dashboard library directory
        project_path = f"{root_path}/config/projects/{self.sage_project_key}/lib/python"
        if not os.path.isdir(project_path):
            raise Exception("CANNOT FIND PROJECT or PROJECT LIBRARY")
        
        # Delete the current running version
        project_path = f"{root_path}/config/projects/{self.sage_project_key}/lib/python/sage"
        if os.path.exists(project_path) and os.path.isdir(project_path):
            try:
                shutil.rmtree(project_path)
            except OSError as e:
                raise Exception(f"Error deleting directory '{project_path}': {e}")

        # Copy the streamlit application
        try:
            shutil.copytree(source_path, project_path)
        except FileExistsError:
            raise Exception(f"Error: Destination directory '{destination_directory}' already exists. Please choose a non-existent directory.")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
            
        # temp file to reload library
        project_handle = local_client.get_project(self.sage_project_key)
        library = project_handle.get_library()
        file = library.add_file("python/sage/initialized.csv")
        file.delete()
        
        # Create the folders
        dss_folder.get_folder(self, project_handle, "partitioned_data")
        dss_folder.get_folder(self, project_handle, "base_data")
        
        
        return