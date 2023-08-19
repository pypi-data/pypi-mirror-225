"""
setup.py required for PyPi distribution.
"""
from setuptools import setup

setup(
    name='workflow_sync',
    version='0.0.4',
    packages=['test', 'features', 'features.steps', 'workflow_sync',
              'workflow_sync.extract', 'workflow_sync.pipelines',
              'workflow_sync.pipelines.price_paid',
              'workflow_sync.pipelines.average_price',
              'workflow_sync.pipelines.average_price.landing'],
    url='http://zwio.com',
    license='The 3-Clause BSD License',
    author='Daniel Humphreys',
    author_email='dan.humphreys@zwio.com',
    description='Library for syncing Databricks workflows (jobs and delta live tables)'
)
