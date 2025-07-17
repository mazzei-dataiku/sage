import dataiku
import os
import importlib
import re
import pandas as pd
import tomllib


def collect_display_data(load_modules):
    display_data = []
    modules = collect_modules(load_modules)
    for key in modules.keys():
        r_type = key.split(" ")
        r_type = r_type[0].lower()
        display_data.append(key)
    return modules, display_data