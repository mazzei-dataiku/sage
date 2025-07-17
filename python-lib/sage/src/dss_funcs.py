import dataiku
import dataikuapi
import os
import re
import importlib
import pandas as pd

from sage.src import dss_folder


def build_local_client():
    client = dataiku.api_client()
    return client


def build_remote_client(host, api_key):
    client = dataikuapi.DSSClient(host, api_key)
    return client


def get_dss_name(client):
    instance_info = client.get_instance_info()
    instance_name = instance_info.node_name.lower()
    instance_name = re.sub(r'[^a-zA-Z0-9]', ' ', instance_name)
    instance_name = re.sub(r'\s+', '_', instance_name)
    return instance_name


def run_modules(self, dss_objs):
    results = []
    directory = dss_objs.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(".py") or f == "__init__.py":
                continue
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            try:
                spec = importlib.util.spec_from_file_location(module_name, fp)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'main'):
                    local_client = build_local_client()
                    df = module.main(local_client)
                    results.append([path, module_name, "load/run", True, None])
            except Exception as e:
                df = pd.DataFrame()
                results.append([path, module_name, "load/run", False, e])
            if df.empty:
                continue # nothing to write, skip
            instance_name = get_dss_name(local_client)
            if "instance_name" not in df.columns:
                df["instance_name"] = instance_name
            try:
                remote_client = build_remote_client(self.sage_project_url, self.sage_project_api)
                dt_year  = str(self.dt.year)
                dt_month = str(f'{self.dt.month:02d}')
                dt_day   = str(f'{self.dt.day:02d}')
                write_path = f"/{instance_name}/{path}/{module_name}/{dt_year}/{dt_month}/{dt_day}/data.csv"
                dss_folder.write_remote_folder_output(self, remote_client, write_path, df)
                results.append([path, module_name, "write/save", True, None])
            except Exception as e:
                results.append([path, module_name, "write/save", False, e])
    return results


def get_nested_value(data, keys):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    return current
















def collect_modules(dss_objs):
    modules = {}
    directory = dss_objs.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(".py") or f == "__init__.py":
                continue
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            l = [path, fp]
            if module_name in modules.keys():
                modules[module_name].append(l)
            else:
                modules[module_name] = []
                modules[module_name].append(l)
    return modules