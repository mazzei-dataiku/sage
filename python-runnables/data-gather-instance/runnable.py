from dataiku.runnables import Runnable
from dataiku.customrecipe import get_recipe_config

import os
import importlib
import pandas as pd

from sage.base_data import client_handle as dss_categories

#import sys
#sys.path.append('/path/to/your/library/directory')

def run_modules(client, instance_name):
    directory = dss_categories.__path__[0]
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
        self.plugin_config = plugin_config
        self.sage_project_key = plugin_config.get("sage_project_key", None)
        self.sage_project_url = plugin_config.get("sage_project_url", None)
        self.sage_project_api = plugin_config.get("sage_project_api", None)
        
    def get_progress_target(self):
        return None

    def run(self, progress_callback):
        
        return
    
    
    
    
    
    
    
    