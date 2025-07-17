from dataiku.runnables import Runnable
from dataiku.customrecipe import get_recipe_config

import os
import importlib
import pandas as pd

def run_modules(client, instance_name, dt):
    directory = dss_object.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(".py") or f == "__init__.py":
                continue
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            spec = importlib.util.spec_from_file_location(module_name, fp)
            results, data = [False, None]
            try:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'main'):
                    results, data = module.main(client)
            except Exception as e:
                results, data = [False, None]
                print(f"Error importing or running ({path}) {module_name}: {e}")


class MyRunnable(Runnable):
    def __init__(self, project_key, config, plugin_config):
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config # sage_project_key | sage_project_url | sage_project_api | sage_worker_key
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        a = []
        for api_config in self.plugin_config["api_configs"]:
            hashKey = api_configs[0]
            worker_url = api_configs[1]
            worker_api = api_configs[2]
            print(api_confg)
            
        return " | ".join(a)
    
    
    
    
    
    
    
    