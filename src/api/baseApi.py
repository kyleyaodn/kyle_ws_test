import yaml
import requests
import json
from requests import Response
from src.entity.yaml_operation import YamlOperation
from src.entity.src_data_path import SrcDataPath


class BaseAPI:
    env_relative_path = 'src/api/configure_files/config_env.yaml'
    env_data = None
    params = {}
    cookies_param = None
    api_version = None
    case_api_version = None
    new_session = requests.Session()
    yamlOpr = YamlOperation()
    '''
    this class contains the base method of APIs
    '''

    @classmethod
    def format_response(cls, resp):
        cls.resp = resp
        print(json.dumps(json.loads(resp.text, encoding='utf-8'), ensure_ascii=True))

    def load_api(self, file_relative_path: str) -> dict:
        '''
        读取yaml 文件中关于API的定义
        :param file_path: API 定义yaml文件路径
        :return: 读取出来的字典
        '''
        file_path = SrcDataPath.get_src_data_path(file_relative_path)
        api_data = self.yamlOpr.load_yaml_file(file_path)
        return api_data

    def load_env(self):
        """
        读取env 数据
        """
        if self.env_data is None:
            # 如果Env 为空, 则调用env 取得env 数据
            print("Env is not load, loading env data")
            env_path = SrcDataPath.get_src_data_path(self.env_relative_path)
            self.env_data = self.yamlOpr.load_yaml_file(env_path)
        else:
            print("Already loads env data.")

    def generate_api_path(self, req) -> str:
        api_path = ""
        path = ""
        if self.api_version == 'v1':
            path = self.env_data.get('apiPath').get("v1_path")
            print("-----------Set V1 path for api")
        elif self.api_version == 'v2':
            path = self.env_data.get('apiPath').get("v2_path")
            print("-----------Set V1 path for api")
        elif self.api_version == 'v3':
            path = self.env_data.get('apiPath').get("v3_path")
            print("-----------Set V1 path for api")
        else:
            path = ""
            print("-----------Empty ")
        api_path = self.env_data.get('siteURL') + path + req.get("end_point")
        return api_path

    def send_request(self, req: dict) -> Response:
        # print("frist params ansd req")
        # print(self.params)
        # print(req)
        # 获取env的数据
        self.load_env()
        # 组合获取API的详细路径
        api_path = self.generate_api_path(req)
        print(api_path)
        # 将yaml格式数据转换成string
        raw = yaml.dump(req)
        print(type(raw))
        for key, value in self.params.items():
            # 替换yaml文件中${key} 样式的字段: username: ${username}
            # 例如test case 传入 email -> username
            # API中: self.params['username'] = username
            raw = raw.replace(f'${{{key}}}', repr(value))
            # print("replace")

        # print(raw)
        # 将Str 转换为 Dict
        req = yaml.safe_load(raw)
        # print(req)
        # print(type(req.get('json')))
        # # print(req.get('json'))
        # if self.cookies_param is not None:
        #     print("-----------------------Cookies has values")
        # else:
        #     print('______No value for cookies')
        resp = requests.request(
            method=req.get("method"),
            url=api_path,
            params=req.get('params'),
            json=req.get('json'),
            cookies=self.cookies_param
        )
        # print(resp.status_code)
        # print(resp.json())
        if self.cookies_param is None:
            print('Cookie is None, set value')
            self.cookies_param = resp.cookies
        else:
            print('Cookie is not None, no need set.')
        return resp

    def generate_request(self, req: dict):
        '''
        调用request 发送request
        :param req: 组成一个request的各种元素, endpoint, json, parameters...
        :return: 返回一个response
        '''
        # 将yaml格式数据转换成string
        raw = yaml.dump(req)
        for key, value in self.params.items():
            # 替换yaml文件中${key} 样式的字段: username: ${username}
            # 例如test case 传入 email -> username
            # API中: self.params['username'] = username
            raw = raw.replace(f'${{{key}}}', repr(value))
        # 将Str 转换为 Dict
        req = yaml.safe_load(raw)
        return req

    def send_requests(self, req: dict, **kwargs) -> Response:
        '''
        发送request
        :param req: 传入request 需要的 method, header, request body, parameters 组装好request.
        :param kwargs: 一些其他的参数, 例如 verifiy, case_api_version
        :return: response
        '''
        req = self.generate_request(req)
        # 获取env的数据
        self.load_env()
        # 组合获取API的详细路径
        api_path = self.generate_api_path(req)
        # 获取case的case api version.
        if 'case_api_version' in kwargs.keys():
            self.case_api_version = kwargs.get('case_api_version')
        # print(case_api_version)
        if self.case_api_version == 'v1':
            print('case is run for cookie')
            resp = self.new_session.request(
                method=req.get('method'),
                url=api_path,
                params=req.get('params'),
                json=req.get('json'),
                verify=False)
        else:
            print('case is run for Oauth')
            resp = requests.request(
                method=req.get('method'),
                url=api_path,
                params=req.get('params'),
                json=req.get('json'),
                verify=False)
        self.format_response(resp)
        self.case_api_version = None
        return resp

    def base_assertion(self, resp=None):
        if (resp is None):
            resp = self.resp
        assert resp.status_code == 200
        pass
