from src.api.baseApi import BaseAPI


class MyAccountService(BaseAPI):
    api_relative_Path = 'src/api/configure_files/config_api/api_definition/Beacon_Rest_Services_V1.yaml'

    '''
    This is My Account Services APIs
    '''

    def __init__(self):
        self.data = self.load_api(self.api_relative_Path)
        self.api_version = 'v1'
        self.params = {}
        self.api_define = None
        self.resp = None

    def login(self, **kwargs):
        self.params.clear()
        # self.params['username'] = username
        # self.params['password'] = password
        self.api_define = self.data.get("My_Account_Services").get("login")
        self.resp = self.send_requests(self.api_define, **kwargs)
        return self.resp

    def logout(self, **kwargs):
        self.api_define = self.data.get("My_Account_Services").get("logout")
        return self.send_requests(self.api_define, **kwargs)

    def getLoginDeclaration(self, **kwargs):
        self.api_define = self.data.get("My_Account_Services").get("getLoginDeclaration")
        return self.send_requests(self.api_define, **kwargs)

    def getCurrentUserInfo(self, **kwargs):
        self.api_define = self.data.get("My_Account_Services").get("getCurrentUserInfo")
        return self.send_requests(self.api_define, **kwargs)

    def accounts(self, **kwargs):
        # self.params.clear()
        # self.params['profileId'] = profileId
        # print(self.params)
        self.api_define = self.data.get("My_Account_Services").get("accounts")
        return self.send_requests(self.api_define, **kwargs)

    def switchAccount(self, accountId, **kwargs):
        # self.params.clear()
        # self.params['accountId'] = accountId
        # print(self.params)
        self.api_define = self.data.get("My_Account_Services").get("switchAccount")
        return self.send_requests(self.api_define, **kwargs)
