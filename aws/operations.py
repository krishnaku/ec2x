import boto3
import name_binding
import os


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


def find_ec2_instance(instance_id, ec2=None):
    if ec2 is None:
        ec2 = boto3.resource('ec2')
    for result in ec2.instances.filter(InstanceIds=[instance_id]):
        return _ec2(result)
    raise NoSuchInstance("Instance Id: " + instance_id)


def running(instance_id, ec2=None):
    with find_ec2_instance(instance_id, ec2) as wrapped:
        rebind = False
        if wrapped.state in ['shutting-down', 'terminated']:
            raise IllegalState('Instance is ' + wrapped.state)
        if wrapped.state in ['stopping', 'stopped']:
            print 'Waiting for instance to stop...'
            wrapped.instance.wait_until_stopped()
        if wrapped.state not in ['pending', 'running']:
            print 'Starting instance...'
            wrapped.instance.start()
            rebind = True
        wrapped.instance.wait_until_running()
        name_binding.export_name_bindings_to_environment(ec2)
        if rebind:
            print "Rebinding all names"
            name_binding.export_name_bindings_to_file(ec2)

    return wrapped


with running('i-05bbd8ea9905f3aa5') as wrap:
    print wrap.instance.public_dns_name + os.environ['euler_id']
