from mock import MagicMock, PropertyMock

from StringIO import StringIO


def mock_ec2_instance(name, **kwargs):
    return MagicMock(
        'ec2.Instance',
        name='ec2-instance-' + name,
        tags=[
            {
                'Key': 'Name',
                'Value': name
            }
        ],
        **kwargs
    )


# Hack-ish class that extends StringIO so that it can be used in place of a file in
# tests in a with statement.
class StringIOCtx(StringIO):
    def __init__(self):
        StringIO.__init__(self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        return False
