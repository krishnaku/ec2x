import name_binding
import tasks
import argh
from argh.decorators import arg
from fabric.tasks import execute


def rehash():
    """Update the cached binding of instance names to instance_id and public_dns_names"""
    name_binding.export_name_bindings_to_file()


@arg('instance_name', help='name of the ec2 instance')
def ssh(instance_name):
    """ssh into a remote ec2 instance by name.

    Example: btx ssh <instance_name>
    """
    execute(tasks.ssh, instance_name)


@arg('instance_name', help='name of the ec2 instance')
@arg('command', help='command to be executed')
def remote(instance_name, *command):
    """Execute a remote ssh command on the named instance

    Example: btx remote <instance_name> ps ax | grep foo
    """
    execute(tasks.remote_run,
            _concat(command),
            instance_name)


def _concat(command):
    return reduce(lambda out, s: out + s + ' ', command, '')


def __main__():
    argh.dispatch_commands(
        [
            ssh,
            remote,
            rehash

        ])
