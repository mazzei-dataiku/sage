import pandas as pd
import os

SAGE_WORKER = os.environ["SAGE_WORKER"]

def get_column_names_from_schema(schema):
    colNames = []
    for colData in schema:
        colNames.append(colData["name"])
    return colNames


def get_remote_dataframe(client, table_name):
    project_handle = client.get_project(project_key=SAGE_WORKER)
    dataset_handle = project_handle.get_dataset(table_name)
    columns = get_column_names_from_schema(dataset_handle.get_schema()["columns"])
    raw_data = dataset_handle.iter_rows()
    df = pd.DataFrame(raw_data, columns = columns)
    return df


def main(client):
    # Pull in DSS Commits table to see user activity better
    dss_commits_df = get_remote_dataframe(client, "dss_commits")

    # Data Users Base Info
    dss_users = client.list_users()
    dss_users_df = pd.DataFrame(dss_users)
    if "trialStatus" in dss_users_df.columns:
        jdf = pd.json_normalize(dss_users_df["trialStatus"]).add_prefix("trialStatus.")
        dss_users_df = pd.concat([dss_users_df, jdf], axis=1)
    
    # Dataiku Users Last Activity
    dss_user_activity = client.list_users_activity()
    user_activity = [[user.login, user.last_session_activity] for user in dss_user_activity]
    dss_user_activity_df = pd.DataFrame(user_activity, columns=["login", "last_session_activity"])

    # Merge users and session activity
    dss_users_df = dss_users_df.merge(dss_user_activity_df, on="login", how="left")

    # Get Commit Data max/min stamps
    grouped = dss_commits_df.groupby("author")
    data = []
    for author, grp in grouped:
        min_ts = pd.to_datetime(grp.timestamp.min(), unit="ms")
        max_ts = pd.to_datetime(grp.timestamp.max(), unit="ms")
        data.append([author, min_ts, max_ts])
    cols = ["login", "first_commit_date", "last_commit_date"]
    user_commits_df = pd.DataFrame(data, columns=cols)

    # Join the user table
    df = pd.merge(dss_users_df, user_commits_df, on="login", how="left")

    # Clean dates
    df["creationDate"] = pd.to_datetime(df["creationDate"], unit="ms", utc=True)
    for c in ["creationDate", "last_session_activity", "first_commit_date", "last_commit_date"]:
        df[c] = pd.to_datetime(df[c], utc=True)
        df[c] = df[c].fillna(pd.to_datetime("1970-01-01", utc=True))
        df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    # Return
    return df