from test_helpers import *
from ec2x import name_binding, operations

from mock import patch
from ec2x.tasks import *

from fabric import api


class ssh_tests:
    @patch('fabric.api.local')
    def it_calls_running_to_get_a_running_ec2_instance_and_opens_an_ssh_shell(self, local_method):
        instance = operations._ec2(mock_ec2_instance('euler', 'running', public_dns_name='aws.euler'))
        with patch('ec2x.tasks.running', return_value=instance) as running_method:
            ssh('euler')
            running_method.assert_called_with('euler')
            local_method.assert_called_with('ssh ec2-user@aws.euler')


class remote_run_tests:
    @patch('fabric.api.run')
    def it_calls_running_to_get_a_running_ec2_instance_and_then_executes_the_remote_command(self, run_method):
        instance = operations._ec2(mock_ec2_instance('euler', 'running', public_dns_name='aws.euler'))
        with patch('ec2x.tasks.running', return_value=instance) as running_method:
            remote_run('ls -al', 'euler')
            running_method.assert_called_with('euler')
            run_method.assert_called_with('ls -al')
            assert api.env.host_string == 'ec2-user@aws.euler'


class local_tests:
    @patch('fabric.api.local')
    def it_exports_name_bindings_to_the_environment_and_then_executes_the_command_locally(self, local_method):
        with patch('ec2x.tasks.export_name_bindings_to_environment') as export_method:
            local('ls -al')
            assert export_method.called
            local_method.assert_called_with('ls -al')
