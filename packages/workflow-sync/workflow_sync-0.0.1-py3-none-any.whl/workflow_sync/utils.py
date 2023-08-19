""" Utility functions.  """
import json

import requests
from databricks.sdk.runtime import dbutils  # type: ignore


def create_job(job_file: str) -> int:
    """ Create a job. """
    databricks_url = dbutils.notebook.entry_point.getDbutils().notebook()\
        .getContext().apiUrl().getOrElse(None)
    my_token = dbutils.notebook.entry_point.getDbutils().notebook()\
        .getContext().apiToken().getOrElse(None)

    header = {'Authorization': f'Bearer {my_token}'}
    endpoint = '/api/2.1/jobs/create'
    with open(job_file, encoding="utf-8") as in_file:
        payload = json.dumps(json.load(in_file))
        resp = requests.post(databricks_url + endpoint, data=payload,
                         headers=header, timeout=0.5)
        return int(resp.json().get("job_id"))

def run_job(job_id: int) -> int:
    """ Run a job. """
    databricks_url = dbutils.notebook.entry_point.getDbutils().notebook()\
        .getContext().apiUrl().getOrElse(None)
    my_token = dbutils.notebook.entry_point.getDbutils().notebook()\
        .getContext().apiToken().getOrElse(None)

    header = {'Authorization': f'Bearer {my_token}'}
    endpoint = '/api/2.1/jobs/run-now'
    payload = f'{{"job_id": {job_id}}}'
    resp = requests.post(databricks_url + endpoint, data=payload,
                         headers=header, timeout=0.5)
    return int(resp.json().get("run_id"))

def create_pipeline(job_file: str) -> None:
    """ Create a pipeline. """
    databricks_url = dbutils.notebook.entry_point.getDbutils().notebook()\
        .getContext().apiUrl().getOrElse(None)
    my_token = dbutils.notebook.entry_point.getDbutils().notebook()\
        .getContext().apiToken().getOrElse(None)

    header = {'Authorization': f'Bearer {my_token}'}
    endpoint = '/api/2.0/pipelines'
    with open(job_file, encoding="utf-8") as in_file:
        payload = json.dumps(json.load(in_file))
        resp = requests.post(databricks_url + endpoint, data=payload,
                         headers=header, timeout=0.5)
        print(resp.json())
    #return int(resp.json().get("pipeline_id"))
  