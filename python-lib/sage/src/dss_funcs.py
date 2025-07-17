import os


def collect_modules(dss_objs):
    d = {}
    directory = dss_objs.__path__[0]
    for root, _, files in os.walk(directory):
        for f in files:
            if not f.endswith(".py") or f != "__init__.py":
                continue
            print(f)
            module_name = f[:-3]
            path = root.replace(directory, "")
            fp = os.path.join(root, f)
            if module_name in d.keys():
                d[module_name].append([path, fp])
            else:
                d[module_name] = [[path,fp]]
    return d