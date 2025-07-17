from dataiku.runnables import Runnable
from dataiku.customrecipe import get_recipe_config

try:
    from sage.base_data import client_handle as dss_objs
except:
    dss_objs = False
from sage.src import dss_funcs

import pandas as pd
from datetime import datetime

# Run Macro
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
        # Test if modules are found
        if not dss_objs:
            raise Exception("No categories or modules found")
        # Collect the modules
        modules = dss_funcs.collect_modules(dss_objs)
        # Run the modules
        results = dss_funcs.run_modules(self, dss_objs)

        if results:
            df = pd.DataFrame(results, columns=["path", "module_name", "step", "result", "message"])
            html = df.to_html()
            return html
        return "FAILED"
    
    
    
    
    
    
    
    