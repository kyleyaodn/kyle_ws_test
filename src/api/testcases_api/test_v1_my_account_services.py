import pytest

from kyle_ws_test.src.api.v1_apis.v1_my_account_services import MyAccountSercice


class Test_MyAccountService:

    @classmethod
    def setup_class(cls):
        cls.myAccount = MyAccountSercice()
        cls.case_api_version = 'v1'

    def test_login(self):
        r = self.myAccount.login('kyleyao@aaxischina.com', '123456aA')
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
