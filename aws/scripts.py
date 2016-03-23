import name_binding
import sys
from fabfile import ssh as _ssh
from fabric.tasks import execute


def rebind_ec2_names():
    name_binding.export_name_bindings_to_file()


def command_test():
    print 'Number of arguments:', len(sys.argv)


def ssh():
    execute(_ssh, sys.argv[1])
