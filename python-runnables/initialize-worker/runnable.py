from sage.src import dss_funcs

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
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        results = []
        for api_config in self.plugin_config["api_configs"]:
            # Create a remote client
            worker_url = api_config["worker_url"]
            worker_api = api_config["worker_api"]
            remote_client = dss_funcs.build_remote_client(worker_url, worker_api)
            
            # Create the Sage Worker Project
            cont = True
            try:
                project_handle = create_worker(remote_client, self.sage_worker_key)
            except:
                cont = False

            # Create the DSS Commits Table
            if cont:
                try:
                    get_dss_commits(project_handle)
                except:
                    cont = False
            
            # Create the Phone Home Scenarios
            if cont:
                try:
                    create_scenarios(project_handle)
                except:
                    cont = False
        
            
        return "123"       