import pytest

from src.api.v1_apis.v1_my_account_services import MyAccountSercice
from src.entity.yaml_operation import YamlOperation
from src.entity.src_data_path import SrcDataPath

class Test_MyAccountService:
    data_relative_path = 'src/api/testcases_api/test_v1_my_account_services_data.yaml'
    email = 'kyleyao@aaxischina.com'
    pwd = '123456aA'
    login_info = [(email, pwd)]
    test_data = YamlOperation.load_yaml_file(SrcDataPath.get_src_data_path(data_relative_path))

    @classmethod
    def setup_class(cls):
        cls.myAccount = MyAccountSercice()
        cls.case_api_version = 'v1'

    @pytest.mark.parametrize('test_login', test_data['test_login'])
    def test_login(self, test_login):
        # test_data = YamlOperation.load_yaml_file(SrcDataPath.get_src_data_path(self.data_relative_path))
        # print(test_data['test_login'])
        print(test_login)
        email = test_login.get('email')
        password = test_login.get('password')
        r = self.myAccount.login(email, password)
        # r.json()
        print(r)
        print(r.json())

    @pytest.mark.parametrize('accountId', ['280381', '280381'])
    def test_switchAccount(self, accountId):
        r = self.myAccount.switchAccount(accountId)
        print(r.json())

    def test_accounts(self):
        r = self.myAccount.accounts('user22340000')
        print(r.json())

    def test_logout(self):
        r = self.myAccount.logout()
        print(r.json())
