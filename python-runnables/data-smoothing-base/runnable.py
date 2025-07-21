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
        
        # get latest partition
        max_date = folder_df['dt'].max()
        write_local_folder_output( # dss_folder
            sage_project_key = "SAGE_DASHBOARD",
            project_handle = project_handle,
            folder_name = "base_data",
            path = f"/partition.csv",
            data_type = "DF",
            data = pd.DataFrame([max_date], columns=["latest_partition"])
        )
        filtered_df = folder_df[folder_df['dt'] == max_date]
        
        # Loop over the sets and gather
        groups = filtered_df.groupby(by=["category", "module"])
        for i, g in groups:
            category, module = i
            # loop over and build consolidated df
            df = pd.DataFrame()
            for partition in g["partitions"].tolist():
                paths = folder.list_paths_in_partition(partition=partition)
                for path in paths:
                    tdf = read_local_folder_input( # dss_folder
                        "SAGE_DASHBOARD", project_handle, "partitioned_data", path
                    )
                    if df.empty:
                        df = tdf
                    else:
                        df = pd.concat([df, tdf], ignore_index=True)
                # Write consolidated DF to folder
                write_local_folder_output( # dss_folder
                    sage_project_key = "SAGE_DASHBOARD",
                    project_handle = project_handle,
                    folder_name = "base_data",
                    path = f"/{category}/{module}.csv",
                    data_type = "DF",
                    data = df
                )
        
        return