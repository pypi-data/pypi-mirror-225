""" Silver table module.  """
from typing import Any

# Databricks notebook source
import dlt

from pyspark.sql.functions import col, to_date, year, month
from pyspark.sql.types import IntegerType

@dlt.table( # type: ignore[attr-defined, misc] # pylint: disable=no-member
  comment="The silver table, validated price_paid data contained in the bronze table dataset."
)
def silver() -> Any:
    """ Builds the silver table.  """
    bronze = dlt.read("bronze") # type: ignore[attr-defined] # pylint: disable=no-member
    # rename columns
    silver_table = bronze.withColumnRenamed("_c0", "uid") \
        .withColumnRenamed("_c1", "price") \
        .withColumnRenamed("_c2", "date") \
        .withColumnRenamed("_c3", "postcode") \
        .withColumnRenamed("_c4", "type") \
        .withColumnRenamed("_c5", "old_new") \
        .withColumnRenamed("_c6", "duration") \
        .withColumnRenamed("_c7", "PAON") \
        .withColumnRenamed("_c8", "SAON") \
        .withColumnRenamed("_c9", "street") \
        .withColumnRenamed("_c10", "locality") \
        .withColumnRenamed("_c11", "town") \
        .withColumnRenamed("_c12", "district") \
        .withColumnRenamed("_c13", "county") \
        .withColumnRenamed("_c14", "category") \
        .withColumnRenamed("_c15", "status")
    # change column types
    silver_table = silver_table.withColumn("price", col("price").cast(IntegerType())) \
        .withColumn("date", to_date(col("date"), 'yyyy-MM-dd HH:mm'))
    # add year and month columns
    silver_table = silver_table.withColumn('year', year(col("date"))) \
        .withColumn('month', month(col("date")))
    return silver_table
