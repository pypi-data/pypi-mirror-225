# # Databricks notebook source
# """ Module for generating extracts. """
# import requests
# from databricks.sdk.runtime import dbutils # type: ignore
#
# TOKEN = "Bearer TBD"
# headers = {"Accept": "application/json", "Authorization": TOKEN}
# data = { "path": "/Users/dan.humphreys@workflow_sync.com/gen_report", "format": "HTML"}
# url = "https://dbc-d4e2664b-363c.cloud.databricks.com/api/2.0/workspace/export"
# response = requests.get(url, headers=headers, json=data)
# html_enc = response.json()["content"]
#
# # COMMAND ----------
#
# import base64
# html = base64.b64decode(html_enc).decode('utf-8')
#
# # COMMAND ----------
#
# #### MOUNT AND READ S3 FILES
# AWS_BUCKET_NAME = "workflow_sync"
# MOUNT_NAME = "exports"
# dbutils.fs.mount("s3a://%s" % AWS_BUCKET_NAME, "/mnt/%s" % MOUNT_NAME)
# #display(dbutils.fs.ls("/mnt/%s" % MOUNT_NAME))
#
#
# # COMMAND ----------
#
# from datetime import datetime
# timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
# filename = f"extract_{timestamp}.html"
# dbutils.fs.put(f"/mnt/{MOUNT_NAME}/out/{filename}", html)
#
#
# # COMMAND ----------
#
# dbutils.fs.unmount("/mnt/%s" % MOUNT_NAME)
#
# # COMMAND ----------
#
# dbutils.fs.mounts()
