import pandas as pd

def get_column_names_from_schema(schema):
    colNames = []
    for colData in schema:
        colNames.append(colData["name"])
    return colNames


def get_remote_dataframe(client, table_name):
    project_handle = client.get_project(project_key="SAGE_WORKER")
    dataset_handle = project_handle.get_dataset(table_name)
    columns = get_column_names_from_schema(dataset_handle.get_schema()["columns"])
    raw_data = dataset_handle.iter_rows()
    df = pd.DataFrame(raw_data, columns = columns)
    return df


def main(client):
    # Pull in DSS Commits table to see user activity better
    dss_commits_df = get_remote_dataframe(client, "dss_commits")
    
    # Pull commit information based off each user and project
    data = []
    for i,g in dss_commits_df.groupby(["author", "project_key"]):
        author = i[0]
        project_key = i[1]
        if "api:" in author:
            continue
        t = [
            author,
            project_key,
            g["project_key"].count(),
            g["timestamp"].min(),
            g["timestamp"].max(),
        ]
        data.append(t)
    df = pd.DataFrame(data, columns=["login", "projet_key", "num_commits", "first_commit", "last_commit"])
    

    # Return
    return df