from mock import MagicMock
from pytest import fixture

from StringIO import StringIO


def mock_ec2_instance(name, state='stopped', **kwargs):
    instance = MagicMock(
        name='ec2-instance-' + name,
        tags=[
            {
                'Key': 'Name',
                'Value': name
            }
        ],
        **kwargs
    )
    instance.state = {'Name': state, 'Code': 0}
    return instance


@fixture
def stopped():
    return mock_ec2_instance(name='euler', state='stopped')


@fixture
def i_pending():
    return mock_ec2_instance(name='euler', state='pending')


@fixture
def i_running():
    return mock_ec2_instance(name='euler', state='running')


@fixture
def i_stopping():
    return mock_ec2_instance(name='euler', state='stopping')


@fixture
def i_shutting_down():
    return mock_ec2_instance(name='euler', state='shutting-down')


@fixture
def i_terminated():
    return mock_ec2_instance(name='euler', state='terminated')


@fixture(params=[i_shutting_down(), i_terminated()])
def terminating_instance(request):
    return request.param


@fixture(params=[i_pending(), i_running()])
def starting_instance(request):
    return request.param


@fixture(params=[i_stopping(), stopped()])
def stopping_instance(request):
    return request.param

# Hack-ish class that extends StringIO so that it can be used in place of a file in
# tests in a with statement.
class StringIOCtx(StringIO):
    def __init__(self):
        StringIO.__init__(self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        return False
