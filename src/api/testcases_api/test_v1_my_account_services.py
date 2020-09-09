import pytest

from src.api.v1_apis.v1_my_account_services import MyAccountSercice
from src.entity.yaml_operation import YamlOperation
from src.entity.src_data_path import SrcDataPath


class Test_MyAccountService:
    data_relative_path = 'src/api/testcases_api/test_v1_my_account_services_data.yaml'
    test_data = YamlOperation.load_yaml_file(SrcDataPath.get_src_data_path(data_relative_path))

    @classmethod
    def setup_class(cls):
        cls.myAccount = MyAccountSercice()
        cls.case_api_version = 'v1'

    @pytest.mark.parametrize('email, password',
                             [(test_data['test_login'].get('email'), test_data['test_login'].get('password'))])
    def test_login(self, email, password):
        r = self.myAccount.login(email, password)
        # r.json()
        print(r)
        print(r.json())

    @pytest.mark.parametrize('accountId', test_data['test_switchAccount'].get('accountId'))
    def test_switchAccount(self, accountId):
        print(self.test_data['test_switchAccount'].get('accountId'))
        r = self.myAccount.switchAccount(accountId)
        print(r.json())

    def test_accounts(self):
        r = self.myAccount.accounts('user22340000')
        print(r.json())

    def test_logout(self):
        r = self.myAccount.logout()
        print(r.json())

    @pytest.mark.scenario
    @pytest.mark.parametrize('email, password',
                             [(test_data['test_login'].get('email'), test_data['test_login'].get('password'))])
    def test_login_logout(self,email, password):
        r = self.myAccount.login(email, password)