

def create_worker(client):
    if "SAGE_WORKER" not in client.list_project_keys():
        project_handle = client.create_project(project_key="SAGE_WORKER", name="SAGE WORKER", owner="admin")
    else:
        project_handle = client.get_project(project_key="SAGE_WORKER")
    return project_handle