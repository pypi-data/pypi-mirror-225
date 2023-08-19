""" Module for building gold table. """
from typing import Any

# Databricks notebook source
import dlt

@dlt.table(comment="The gold table, enhanced price_paid data contained in the" # type: ignore[attr-defined, misc]  # pylint: disable=no-member
                   " silver table dataset.")
def gold() -> Any:
    """
    Build gold table.
    :return:
    """
    # silver = dlt.read("silver") # pylint: disable=no-member
    #
    # #gold = silver.withColumn("12_month", mean(col("total_expense")).over(w.rangeBetween(-1, 0)))
    # gold = silver
    return dlt.read("silver") # type: ignore[attr-defined] # pylint: disable=no-member
