from dataiku.runnables import Runnable
from dataiku.customrecipe import get_recipe_config

import os
import importlib
import pandas as pd

try:
    from sage.base_data import client_handle as dss_objs
except:
    dss_objs = False
from sage.src import dss_funcs

#import sys
#sys.path.append('/path/to/your/library/directory')


def run_modules(client, instance_name):
        try:
            spec = importlib.util.spec_from_file_location(module_name, fp)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'main'):
                df = module.main(client)
                results.append([path, module_name, "load/run", True, None])
        except Exception as e:
            df = pd.DataFrame()
            results.append([path, module_name, "load/run", False, e])
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
        if not dss_objs:
            raise Exception("No categories or modules found")

        # Load the INSIGHTS information
        categories_modules = dss_funcs.collect_modules(dss_objs)

        return " | ".join(categories_modules.keys())
    
    
    
    
    
    
    
    