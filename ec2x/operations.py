import boto3

from . import name_binding


class NoSuchInstance(Exception):
    pass


class IllegalState(Exception):
    pass


# wrapper around ec2 instance that defines __enter__ and __exit__ methods so that
# they can be used as resources in with statements. The instance method can be
# used to grab the underlying ec2 instance object when needed.
# also adds some utility methods to cleanup the api access.


class _ec2:
    def __init__(self, ec2_instance):
        self.__instance__ = ec2_instance

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        return False

    @property
    def instance(self):
        return self.__instance__

    @property
    def state(self):
        return self.instance.state['Name']

    @property
    def host_name(self):
        return 'ec2-user@' + self.instance.public_dns_name


def find_ec2_instance(instance_name):
    ec2 = boto3.resource('ec2')
    for result in ec2.instances.filter(Filters=[{
        'Name': 'tag:Name',
        'Values': [instance_name]
    }]):
        return _ec2(result)
    raise NoSuchInstance("Instance Id: " + instance_name)


def running(instance_name):
    with find_ec2_instance(instance_name) as wrapped:
        if wrapped.state in ['shutting-down', 'terminated']:
            raise IllegalState('Instance is ' + wrapped.state)
        if wrapped.state in ['stopping', 'stopped']:
            print('Waiting for instance to stop...')
            wrapped.instance.wait_until_stopped()
            wrapped.instance.start()
        if wrapped.state not in ['pending', 'running']:
            print('Starting instance...')
            wrapped.instance.start()
        wrapped.instance.wait_until_running()
        name_binding.rebind_all()

    return wrapped

