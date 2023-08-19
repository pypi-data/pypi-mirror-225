# workflow-sync

A library for syncing Databricks workflows defined in JSON format with Databricks.

## Introduction

Databricks jobs and Delta Live Table pipelines (workflows) are usually created manually using the Databricks web user interface.  At [zwio](www.zwio.com) we wanted to manage our pipelines using Git and JSON and therefore needed a way to sync our JSON workflows in Databricks.

## Usage

Clone from Github:

```
git clone https://github.com/zwio-com/workflow-sync.git
cd workflow-sync
```

Set environment variables:

```
CLUSTER_ID=
```

Run:

```shell
python sync --dir=
```