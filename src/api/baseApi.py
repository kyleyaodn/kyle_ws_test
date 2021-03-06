import yaml
import requests
import json
from requests import Response
from src.entity.yaml_operation import YamlOperation
from src.entity.src_data_path import SrcDataPath
from src.entity.json_schema_operation import JsonSchemeOperation
from src.entity.json_operation import JsonOperation
from src.entity.commen_tools import CommonTools


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
    common_tools = CommonTools()
    req = {}
    resp = None
    """
    this class contains the base method of APIs
    """

    @classmethod
    def format_response(cls, resp):
        cls.resp = resp
        print('response data is as following:')
        print(json.dumps(json.loads(cls.resp.text, encoding='utf-8'), ensure_ascii=True))
        # print(resp.json())

    @classmethod
    def format_parameter(cls, params):
        cls.params = params
        print(cls.params)

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
        print('will send request as following: ')
        print(self.req)
        # 获取case的case api version.
        # if 'case_api_version' in kwargs.keys():
        #     self.case_api_version = kwargs.get('case_api_version')
        if self.case_api_version == 'V1':
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

    def validate_json_schema(self, type_4_resp, api_define=None, resp=None):
        """
        校验Response的Json格式正确不, 使用json schema
        :param type_4_resp: 传入期望的json schema路径, schema_path_success, schemea_path_failed 目前为两种
        :param api_define: api 的定义
        :param resp: 传入response, 如果没有就取类变量
        :return:
        """
        if api_define is None:
            print('no api define so use the value from request')
            api_define = self.req
        if resp is None:
            resp = self.resp
        resp_json_data = resp.json()
        try:
            schema_file_path = api_define['json_schema'].get(type_4_resp)
            print('validate the type for Json Schema: ' + type_4_resp)
            # 断言jsonschema 是否正确
            assert JsonSchemeOperation.check_json_schema(resp_json_data, schema_file_path)
        except KeyError as key_error:
            print(key_error)

    def response_json_schema_check(self, api_define=None, resp=None):
        """
        为response 做json schema 的校验.
        :param api_define: api 定义字典, 从中取得json schema 文件的位置.
        :param resp: 接口返回的数据. 不传则直接取类变量中存储的response
        :return: 无返回, 直接断言校验结果是否为True.
        """
        if api_define is None:
            api_define = self.req
        if resp is None:
            resp = self.resp
        resp_json = resp.json()
        schema_file = api_define['json_schema']
        result = False
        if isinstance(schema_file, dict):
            for key in schema_file.keys():
                file_path = schema_file.get(key)
                if file_path is "":
                    print('No schema defined for: ' + key)
                    result = True
                else:
                    print('validate the type for Json Schema: ' + key)
                    print(file_path)
                    result = JsonSchemeOperation.check_json_schema(resp_json, file_path)
                    if result is True:
                        break
        assert result

    def validate_json_path(self, json_path, compare_condition, expect_value, resp=None) -> bool:
        """
        根据提供的json_path 获取response 中的数据, expect_value 对比
        :param json_path: 已知想要查找数据的json_path
        :param compare_condition: 对比条件
        :param expect_value: 预期结果.
        :param resp 接口的返回response
        :return: compare_result 符合预期返回 true, 不符合返回 false
        """
        compare_result = False
        if resp is None:
            resp = self.resp
            print(resp.json())
        result_list = self.jsonOpr.json_path_data(resp.json(), json_path)
        print('**********************************result list?')
        print(result_list)
        if compare_condition == "value_equals":
            for index in range(len(result_list)):
                if result_list[index].lower() == expect_value.lower():
                    compare_result = True
                else:
                    compare_result = False
                    break
        elif compare_condition == 'length_large':
            if len(result_list) > int(expect_value):
                compare_result = True
        elif compare_condition == 'value_contains':
            for index in range(len(result_list)):
                if expect_value.lower() in result_list[index].lower():
                    compare_result = True
                    break
                else:
                    compare_result = False
        return compare_result

    def str_to_dict(self, target_data) -> dict:
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

    def run_steps(self, test_cases, **kwargs):
        self.case_api_version = test_cases.get('run_type')
        case_steps = test_cases.get('test_steps')
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
                            print('set request param from test data:')
                            print(step.get('request_param'))
                            data_req_param = step.get('request_param')
                            data_param_after_replace = self.common_tools.replace_value(data_req_param, self.params)
                            self.req.setdefault('params', self.str_to_dict(data_param_after_replace))
                    if 'request_body' in step.keys():
                        if step.get('request_body') is not None:
                            print('set request body from test data: \n' + step.get('request_body'))
                            self.req.setdefault('json', self.str_to_dict(step.get('request_body')))
                    if 'method' in step.keys():
                        method = step['method'].split('.')[-1]
                        getattr(self, method)(**kwargs)
                        self.base_assertion()
                        self.response_json_schema_check()
                    if 'check_point' in step.keys():
                        self.exec_checkpoints(step.get('check_point'))
                    if 'extract' in step.keys():
                        extract_data = step.get('extract')
                        self.set_extract_data(extract_data)

                else:
                    print('the step definition is incorrect, should be dict')

    def exec_checkpoints(self, checkpoint, resp=None):
        result = True
        if resp is None:
            resp = self.resp
            print('***************exec_checkpoints')
            print(resp.json())
        if isinstance(checkpoint, list):
            for index in range(len(checkpoint)):
                checker_dict = checkpoint[index]
                print('start checking data with: path, condition, expect value is:')
                print(checker_dict.get('path'))
                print(checker_dict.get('condition'))
                # print(checker_dict.get('expect_value'))
                result = self.validate_json_path(checker_dict.get('path'), checker_dict.get('condition'),
                                                 checker_dict.get('expect_value'))
                if result is False:
                    print('Failed validate value for path: ' + checker_dict.get('path'))
                    print('Expect value is: ' + checker_dict.get('expect_value'))
                    print('Actually result is: ')
                    print(resp.json())
                    break
        assert result

    def set_extract_data(self, extract_list, resp=None):
        if resp is None:
            resp = self.resp
        if isinstance(extract_list, list):
            if len(extract_list) > 0:
                for index in range(len(extract_list)):
                    extract = extract_list[index]
                    param_value = self.jsonOpr.json_path_data(resp.json(), extract.get('path'))
                    param_key = extract.get('variable_name')
                    print('set the out put value for key is: \n' + "key is: ")
                    print(param_key)
                    print('value is: ')
                    print(param_value)
                    self.params.setdefault(param_key, param_value[0])
                    self.format_parameter(self.params)
