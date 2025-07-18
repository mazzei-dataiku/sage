from dataiku.runnables import Runnable
import logging

class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        # {'$$hashKey': 'object:6605', 'worker_url': 'https://mazzei-designer.fe-aws.dkucloud-dev.com', 'worker_api': 'dkuaps-MSleUwXxL2lCXEMQZVwiJNjMHfS0zIJ2'}
        for api_config in self.plugin_config["api_configs"]:
            logging.error(api_config)
            
        raise "123"       