import os


def collect_modules(dss_objs):
    modules = {}
    directory = dss_objs.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(".py") or f != "__init__.py":
                continue
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            l = [path, fp]
            if module_name in d.keys():
                modules[module_name].append(l)
            else:
                modules[module_name] = []
                modules[module_name].append(l)
    return modules