import pytest

from src.api.v1_apis.my_account_services_v1 import MyAccountService
from src.entity.commen_tools import CommonTools
from src.entity.src_data_path import SrcDataPath
from src.entity.yaml_operation import YamlOperation

data_relative_path = 'src/api/test_data/${run_env}/v1_apis/test_v1_my_account_services_data.yaml'
env_path = 'src/api/configure_files/config_env.yaml'
env = YamlOperation.load_yaml_file(SrcDataPath.get_src_data_path(env_path))
run_env = {}
run_env['run_env'] = env.get('run_env')
case_api_version = 'v1'
data_file_path = SrcDataPath.get_src_data_path(CommonTools.replace_value(data_relative_path, run_env))
test_data = YamlOperation.load_yaml_file(data_file_path)
my_account = MyAccountService()

@pytest.fixture(scope="session", autouse="true")
def login():
    print('***********************************************fixture setup')
    my_account.run_steps(test_data['base_login'], case_api_version=case_api_version)

    yield

    print('***********************************************fixture teardown')
    my_account.run_steps(test_data['base_logout'], case_api_version=case_api_version)