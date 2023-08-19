""" Module for ingesting data from outside AWS into AWS. """
import os
from typing import Optional
from urllib import request

from databricks.sdk.runtime import dbutils  # type: ignore


def path_exists(path: str) -> bool:
    """ Check to see whether a path already exists.  Returns True if the path
     exists or False if it doesn't. """
    if path[:5] == "/dbfs":
        return os.path.exists(path)
    try:
        dbutils.fs.ls(path)
        return True
    except Exception as exc: # pylint: disable=broad-exception-caught
        if 'java.io.FileNotFoundException' in str(exc):
            return False
        raise

def url_to_s3(url: str, project: str, filename: Optional[str] = None) -> None:
    """ Downloads a file from the internet and saves it to S3. """
    if not filename:
        filename = os.path.basename(url)
    s3_loc = "s3://workflow_sync/" + project + "/" + filename
    if path_exists(s3_loc):
        raise IOError("File exists already so will not be downloaded again")
    tmp_loc = "/dbfs/tmp/" + filename
    request.urlretrieve(url, tmp_loc)
    dbutils.fs.mv(f"file:{tmp_loc}", s3_loc)
