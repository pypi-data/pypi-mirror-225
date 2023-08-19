""" manage_jobs unit tests. """
import json
from pathlib import Path

from workflow_sync.manage_jobs import DeltaLiveTables

class TestDeltaLiveTables:
    """ DeltaLiveTable workflow unit tests.  """
    pipeline_json_file = str(Path(__file__).parent.joinpath("data", "dlt_example.json"))
    with open(pipeline_json_file, encoding="utf-8") as pipeline_json:
        pipeline = json.load(pipeline_json)
    delta_live_tables = DeltaLiveTables()

    def test_dlt_create_new_returns_not_none(self) -> None:
        """ Test create new workflow.  """
        pipeline_id = self.delta_live_tables.create(self.pipeline)
        assert pipeline_id is not None

    def test_dlt_create_existing_returns_none(self) -> None:
        """ Test create new workflow when it already exists.  """
        pipeline_id = self.delta_live_tables.create(self.pipeline)
        assert pipeline_id is None

    def test_get_valid_dlt_name_returns_not_none\
                    (self, name: str="feature_test_pipeline") -> None:
        """ Test get existing valid workflow.  """
        pipeline_id = self.delta_live_tables.get(name)
        assert pipeline_id is not None

    def test_get_invalid_dlt_name_returns_none\
                    (self, name: str="dummy") -> None:
        """ Test get invalid workflow.  """
        pipeline_id = self.delta_live_tables.get(name)
        assert pipeline_id is None

    def test_delete_valid_name(self, name: str="feature_test_pipeline")\
            -> None:
        """ Test delete pipeline. """
        pipeline = self.delta_live_tables.get(name)
        self.delta_live_tables.delete(pipeline.get("pipeline_id"))
        assert True
