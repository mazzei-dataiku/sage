from dataiku.runnables import Runnable

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
        # get partitioned folder
        local_client = build_local_client() # dss_funcs
        project_handle = local_client.get_project(project_key="SAGE_DASHBOARD") # self.sage_project_key
        folder = get_folder("SAGE_DASHBOARD", project_handle, "partitioned_data") # dss_folder, self.sage_project_key
        
        # list partitions and turn into a df
        partitions = folder.list_partitions()
        folder_df = pd.DataFrame(partitions, columns=["partitions"])
        cols = ["instance_name", "category", "module", "dt"]
        folder_df[cols] = folder_df["partitions"].str.split("|", expand=True)