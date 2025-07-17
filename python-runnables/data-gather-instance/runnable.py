from dataiku.runnables import Runnable
from dataiku.customrecipe import get_recipe_config

import os
import importlib
import pandas as pd

try:
    from sage.base_data import client_handle as dss_categories
except:
    dss_categories = False

#import sys
#sys.path.append('/path/to/your/library/directory')

def collect_modules(module):
    d = {}
    directory = module.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                module_name = f[:-3]
                path = root.replace(directory, "")
                fp = os.path.join(root, f)
                delimiters = r'[-_]'
                words = re.split(delimiters, module_name)
                capitalized_words = [word.capitalize() for word in words]
                final_string = " ".join(capitalized_words)
                d[final_string] = [module_name, fp]
    return d


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
        if not dss_categories:
            raise Exception("No categories or modules found")

        # Load the INSIGHTS information
        modules, display_data = collect_display_data(dss_objects)

        return
    
    
    
    
    
    
    
    