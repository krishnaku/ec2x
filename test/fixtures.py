from mock import MagicMock, PropertyMock


# helpers to construct ec2 service mocks. Somewhat obscure due to the way
# mock handles properties and the way ec2 handles tags. Figured it was better to isolate the complexity
# here rather than

def configure_ec2_service_mock(mock_instances=None):
    if mock_instances is None:
        mock_instances = []

    mock = MagicMock('ec2.ServiceResource', name='ec2-service-resource-mock')

    # setting up the mock for the instances property of the service resource.

    instances_method_mock = PropertyMock(
        return_value=MagicMock(
            # mock for the all() iterable on instances. creates an iterable over the passed in list.
            all=MagicMock(return_value=iter(mock_instances))
        ))
    # this is a magic incantation to let mock attach the PropertyMock as a property of the mock.
    type(mock).instances = instances_method_mock

    # we need this awful thing because once the property mock is attached it returns its return value
    # when accessed. so we lose the orignal mock object and need someway to get a reference to the
    # PropertyMock to examine its call history etc.
    # so we can do things like mock.instance_method.called etc.. once we have the enclosing mock.
    type(mock).instances_property = PropertyMock(return_value=instances_method_mock)
    return mock


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
