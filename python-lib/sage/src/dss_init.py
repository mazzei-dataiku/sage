
t = """
[default]
trigger = '{"type": "temporal", "name": "Time-based", "delay": 5, "active": true, "params": {"repeatFrequency": 1, "frequency": "Daily", "startingFrom": "2025-07-16", "daysOfWeek": ["Wednesday"], "monthlyRunOn": "ON_THE_DAY", "minute": 0, "hour": 1, "timezone": "Canada/Eastern"}}'
step = '{"type": "runnable", "name": "run_macro", "enabled": true, "alwaysShowComment": false, "runConditionType": "RUN_IF_STATUS_MATCH", "runConditionStatuses": ["SUCCESS", "WARNING"], "runConditionExpression": "", "resetScenarioStatus": false, "delayBetweenRetries": 10, "maxRetriesOnFail": 0, "params": {"runnableType": "REPLACE_MACRO_HERE",   "config": {}, "adminConfig": {}, "proceedOnFailure": false}}'

[data_gather_instance]
macro = "pyrunnable_sage_data-gather-instance"

[data_gather_project]
macro = "pyrunnable_sage_data-gather-project"

[data_gather_audit]
macro = "pyrunnable_sage_data-gather-audit"

[data_gather_diskspace]
macro = "pyrunnable_sage_data-gather-diskspace"

[data_gather_filesystem]
macro = "pyrunnable_sage_data-gather-filesystem"
"""


def create_worker(client):
    if "SAGE_WORKER" not in client.list_project_keys():
        project_handle = client.create_project(project_key="SAGE_WORKER", name="SAGE WORKER", owner="admin")
    else:
        project_handle = client.get_project(project_key="SAGE_WORKER")
    return project_handle


def get_dss_commits(project_handle):
    dataset = project_handle.get_dataset("dss_commits")
    if not dataset.exists():
        dataset = project_handle.create_dataset(
            dataset_name = "dss_commits",
            type = "StatsDB",
            params = {
                'view': 'COMMITS',
                'orderByDate': False,
                'clusterTasks': {},
                'commits': {},
                'jobs': {},
                'scenarioRuns': {},
                'flowActions': {}
            }
        )
        schema = {
            "columns": [
                {"name": "project_key", "type": "string"},
                {"name": "commit_id", "type": "string"},
                {"name": "author", "type": "string"},
                {"name": "timestamp", "type": "bigint"},
                {"name": "added_files", "type": "int"},
                {"name": "added_lines", "type": "int"},
                {"name": "removed_files", "type": "int"},
                {"name": "removed_lines", "type": "int"},
                {"name": "changed_files", "type": "int"},
            ],
            "userModified": True,
        }
        r = dataset.set_schema(schema=schema)
    return


def create_scenarios(project_handle):
    macros = tomllib.loads(t)
    for key in macros:
        # skip default
        if key == "default":
            continue
        
        # rebase and setup macro in step
        trigger = json.loads(macros["default"]["trigger"])
        step = json.loads(macros["default"]["step"])
        step["params"]["runnableType"] = macros[key]["macro"]

        # create or connect to scenario
        try:
            scenario_handle = project_handle.get_scenario(scenario_id=key)
            settings = scenario_handle.get_settings()
        except:
            scenario_handle = project_handle.create_scenario(scenario_name=key, type="step_based")
            settings = scenario_handle.get_settings()
            
        # Trigger
        del settings.raw_triggers[:]
        settings.raw_triggers.append(trigger)
        
        # Steps
        del settings.raw_steps[:]
        settings.raw_steps.append(step)
        
        # Save
        settings.active = True
        settings.save()
    return