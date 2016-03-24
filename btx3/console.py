import name_binding
import tasks
import argh
from argh.decorators import arg
from fabric.tasks import execute


def rehash():
    """Update the binding of instance names to instance_id and public_dns_names
    and also update the name_binding cache.
    """
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

    Examples:
        btx remote <instance_name> ps ax
        :show the processes running on the remote instance <instance>

        btx remote <instance_name> \"ps ax | grep ssh\"
        :run the piped command sequence on the remote instance
    """
    execute(tasks.remote_run,
            _concat(command),
            instance_name)


@arg('command', help='commmand to be executed')
def local(*command):
    """Execute a local command with the ec2 name bindings in the environment

    Example: btx local echo "The public dns name of the instance named euler is " $euler
    """
    tasks.local(_concat(command))


def _concat(command):
    return reduce(lambda out, s: out + s + ' ', command, '')


def __main__():
    argh.dispatch_commands(
        [
            ssh,
            remote,
            local,
            rehash

        ])
