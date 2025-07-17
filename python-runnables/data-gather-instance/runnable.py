from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config # sage_project_key | sage_project_url | sage_project_api | sage_worker_key
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        a = []
        #for k in self.plugin_config.keys():
        for k in self.config.keys():
            a.append(k)
        return " | ".join(a)