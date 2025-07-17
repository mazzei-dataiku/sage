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
            if not f.endswith(".py") or f != "__init__.py":
                continue
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            if d.get(module_name):
                d[module_name].append([path, fp])
            else:
                d[module_name] = [[path,fp]]
    return d