import yaml
import requests
import json
from requests import Response
from src.entity.yaml_operation import YamlOperation
from src.entity.src_data_path import SrcDataPath
from src.entity.json_schema_operation import JsonSchemeOperation
from src.entity.json_operation import JsonOperation


class BaseAPI:
    env_relative_path = 'src/api/configure_files/config_env.yaml'
    env_data = None
    params = {}
    cookies_param = None
    api_version = None
    case_api_version = None
    new_session = requests.Session()
    yamlOpr = YamlOperation()
    jsonOpr = JsonOperation()
    req = {}
    resp = None
    """
    this class contains the base method of APIs
    """

    @classmethod
    def format_response(cls, resp):
        cls.resp = resp
        # print(json.dumps(json.loads(cls.resp.text, encoding='utf-8'), ensure_ascii=True))
        print(resp.json())

    def set_req(self, req):
        for key in req:
            if key in self.req:
                print("The following key is already in req, do not set value again: " + key)
            else:
                self.req[key] = req[key]

    def load_api(self, file_relative_path: str) -> dict:
        """
        读取yaml 文件中关于API的定义
        :param file_relative_path: API 定义yaml文件路径
        :return: 读取出来的字典
        """
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
        print('set request url as: \n' + api_path)
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
        """
        调用request 发送request
        :param req: 组成一个request的各种元素, endpoint, json, parameters...
        :return: 返回一个response
        """
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
        """
        发送request
        :param req: 传入request 需要的 method, header, request body, parameters 组装好request.
        :param kwargs: 一些其他的参数, 例如 verifiy, case_api_version
        :return: response
        """
        # 初始化类变量: request
        self.set_req(req)
        if 'data_params' in kwargs.keys():
            # 使用测试数据中的param
            self.req['params'] = self.str_to_dict(kwargs.get('data_params'))
        if 'data_json' in kwargs.keys():
            # 使用测试数据中的json
            self.req['json'] = self.str_to_dict(kwargs.get('data_json'))
        self.req = self.generate_request(self.req)
        # 获取env的数据
        self.load_env()
        # 组合获取API的详细路径
        api_path = self.generate_api_path(self.req)
        # 获取case的case api version.
        if 'case_api_version' in kwargs.keys():
            self.case_api_version = kwargs.get('case_api_version')
        if self.case_api_version == 'v1':
            print('case is run for cookie')
            resp = self.new_session.request(
                method=self.req.get('method'),
                url=api_path,
                params=self.req.get('params'),
                json=self.req.get('json'),
                verify=self.env_data.get('ssl_check'))
        else:
            print('case is run for Oauth')
            resp = requests.request(
                method=self.req.get('method'),
                url=api_path,
                params=self.req.get('params'),
                json=self.req.get('json'),
                verify=self.env_data.get('ssl_check'))
        self.format_response(resp)
        self.case_api_version = None
        return resp

    def base_assertion(self, resp=None):
        """
        检查response的status code
        :param resp:
        :return:
        """
        if resp is None:
            resp = self.resp
        assert resp.status_code == 200

    @classmethod
    def validate_json_schema(cls, type_4_resp, api_define=None, resp=None):
        """
        校验Response的Json格式正确不, 使用json schema
        :param type_4_resp: 传入期望的json schema路径, schema_path_success, schemea_path_failed 目前为两种
        :param api_define: api 的定义
        :param resp: 传入response, 如果没有就取类变量
        :return:
        """
        if api_define is None:
            print('no api define so use the value from request')
            api_define = cls.req
        if resp is None:
            resp = cls.resp
        resp_json_data = resp.json()
        try:
            schema_file_path = api_define['json_schema'].get(type_4_resp)
            print('validate the type for Json Schema: ' + type_4_resp)
            # 断言jsonschema 是否正确
            assert JsonSchemeOperation.check_json_schema(resp_json_data, schema_file_path)
        except KeyError as key_error:
            print(key_error)

    @classmethod
    def validate_json_path(cls, json_path, compare_condition, except_value, resp=None) -> bool:
        """
        根据提供的json_path 获取response 中的数据, 和except_value 对比
        :param json_path: 已知想要查找数据的json_path
        :param compare_condition: 对比条件
        :param except_value: 预期结果.
        :param resp 接口的返回response
        :return: compare_result 符合预期返回 true, 不符合返回 false
        """
        compare_result = False
        if resp in None:
            resp = cls.resp
        result_list = cls.jsonOpr.json_path_data(resp, json_path)
        if compare_condition == "value_equals":
            for index in range(len(result_list)):
                if result_list[index] == except_value:
                    compare_result = True
                else:
                    compare_result = False
                    break
        elif compare_condition == 'length_large':
            if len(result_list) > int(except_value):
                compare_result = True
        elif compare_condition == 'value_contains':
            for index in range(len(result_list)):
                if except_value in result_list[index]:
                    compare_result = True
                else:
                    compare_result = False
                    break
        return compare_result

    @staticmethod
    def str_to_dict(target_data) -> dict:
        """
        字符串里面存储的是Json 格式的数据, 将字符串读取为字典
        :param target_data:
        :return:
        """
        out_data = None
        if isinstance(target_data, str):
            try:
                out_data = json.loads(target_data)
            except json.decoder.JSONDecodeError as decode_error:
                print(decode_error)
        elif isinstance(target_data, dict):
            out_data = target_data
        else:
            print('the data type is incorrect should be str or dict')
            print(type(target_data))
        return out_data

    def run_steps(self, case_steps: list, **kwargs):
        print(case_steps)
        if isinstance(case_steps, list):
            for index in range(len(case_steps)):
                step = case_steps[index]
                print('run case with step: ')
                print(step)
                self.req.clear()  # 清空req的数据, 为下一次request 数据做准备
                if isinstance(step, dict):
                    if 'request_param' in step.keys():
                        if step.get('request_param') is not None:
                            print('set request param from test data: \n' + step.get('request_param'))
                            self.req.setdefault('params', self.str_to_dict(step.get('request_param')))
                    if 'request_body' in step.keys():
                        if step.get('request_body') is not None:
                            print('set request body from test data: \n' + step.get('request_body'))
                            self.req.setdefault('json', self.str_to_dict(step.get('request_body')))
                    if 'method' in step.keys():
                        method = step['method'].split('.')[-1]
                        getattr(self, method)(**kwargs)
                else:
                    print('the step definition is incorrect, should be dict')
