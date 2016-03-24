from fabric.api import task
from fabric import api as fab
import os
from operations import running

# Get the key file to be used by fabric for remote ssh calls.
try:
    fab.env.key_filename = os.environ['EC2_DEFAULT_KEY_FILE']
except (NameError, KeyError):
    pass


@task
def ssh(instance_name):
    with running(instance_name) as instance:
        fab.local('ssh ' + instance.host_name)


@task
def remote_run(command, instance_name):
    with running(instance_name) as instance:
        fab.env.host_string = instance.host_name
        fab.run(command)
