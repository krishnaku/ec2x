from fabric import api as fab
import os
from aws import name_binding

# Get the key file to be used by fabric for remote ssh calls.
fab.env.key_filename = os.environ['EC2_DEFAULT_KEY_FILE']


def ec2_env():
    name_binding.export_name_bindings_to_environment()


def run(command):
    fab.local(command)
