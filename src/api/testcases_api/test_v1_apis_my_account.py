import pytest

from src.api.v1_apis.my_account_services_v1 import MyAccountService
from src.entity.src_data_path import SrcDataPath
from src.entity.yaml_operation import YamlOperation
from src.entity.commen_tools import CommonTools


class TestMyAccountServices:
    data_relative_path = 'src/api/test_data/${run_env}/v1_apis/test_v1_my_account_services_data.yaml'
    env_path = 'src/api/configure_files/config_env.yaml'
    env = YamlOperation.load_yaml_file(SrcDataPath.get_src_data_path(env_path))
    run_env = {}
    run_env['run_env'] = env.get('run_env')
    case_api_version = 'v1'
    data_file_path = SrcDataPath.get_src_data_path(CommonTools.replace_value(data_relative_path, run_env))
    test_data = YamlOperation.load_yaml_file(data_file_path)

    @classmethod
    def setup_class(cls):
        cls.my_account = MyAccountService()

    @pytest.mark.parametrize('login_logout_data', [test_data['login_logout_data']])
    def test_login_logout(self, login_logout_data):
        self.my_account.run_steps(login_logout_data, case_api_version=self.case_api_version)
