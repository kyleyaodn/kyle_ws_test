import yaml
from ruamel import yaml as ruyaml


class YamlOperation:

    def load_yaml_file(self, file_path):
        '''
        读取yaml 文件返回数据
        :param file_path: 文件的路径
        :return: yaml load 的数据
        '''
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                file_data = f.read()
                f.close()
        except FileNotFoundError as e:
            print('------------No file found at path: ' + file_path)
        return yaml.safe_load(file_data)

    def conver_data_2_yaml_file(self, file_name, src_data):
        '''
        将数据写成Yaml 文件
        :param file_name: 文件名
        :param src_data: 词典数据
        :return:
        '''
        try:
            with open(file_name, 'w', encoding="utf-8") as f:
                ruyaml.dump(src_data, f, Dumper=ruyaml.RoundTripDumper)
                f.close()
        except FileNotFoundError as e:
            print('got error when writing file' + e)
