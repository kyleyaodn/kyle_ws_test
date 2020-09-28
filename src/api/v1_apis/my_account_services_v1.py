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

    def login(self, **kwargs):
        self.params.clear()
        # self.params['username'] = username
        # self.params['password'] = password
        self.api_define = self.data.get("My_Account_Services").get("login")
        return self.send_requests(self.api_define, **kwargs)

    def logout(self, **kwargs):
        return self.send_requests(self.data.get("My_Account_Services").get("logout"), **kwargs)

    def getLoginDeclaration(self, **kwargs):
        return self.send_requests(self.data.get("My_Account_Services").get("getLoginDeclaration", **kwargs))

    def getCurrentUserInfo(self, **kwargs):
        return self.send_requests(self.data.get("My_Account_Services").get("getCurrentUserInfo"), **kwargs)

    def accounts(self, profileId, **kwargs):
        self.params.clear()
        self.params['profileId'] = profileId
        # print(self.params)
        return self.send_requests(self.data.get("My_Account_Services").get("accounts"), **kwargs)

    def switchAccount(self, accountId, **kwargs):
        self.params.clear()
        self.params['accountId'] = accountId
        # print(self.params)
        return self.send_requests(self.data.get("My_Account_Services").get("switchAccount"), **kwargs)