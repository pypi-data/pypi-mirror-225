""" Bronze table module. """
from typing import Any

# Databricks notebook source
import dlt

from databricks.connect import DatabricksSession # type: ignore

spark = DatabricksSession.builder.getOrCreate()
@dlt.table(comment="The raw price_paid dataset, ingested from s3://workflow_sync/price_paid.") # type: ignore[attr-defined, misc] # pylint: disable=no-member
def bronze() -> Any:
    """
    The raw average price data from gov.uk, ingested from s3://workflow_sync/price_paid.
    :return:
    """
    return spark.read.format("csv").load("s3://workflow_sync/price_paid/")

# @dlt.table(
#   comment="The raw average price data from gov.uk, ingested from s3://workflow_sync/price_paid."
# )
# def bronze():
#   return (spark.read.format("csv").load("s3://workflow_sync/price_paid/"))
#
# # COMMAND ----------
