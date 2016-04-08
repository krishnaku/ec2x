from mock import patch
from pytest import raises

from ec2x.operations import *
from ec2x.operations import _ec2
from test_helpers import *


# find_ec2_instance
class find_ec2_instance_tests:
    def it_calls_boto3_resource_and_filter_to_fetch_the_service(self):
        with patch('boto3.resource') as mock:
            ec2_mock = mock.return_value
            ec2_mock.instances.filter.return_value = [MagicMock()]
            find_ec2_instance('foo')
            assert mock.called
            assert ec2_mock.instances.filter.called

    def it_returns_a_wrapped_service_instance_if_found(self):
        with patch('boto3.resource') as mock:
            ec2_mock = mock.return_value
            found_instance = MagicMock()
            ec2_mock.instances.filter.return_value = [found_instance]
            result = find_ec2_instance('foo')
            assert result is not None \
                   and isinstance(result, _ec2) \
                   and result.instance == found_instance

    def it_throws_NoSuchInstanceException_if_not_found(self):
        with patch('boto3.resource') as mock:
            with raises(NoSuchInstance):
                ec2_mock = mock.return_value
                ec2_mock.instances.filter.return_value = []
                find_ec2_instance('foo')


# running

class running_tests:
    def it_calls_find_ec2_instance_to_fetch_the_instance(self):
        with patch('ec2x.operations.find_ec2_instance', side_effect=NoSuchInstance) as find_ec2_instance_method:
            try:
                running('foo')
            except NoSuchInstance:
                assert find_ec2_instance_method.called

    def it_throws_an_exception_if_the_instance_is_shutting_down_or_terminated(self, terminating_instance):
        with patch('ec2x.name_binding.rebind_all') as rebind:
            with patch('ec2x.operations.find_ec2_instance', return_value=_ec2(terminating_instance)):
                with raises(IllegalState):
                    running('euler')
            assert not rebind.called

    def it_waits_for_a_stopping_instance_to_stop_and_waits_till_it_restarts(self, stopping_instance):
        with patch('ec2x.name_binding.rebind_all') as rebind:
            with patch('ec2x.operations.find_ec2_instance', return_value=_ec2(stopping_instance)):
                running('euler')
                assert stopping_instance.wait_until_stopped.called
                assert stopping_instance.start.called
                assert stopping_instance.wait_until_running.called
            assert rebind.called

    def it_waits_for_a_pending_or_running_instance_to_start_and_does_not_call_start_again(self, starting_instance):
        with patch('ec2x.name_binding.rebind_all') as rebind:
            with patch('ec2x.operations.find_ec2_instance', return_value=_ec2(starting_instance)):
                running('euler')
                assert starting_instance.wait_until_running.called
                assert not starting_instance.start.called
            assert rebind.called


# _ec2 tests

class _ec2_tests:
    def verify_attributes(self):
        instance = mock_ec2_instance('euler', 'stopped', public_dns_name='aws.euler')
        wrapped = _ec2(instance)
        assert wrapped.instance == instance
        assert wrapped.state == 'stopped'
        assert wrapped.host_name == 'ec2-user@aws.euler'
