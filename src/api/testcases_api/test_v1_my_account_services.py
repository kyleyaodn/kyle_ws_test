import pytest

from src.api.baseApi import BaseAPI
from src.api.v1_apis.my_account_services_v1 import MyAccountService
from src.api.v1_apis.v1_my_account_services import MyAccountSercice
from src.entity.yaml_operation import YamlOperation
from src.entity.src_data_path import SrcDataPath


class TestMyAccountService:
    data_relative_path = 'src/api/testcases_api/test_v1_my_account_services_data.yaml'
    test_data = YamlOperation.load_yaml_file(SrcDataPath.get_src_data_path(data_relative_path))
    case_api_version = 'v1'

    @classmethod
    def setup_class(cls):
        cls.myAccount = MyAccountSercice()
        cls.new_myAccount = MyAccountService()
        cls.baseAPI = BaseAPI()

    @pytest.mark.parametrize('email, password',
                             [(test_data['test_login'].get('email'), test_data['test_login'].get('password'))])
    def test_login(self, email, password):
        r = self.myAccount.login(email, password, case_api_version=self.case_api_version)
        # r.json()
        print(r)
        print(r.json())

    @pytest.mark.parametrize('accountId', test_data['test_switchAccount'].get('accountId'))
    def test_switchAccount(self, accountId):
        print(self.test_data['test_switchAccount'].get('accountId'))
        r = self.myAccount.switchAccount(accountId, case_api_version=self.case_api_version)
        print(r.json())

    def test_accounts(self):
        r = self.myAccount.accounts('user22340000', case_api_version=self.case_api_version)
        print(r.json())

    def test_logout(self):
        r = self.myAccount.logout(case_api_version=self.case_api_version)
        print(r.json())

    # @pytest.mark.scenario
    # @pytest.mark.parametrize('email, password',
    #                          [(test_data['test_login'].get('email'), test_data['test_login'].get('password'))])
    # def test_login_logout(self,email, password):
    #     r = self.myAccount.login(email, password)

    def test_login_logout(self):
        print(self.test_data['test_login_logout']['login_api']['data_json'])
        resp = self.new_myAccount.login(data_json=self.test_data['test_login_logout']['login_api']['data_json'],
                                        case_api_version=self.case_api_version)
        self.new_myAccount.base_assertion(resp)
        self.new_myAccount.validate_json_schema('schema_path_success', self.new_myAccount.api_define, resp)
        resp = self.new_myAccount.logout(case_api_version=self.case_api_version)
        self.new_myAccount.base_assertion(resp)
