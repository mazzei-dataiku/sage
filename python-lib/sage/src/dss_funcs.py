import dataiku
import dataikuapi
import os


def build_local_client():
    return client


def build_remote_client():
    return client


def get_dss_name(client):
    instance_info = client.get_instance_info()
    instance_name = instance_info.node_name.lower()
    instance_name = re.sub(r'[^a-zA-Z0-9]', ' ', instance_name)
    instance_name = re.sub(r'\s+', '_', instance_name)
    return instance_name


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