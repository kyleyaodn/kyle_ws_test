from kyle_ws_test.src.entity.json_operation import JsonOperation
from kyle_ws_test.src.entity.yaml_operation import YamlOperation


class postman2Case:
    def __init__(self):
        self.jsonOpr = JsonOperation()
        self.yamlOpr = YamlOperation()

    def postman_data2_api(self, file_postman):
        '''
        读取postman 文件
        :param file_postman: postman 文件地址
        :return: 返回一个包含API定义的词典
        '''
        data_json = self.jsonOpr.load_json_file(file_postman)
        item_data = data_json.get('item')
        # print(item_data[0]['name'])
        # print('---------------------item data finished')
        # temp_dict = item_data[0]
        # print(temp_dict.get('name'))
        data_finally = self.jsonOpr.get_api_form_postman_data(item_data)
        return data_finally

    def write_to_yaml_file(self, location_path: str, src_data: dict):
        '''
        将读取出来的postman 数据读取, 然后按每一个key的value生成对应的yaml文件
        :param location_path: 文件存放地址
        :param src_data: 源数据
        :return:
        '''
        file_name = ''
        for key in src_data.keys():
            file_name = key
            file_path = location_path + '\\' + file_name + '.yaml'
            self.yamlOpr.conver_data_2_yaml_file(file_path, src_data.get(key))


if __name__ == "__main__":
    postmanCase = postman2Case()
    folder_path = r'D:\AllWorkSpaces\Python\PycharmProjects\becn_project\kyle_ws_test\configure_files\config_api\api_definition'
    postman_file = r'D:\AllWorkSpaces\Python\PycharmProjects\becn_project\kyle_ws_test\configure_files\config_api\postman_export_files\Beacon-API-All_Reorder_For_APIgenerate.postman_collection.json'
    src_data = postmanCase.postman_data2_api(postman_file)
    postmanCase.write_to_yaml_file(folder_path, src_data)
