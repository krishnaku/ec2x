from mock import patch
from ec2x.name_binding import *
from pytest import fixture

from test_helpers import *
import os

from ec2x.name_binding import _open_aws_env_file, AWS_CONFIG_DIR


# Test ec2_instance_attributes
class ec2_instance_attributes_tests:

    def it_calls_boto3_resource_to_fetch_the_service_handle(self):
        with patch('boto3.resource') as mock:
            ec2_service_mock = mock.return_value
            ec2_service_mock.instances.all.return_value = []
            ec2_instance_attributes()
            mock.assert_called_with('ec2')

    def it_retrieves_the_list_of_instances_from_the_service_resource(self):
        with patch('boto3.resource') as mock:
            ec2_service_mock = mock.return_value
            ec2_service_mock.instances.all.return_value = []
            ec2_instance_attributes()
            assert ec2_service_mock.instances.all.called

    def it_extracts_name_id_and_public_dns_name_of_the_instances(self):
        with patch('boto3.resource') as mock:
            ec2_service_mock = mock.return_value
            ec2_service_mock.instances.all.return_value = [
                    mock_ec2_instance('gauss', id='i-23001', public_dns_name='gauss.aws')
            ]
            attributes = ec2_instance_attributes()

            assert len(attributes) == 1
            assert attributes[0]['name'] == 'gauss'
            assert attributes[0]['id'] == 'i-23001'
            assert attributes[0]['public_dns_name'] == 'gauss.aws'


# test_get_ec2_name_bindings
def get_ec2_name_bindings_mapping_examples():
    return [
        # Single input
        {
            'input': [
                {
                    'name': 'gauss',
                    'id': 'i-20134',
                    'public_dns_name': 'gauss.aws'
                }
            ],
            'expect': {
                'gauss': 'gauss.aws',
                'gauss_id': 'i-20134'
            }
        },

        # Single input with extra attributes that should be ignored
        {
            'input': [
                {
                    'name': 'gauss',
                    'id': 'i-20134',
                    'public_dns_name': 'gauss.aws',
                    'state': 'running'
                }
            ],
            'expect': {
                'gauss': 'gauss.aws',
                'gauss_id': 'i-20134'
            }
        },

        # Multiple Input instances
        {
            'input': [
                {
                    'name': 'gauss',
                    'id': 'i-20134',
                    'public_dns_name': 'gauss.aws',
                    'state': 'running'
                },
                {
                    'name': 'euler',
                    'id': 'i-20135',
                    'public_dns_name': 'euler.aws',
                    'state': 'running'
                },

            ],
            'expect': {
                'gauss': 'gauss.aws',
                'gauss_id': 'i-20134',
                'euler': 'euler.aws',
                'euler_id': 'i-20135'
            }
        }
    ]


@fixture(params=get_ec2_name_bindings_mapping_examples())
def name_binding_mappings_example(request):
    return request.param


class get_ec2_name_bindings_tests:
    def it_calls_ec2_instance_attributes_to_get_instance_info(self):
        with patch('ec2x.name_binding.ec2_instance_attributes', return_value=[]) as mock:
            get_ec2_name_bindings()
            assert mock.called

    def verify_bindings_mapping(self, name_binding_mappings_example):
        with patch('ec2x.name_binding.ec2_instance_attributes') as mock:
            mock.return_value = name_binding_mappings_example['input']
            result = get_ec2_name_bindings()

            expect = name_binding_mappings_example['expect']

            for k, v in expect.iteritems():
                assert k in result and result[k] == v


# export_name_bindings_to_file

def get_export_name_bindings_output_examples():
    return [
        {
            'input': {
                'gauss': 'gauss.aws',
                'gauss_id': 'i-20134'
            },
            'expect': [
                "export gauss=gauss.aws",
                "export gauss_id=i-20134"
            ]

        },
        {
            'input': {
                'gauss': 'gauss.aws',
                'gauss_id': 'i-20134',
                'euler': 'euler.aws',
                'euler_id': 'i-20135'
            },
            'expect': [
                "export gauss=gauss.aws",
                "export gauss_id=i-20134",
                "export euler=euler.aws",
                "export euler_id=i-20135"
            ]
        }
    ]


@fixture(params=get_export_name_bindings_output_examples())
def name_binding_exports_example(request):
    return request.param


class export_name_bindings_to_file_tests:
    def it_calls_get_ec2_name_bindings_to_get_the_name_bindings(self):
        with patch('ec2x.name_binding.get_ec2_name_bindings', return_value={}) as get_ec2_name_bindings_method:
            with patch('ec2x.name_binding._open_aws_env_file', return_value=StringIOCtx()):
                export_name_bindings_to_file()
                assert get_ec2_name_bindings_method.called

    def it_writes_bindings_to_file_as_env_exports(self, name_binding_exports_example):
        file_mock = StringIOCtx()
        with patch('ec2x.name_binding.get_ec2_name_bindings',
                   return_value=name_binding_exports_example['input']) as get_ec2_name_bindings_method:
            with patch('ec2x.name_binding._open_aws_env_file', return_value=file_mock):
                export_name_bindings_to_file()

                output = file_mock.getvalue()
                expect = name_binding_exports_example['expect']
                for mapping in expect:
                    assert mapping in output

        file_mock.close()


# export_name_bindings_to_environment

class export_name_bindings_to_environment_tests:
    def it_calls_get_name_bindings_to_get_the_name_bindings(self):
        with patch('ec2x.name_binding.get_ec2_name_bindings', return_value={}) as get_ec2_name_bindings_method:
            export_name_bindings_to_environment()
            assert get_ec2_name_bindings_method.called

    def it_exports_bindings_to_the_environment(self, name_binding_exports_example):
        with patch('ec2x.name_binding.get_ec2_name_bindings',
                   return_value=name_binding_exports_example['input']) as get_ec2_name_bindings_method:
            export_name_bindings_to_environment()

            for k, v in name_binding_exports_example['input'].iteritems():
                assert k in os.environ and os.environ[k] == v


# rebind_all
class rebind_all_tests:
    def it_calls_export_name_bindings_to_file(self):
        with patch('ec2x.name_binding.export_name_bindings_to_file') as mock:
            rebind_all()
            assert mock.called

    def it_calls_export_name_bindings_to_environment(self):
        with patch('ec2x.name_binding.export_name_bindings_to_environment') as mock:
            rebind_all()
            assert mock.called


# _open_aws_env_file


class _open_aws_env_file_tests:
    @patch('os.path.exists', return_value=False)
    def it_creates_the_environment_directory_if_it_does_not_exist(self, os_path_exists_ignored):
        with patch('os.mkdir') as os_mkdir:
            _open_aws_env_file('w')
            os_mkdir.assert_called_with(AWS_CONFIG_DIR)

    @patch('os.path.exists', return_value=True)
    @patch('os.mkdir')
    def it_opens_the_config_file_with_the_mode_specified(self, os_mkdir, os_path_exists_ignored):
        with patch('__builtin__.open', return_value=StringIO()) as _open:
            _open_aws_env_file('w')

            _open.assert_called_with(AWS_CONFIG_FILE, 'w')
            assert not os_mkdir.called
