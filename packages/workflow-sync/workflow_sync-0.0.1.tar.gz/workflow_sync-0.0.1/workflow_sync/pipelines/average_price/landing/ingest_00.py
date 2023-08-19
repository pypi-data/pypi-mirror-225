""" Data ingestion module for the landing pipeline. """
# Databricks notebook source
# Copyright (c) 2023, ZWIO
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# download the last months property data to S3
from workflow_sync import ingest
# MAGIC
# given the file exists in 's3://workflow_sync/price_paid'
# when I run the pipeline
# then the pipeline will not download the file again
# MAGIC
# given the file does not exist in 's3://workflow_sync/price_paid'
# when I run the pipeline
# then the pipeline will download the file
# MAGIC
# load all price paid data prior to current month
PROJECT = "price_paid"
URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1." \
      "amazonaws.com/pp-complete.csv"
ingest.url_to_s3(URL, PROJECT)
# MAGIC
# load current months price paid data
URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1." \
      "amazonaws.com/pp-monthly-update-new-version.csv"
# new version is two months behind current month, if job is run on 22nd of
# every month (22nd since data is updated on the 20th and to allow for the
# weekend)
# filename = f"{datetime.today().year}{datetime.today().month - 2:02}.csv"
# ingest.url_to_s3(URL, PROJECT, filename)
# # MAGIC
# # download average property price data from gov.uk
# URL = "http://publicdata.landregistry.gov.uk/market-trend-data/" \
#       "house-price-index-data/Average-prices-2023-04.csv"
# ingest.url_to_s3(URL, PROJECT)
