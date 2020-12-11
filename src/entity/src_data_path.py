import os


class SrcDataPath:
    @classmethod
    def get_src_data_path(cls, data_relative_path: str) -> str:
        """
        传入相对路径, 获取绝对路径
        :param data_relative_path: 相对路径
        :return: 绝对路径
        """
        current_path = os.path.abspath(os.path.abspath(__file__))  # 当前文件的路径
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path))) # 获取项目的根目录
        print(project_path)
        # project_name = os.path.basename(project_path) # 获取项目的名字
        # root_path = current_path.split('test_demo')[0]  # 项目的root 路径
        # root_path = current_path.split(project_name)[0]
        # data_path = os.path.abspath(root_path + '/'+project_name+'/' + data_relative_path)  # 获取数据文件路径
        data_path = os.path.abspath(project_path + '/' + data_relative_path) # 获取数据文件路径
        return data_path


if __name__ == "__main__":
    apiPath = 'src/api/configure_files/config_api/api_definition/Beacon_Rest_Services_V1.yaml'
    pathh = SrcDataPath.get_src_data_path(apiPath)
    print(pathh)
