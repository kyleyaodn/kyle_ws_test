from src.api.baseApi import BaseAPI


class MyAccountSercice(BaseAPI):
    api_relative_Path = 'src/api/configure_files/config_api/api_definition/Beacon_Rest_Services_V1.yaml'

    '''
    This is My Account Services APIs
    '''

    def __init__(self):
        self.data = self.load_api(self.api_relative_Path)
        self.api_version = 'v1'
        self.params = {}

    def login(self, username, password, **kwargs):
        self.params.clear()
        self.params['username'] = username
        self.params['password'] = password
        return self.send_requests(self.data.get("My_Account_Services").get("login"), **kwargs)

    def logout(self):
        return self.send_requests(self.data.get("My_Account_Services").get("logout"))

    def getLoginDeclaration(self):
        return self.send_requests(self.data.get("My_Account_Services").get("getLoginDeclaration"))

    def getCurrentUserInfo(self):
        return self.send_requests(self.data.get("My_Account_Services").get("getCurrentUserInfo"))

    def accounts(self, profileId):
        self.params.clear()
        self.params['profileId'] = profileId
        # print(self.params)
        return self.send_requests(self.data.get("My_Account_Services").get("accounts"))

    def switchAccount(self, accountId):
        self.params.clear()
        self.params['accountId'] = accountId
        # print(self.params)
        return self.send_requests(self.data.get("My_Account_Services").get("switchAccount"))
