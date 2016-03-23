from fabric import api as fab
import os
from aws.operations import running

# Get the key file to be used by fabric for remote ssh calls.
fab.env.key_filename = os.environ['EC2_DEFAULT_KEY_FILE']


def run(command):
    fab.local(command)


def remote_run(command, instance_name):
    with running(instance_name) as wrapped:
        fab.env.hosts = [wrapped.host_name]
        fab.run(command)


def ssh(instance_name):
    with running(instance_name) as instance:
        fab.local('ssh ' + instance.host_name)
