import pytest

from src.api.baseApi import BaseAPI
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
