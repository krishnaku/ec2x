from mock import MagicMock, patch
import boto3
from ec2x import name_binding
from fixtures import *


class ec2_instance_attributes_tests:
    def it_calls_boto3_resource_to_fetch_the_service_handle(self):
        with patch('boto3.resource') as mock:
            mock.return_value = configure_ec2_service_mock([])
            name_binding.ec2_instance_attributes()
            mock.assert_called_with('ec2')

    def it_retrieves_the_list_of_instances_from_the_service_resource(self):
        with patch('boto3.resource') as mock:
            ec2_service_mock = configure_ec2_service_mock([])
            mock.return_value = ec2_service_mock
            name_binding.ec2_instance_attributes()
            assert ec2_service_mock.instances.all.called

    def it_extracts_name_id_and_public_dns_name_of_the_instances(self):
        with patch('boto3.resource') as mock:
            mock.return_value = configure_ec2_service_mock(
                [
                    mock_ec2_instance('gauss', id='i-23001', public_dns_name='gauss.aws')
                ]
            )
            attributes = name_binding.ec2_instance_attributes()

            assert len(attributes) == 1
            assert attributes[0]['name'] == 'gauss'
            assert attributes[0]['id'] == 'i-23001'
            assert attributes[0]['public_dns_name'] == 'gauss.aws'
