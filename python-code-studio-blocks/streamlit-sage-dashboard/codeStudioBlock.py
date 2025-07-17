import os, json, re, logging
from dataiku.code_studio import CodeStudioBlock

from block_utils import LibLocationPathReplacer, generate_python_codenv

from distutils.version import LooseVersion

# starting file       __PROJECT_LIB_VERSIONED__/python/sage/streamlit/app.py
# settings folder     __PROJECT_LIB_VERSIONED__/python/sage/streamlit

class MyCodeStudioBlock(CodeStudioBlock):
    def __init__(self, config, plugin_config):
        self.config = config
        self.plugin_config = plugin_config
        
    _ENTRYPOINT_FILE = "streamlit-entrypoint.sh"
    
    def _get_entrypoint_path(self):
        entrypoint_path = "/opt/dataiku"
        if entrypoint_path.endswith("/") or not entrypoint_path.endswith(".sh"):
            entrypoint_path = os.path.join(entrypoint_path, self._ENTRYPOINT_FILE)
        return entrypoint_path
    
    def _get_port(self):
        return 8181
        
    def build_spec(self, spec, env):
        dockerfile = spec.get("dockerfile", "")
        dockerfile = dockerfile + "\n\n# this was added by a block\n"
        return {"dockerfile":dockerfile}

    def build_launch(self, spec, env):
        return result
