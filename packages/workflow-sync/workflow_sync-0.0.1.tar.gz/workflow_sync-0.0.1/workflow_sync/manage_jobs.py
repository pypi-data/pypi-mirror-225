""" Module for managing workflows which include jobs and Delta Live Table
pipeline jobs.  Pipeline names must be unique otherwise "RESOURCE_CONFLICT"
is returned in the error_code field along with a message.  However, this can
be overwritten by setting `allow_duplicate_names = true` in the request, but
we don't want to do this."""
import json
import os
import pathlib
from abc import ABC, abstractmethod
from typing import Optional, Any

import requests


class Workflow(ABC):
    """ Workflow abstract superclass from which DeltaLiveTables and Jobs
    classes can inherit from. """
    databricks_url = "https://dbc-c485f5e8-763f.cloud.databricks.com"
    header = {'Authorization': f'Bearer {os.getenv("TOKEN")}'}

    @abstractmethod
    def create(self, pipeline: dict[str, Any]) -> Optional[str]:
        """
        Create a new workflow.  Returns the id of the newly created workflow
        or None if it fails to be created.
        :param json_file:
        :return:
        """

    @abstractmethod
    def update(self, pipeline: dict[str, Any]) -> Any:
        """
        Update an existing workflow.
        :param pipeline:
        :return:
        """

    @abstractmethod
    def _get_all(self) -> Optional[dict[str, Any]]:
        """
        List all the existing workflows.
        :return:
        """

    @abstractmethod
    def get(self, pipeline_name: Optional[str]) -> Optional[dict[str, Any]]:
        """
        Get a workflow.
        :param pipeline_name:
        :return:
        """

    @abstractmethod
    def delete(self, pipeline_id: str) -> None:
        """
        Delete a workflow.
        :param pipeline_id:
        :return:
        """

    @abstractmethod
    def load_from_json(self) -> list[dict[str, Any]]:
        """
        Load all the existing workflows from the json files.
        :return:
        """

    @abstractmethod
    def refresh(self, pipelines: list[dict[str, Any]]) -> None:
        """
        Sync the databricks workflows with the json definitions.
        :param pipelines:
        :return:
        """

class DeltaLiveTables(Workflow):
    """ Utility class for managing Delta Live Table pipelines.  """
    def create(self, pipeline: dict[str, Any]) -> Optional[str]:
        endpoint = '/api/2.0/pipelines'
        payload = json.dumps(pipeline)
        resp = requests.post(Workflow.databricks_url + endpoint, data=payload,
                             headers=Workflow.header, timeout=0.5)
        if (pipeline_id:= resp.json().get("pipeline_id")):
            return str(pipeline_id)
        return None


    def update(self, pipeline: dict[str, Any]) -> Any:
        endpoint = '/api/2.0/pipelines/'
        resp = requests.put(Workflow.databricks_url + endpoint +
                            pipeline["id"], data=json.dumps(pipeline),
                            headers=Workflow.header, timeout=0.5)
        return resp.json().get("message")

    def _get_all(self) -> Optional[dict[str, Any]]:
        """ Return all delta live table pipelines.  Key is name.  """
        endpoint = '/api/2.0/pipelines/'
        resp = requests.get(Workflow.databricks_url + endpoint,
                            headers=Workflow.header, timeout=0.5)
        if pipelines:= resp.json()["statuses"]:
            return {pipeline["name"]: pipeline for pipeline in
                              pipelines}
        return None

    def get(self, pipeline_name: Optional[str]) -> Any:
        """ Checks to see whether a pipeline already exists with the same name
        and returns the pipeline id of the matching pipeline. We need to get
        the pipeline again using the API since the spec field isn't returned
        when called by ListPipelines.

        If pipeline_name isn't supplied then return all the pipelines.  """
        pipelines = self._get_all()
        if pipeline_name is None:
            return pipelines
        if pipelines and pipeline_name in pipelines:
            endpoint = '/api/2.0/pipelines/'
            if (pipeline:= pipelines.get(pipeline_name)) is not None:
                resp = requests.get(Workflow.databricks_url + endpoint
                                    + pipeline.get("pipeline_id"), headers=Workflow.header,
                                    timeout=0.5)
                return resp.json()
        return None

    def delete(self, pipeline_id: str) -> None:
        """
        Deletes a pipeline with the id pipeline_id.
        :param pipeline_id:
        :return:
        """
        endpoint = '/api/2.0/pipelines/'
        requests.delete(Workflow.databricks_url + endpoint + pipeline_id,
                        headers=Workflow.header, timeout=0.5)

    def load_from_json(self) -> list[dict[str, Any]]:
        """
        Load all the delta live table pipelines from json files.
        :return:
        """
        dlt_path = pathlib.Path(__file__).parent.parent.joinpath(*["workflows",
                                                                   "delta_live_tables"])
        dlt_pipelines = []
        for filepath in dlt_path.glob('**/*.json'):
            with open(filepath.absolute(), encoding="utf-8") as f_in:
                dlt_pipelines.append(json.load(f_in))
        return dlt_pipelines

    def refresh(self, pipelines: list[dict[str, Any]]) -> None:
        """ For each of the delta live table pipeline json files see if there
        is an existing job and if so update it.  If no job exists already, then
        create a new one.  """
        for pipeline in pipelines:
            if pipeline.get("id"):
                self.update(pipeline)
            else:
                self.create(pipeline)


def main() -> None:
    """ Main method called when running module directly. """
    delta_live_tables = DeltaLiveTables()
    dlt_pipelines = delta_live_tables.load_from_json()
    delta_live_tables.refresh(dlt_pipelines)

if __name__ == "__main__":
    main()
