# ---------- DATAIKU REMOTE FOLDERS ----------------------------
def write_remote_folder_output(self, client, path, df):
    projet_handle = client.get_project(project_key=self.sage_project_key)
    fid = None
    for f in projet_handle.list_managed_folders():
        if f["name"] == "partitioned_data":
            fid = f["id"]
            break
    if not fid:
        raise Exception()
    folder = projet_handle.get_managed_folder(odb_id=fid)
    r = folder.put_file(path, df.to_csv(index=None))
    return


# ---------- DATAIKU LOCAL FOLDERS -----------------------------
def get_folder(folder_name):
    import dataiku
    folder = dataiku.Folder(
        lookup = folder_name,
        project_key = dataiku.default_project_key(),
        ignore_flow = True
        )
    try:
        folder.get_id()
    except:
        folder = create_folder(folder_name)
    return folder


def create_folder(client, folder_name):
    client = dataiku.api_client()
    project = client.get_default_project()    
    # Create Folder
    folder_handle = project.create_managed_folder(
        name = folder_name,
        connection_name = "filesystem_folders"
    )
    if folder_name == "partitioned_data":
        settings = folder_handle.get_settings()
        settings.remove_partitioning()
        settings.add_discrete_partitioning_dimension("instance_name")
        settings.add_discrete_partitioning_dimension("category")
        settings.add_discrete_partitioning_dimension("module")
        settings.add_time_partitioning_dimension("date", period='DAY')
        settings.set_partitioning_file_pattern("%{instance_name}/%{category}/%{module}/%Y/%M/%D/.*")
        settings.save()
    # Return Folder object
    folder = dataiku.Folder(
        lookup = folder_name,
        ignore_flow = True,
        project_key = dataiku.default_project_key()
    )
    return folder