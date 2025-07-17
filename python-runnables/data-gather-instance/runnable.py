from dataiku.runnables import Runnable
from dataiku.customrecipe import get_recipe_config

import os
import importlib
import pandas as pd

#import sys
#sys.path.append('/path/to/your/library/directory')

from sage.src import dss_funcs
try:
    from sage.base_data import client_handle as dss_objs
except:
    dss_objs = False


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
            
        client = build_local_client(host, api_key)

        # Load the INSIGHTS information
        modules = dss_funcs.collect_modules(dss_objs)

        if modules:
            return modules
        return "FAILED"
    
    
    
    
    
    
    
    