import json
import jsonpath


class JsonOperation:

    @classmethod
    def load_json_file(cls, file_path) -> dict:
        '''
        从文件读取Json 文件
        :param file_path: json文件路径
        :return: 返回一个字段
        '''
        try:
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
                f.close()
        except FileNotFoundError as e:
            print("-------------No file found at path: " + file_path)
            data = None
        return data

    def get_api_form_postman_data(self, postman_data: list) -> dict:
        '''
        将postman 文件中读取来的list 转换为一个个的API定义字典.
        :param: postman_data
        :return:
        '''
        temp_dict = {}
        for index in range(len(postman_data)):
            temp_data = postman_data[index]
            if isinstance(temp_data, dict):
                if 'name' in temp_data.keys() and 'item' in temp_data.keys():
                    # 将 name的值作为key, item的值作为value 放入 temp_dict中.
                    if temp_data.get('name') in temp_dict.keys():
                        continue
                    else:
                        temp_dict[temp_data.get('name')] = self.get_api_form_postman_data(temp_data.get('item'))
                    # print(temp_dict)
                elif 'name' in temp_data.keys() and 'item' not in temp_data.keys():
                    api_define_dict = {}
                    request_data = self.get_dict_value(temp_data, 'request')
                    url_dict = self.get_dict_value(request_data, 'url')
                    url_path_list = self.get_dict_value(url_dict, 'path')
                    api_define_dict['end_point'] = '/' + url_path_list[-1]
                    api_define_dict['method'] = self.get_dict_value(request_data, 'method').lower()
                    api_define_dict['params'] = self.generate_params_dict(self.get_dict_value(url_dict, 'query'))
                    body_dict = self.get_dict_value(request_data, 'body')
                    get_json_request_body = self.get_dict_value(body_dict, 'raw')
                    try:
                        request_body_json = json.loads(get_json_request_body)
                        # print(request_body_json)
                        api_define_dict['json'] = request_body_json
                    except Exception as e:
                        api_define_dict['json'] = None
                    # temp_dict[temp_data.get('name')] = api_define_dict
                    if url_path_list[-1] in temp_dict:
                        continue
                    else:
                        temp_dict[url_path_list[-1]] = api_define_dict
                    # print(temp_dict)
        return temp_dict

    def get_dict_value(self, src_dict: dict, target_key):
        '''
        获取字典中key 对应的value
        :param src_dict:  字典
        :param target_key: key值
        :return: 如果有值就返回值, 如果没有就返回None
        '''
        try:
            result_value = src_dict.get(target_key)
        except Exception as e:
            # print('----------------No data found for target key: ' + target_key)
            result_value = None
        return result_value

    def generate_params_dict(self, param_list: list) -> dict:
        '''
        postman json 文件中 param 的存储形式为list [ dictionary,dictionary], dict 存储又为key, value 方式
        将之转换为 dictionary, 例如
        {
			"key": "persistentLoginType",
			"value": "rememberme"
		}
		转换为 persistentLoginType : rememberme
        :param param_list:
        :return:
        '''
        param_dict = {}
        if param_list is None:
            param_dict = None
        else:
            for index in range(len(param_list)):
                temp_data = param_list[index]
                param_dict[temp_data.get('key')] = temp_data.get('value')
        return param_dict

    def postman_data2_api(self, file_postman):
        '''
        暂时没用这个
        :param file_postman:
        :return:
        '''
        data_json = self.load_json_file(file_postman)
        item_data = data_json.get('item')
        # print(item_data[0]['name'])
        # print('---------------------item data finished')
        # temp_dict = item_data[0]
        # print(temp_dict.get('name'))
        data_finally = self.get_api_form_postman_data(item_data)
        return data_finally


if __name__ == "__main__":
    # postman_comp_file = r'D:\Installation\PycharmProjects\becn_project\configure_files\config_api\postman_export_files\Beacon-API-All_Reorder_For_APIgenerate.postman_collection.json'
    # postman_file = r'D:\AllWorkSpaces\Python\PycharmProjects\becn_project\configure_files\config_api\postman_export_files\Beacon-API-All_Reorder_For_APIgenerate.postman_collection.json'
    # print('this is test for check')
    # json_opr = JsonOperation()
    # final_data = json_opr.postman_data2_api(postman_comp_file)
    # print(json.dumps(final_data))
    json_data = "{\n    \"username\": \"${username}\",\n    \"password\": \"${password}\",\n    \"siteId\": \"homeSite\",\n    \"persistentLoginType\": \"rememberPassword\",\n    \"userAgent\": \"desktop\"\n}"
    print(type(json.dumps(json_data)))
    print(json.dumps(json_data))
    print('------------------------')
    print(type(json.loads(json_data)))
    print(json.loads(json_data))