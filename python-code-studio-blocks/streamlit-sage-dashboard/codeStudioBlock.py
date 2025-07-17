import os, json, re, logging
from dataiku.code_studio import CodeStudioBlock

from block_utils import LibLocationPathReplacer, generate_python_codenv

from distutils.version import LooseVersion

class MyCodeStudioBlock(CodeStudioBlock):
    def __init__(self, config, plugin_config):
        self.config = config
        self.plugin_config = plugin_config
        
    _ENTRYPOINT_FILE = "streamlit-entrypoint.sh"
        
    def build_spec(self, spec, env):
        dockerfile = spec.get("dockerfile", "")
        dockerfile = dockerfile + "\n\n# this was added by a block\n"
        return {"dockerfile":dockerfile}

    def build_launch(self, spec, env):
        return result
