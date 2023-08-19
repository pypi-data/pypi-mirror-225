""" Step file for feature test. """
import json
import os
import shutil
import tempfile
from pathlib import Path

from behave import (step,  # type: ignore # pylint: disable=no-name-in-module
                    then, when)

from workflow_sync.manage_jobs import DeltaLiveTables


@step("there is a new delta live table pipeline to add")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    path = Path(__file__).parent.parent.parent.joinpath("workflows", "delta_live_tables")
    temp_file = tempfile.NamedTemporaryFile(mode='w+t', dir=str(path), suffix=".json", delete=False) # pylint: disable=consider-using-with
    # if a modified pipeline has been already added to the context then use this,
    # else use the unmodified (i.e. file version)
    try:
        if pipeline:= context.modified_pipeline:
            temp_file.writelines(json.dumps(pipeline))
    except AttributeError:
        from_file = str(Path(__file__).parent.parent.parent.joinpath("test", "data",
                                                                     "dlt_example.json"))
        shutil.copy2(from_file, temp_file.name)
    context.temp_filename = temp_file.name
    temp_file.close()


@step("the delta live table pipelines have been refreshed") # type: ignore[no-redef]
def step_impl(context): # pylint: disable=function-redefined,unused-argument
    """
    :type context: behave.runner.Context
    """
    delta_live_tables = DeltaLiveTables()
    pipelines = delta_live_tables.load_from_json()
    delta_live_tables.refresh(pipelines)

@step("the new delta live table pipeline is added") # type: ignore[no-redef]
def step_impl(context): # pylint: disable=function-redefined
    """
    :type context: behave.runner.Context
    """
    delta_live_tables = DeltaLiveTables()
    pipeline = delta_live_tables.get("feature_test_pipeline")
    assert pipeline is not None
    # delete the pipeline
    delta_live_tables.delete(pipeline.get("pipeline_id"))
    # delete the temp file
    os.unlink(context.temp_filename)

@when("an existing delta live table pipeline has been modified") # type: ignore[no-redef]
def step_impl(context): # pylint: disable=function-redefined, unused-argument
    """
    :type context: behave.runner.Context
    """
    with open("./test/data/dlt_example.json", encoding="utf-8") as pipeline_json:
        pipeline = json.load(pipeline_json)
        # make an arbitrary change, set max_workers to 2
        pipeline["clusters"][0]["autoscale"]["max_workers"] = 2
        context.modified_pipeline = pipeline


@then("the existing delta live table pipeline is updated") # type: ignore[no-redef]
def step_impl(context): # pylint: disable=function-redefined
    """
    :type context: behave.runner.Context
    """
    delta_live_tables = DeltaLiveTables()
    pipeline = delta_live_tables.get("feature_test_pipeline")
    assert pipeline["spec"]["clusters"][0]["autoscale"]["max_workers"] == 2
    # delete the pipeline
    delta_live_tables.delete(pipeline.get("pipeline_id"))
    # delete the temp file
    os.unlink(context.temp_filename)
