import dataiku
import os
import importlib
import re
import pandas as pd
import tomllib


def collect_modules(dss_objs):
    d = {}
    directory = dss_objs.__path__[0]
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


def collect_display_data(dss_objs):
    display_data = []
    modules = collect_modules(dss_objs)
    for key in modules.keys():
        r_type = key.split(" ")
        r_type = r_type[0].lower()
        display_data.append(key)
    return modules, display_data