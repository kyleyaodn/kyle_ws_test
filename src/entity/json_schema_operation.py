from src.entity.src_data_path import SrcDataPath
from src.entity.read_file import ReadFile
from jsonschema import validate
from jsonschema import exceptions
import json


class JsonSchemeOperation:

    @classmethod
    def check_json_schema(cls, src_json, schema_path):
        '''
        校验Response的Json 的JsonSchema
        校验的两个值必须为字典类型的.
        :param src_json: 被校验的response的Json
        :param schema_path: Json Schema文件路径
        :return:
        '''
        obs_path = SrcDataPath.get_src_data_path(schema_path)
        json_schema_data = ReadFile.read_file(obs_path)
        try:
            validate(json.loads(src_json), json.loads(json_schema_data))
        except TypeError as type_error:
            print(type_error)
        except exceptions.ValidationError as validate_error:
            # 校验json的格式, 输出错误内容, 这个错误好像一次只能输出一处错误地方.
            print(validate_error.message)
            print(validate_error.absolute_schema_path)


if __name__ == "__main__":
    relative_path = 'src/api/configure_files/config_api/api_schemas/v1_apis/my_account_services/schema_success_login.json'
    resp_json = '{"messageInfo":{"firstName": "API Change","lastName":"API test","emailAddress":3,"cartLineItems":3,"internalUser":false,"lastSelectedAccount":{"accountName":"KEVIN KIRSCH NEW HOMES INC","accountLegacyId":"280381","accountViewPrices":true,"accountEnabled":true},"profileId":"user23820022","userType":"Customer","accountBranch":{"address":{"country":null,"address3":null,"address2":"4795 FOREST ST.","city":"DENVER","address1":"ROOF DEPOT MOUNTAIN","postalCode":"80216","state":"CO"},"branchNumber":"180","branchPhone":"3033886493","branchName":"DENVER BRANCH","branchRegionId":"33"}}}'
    new_resp_json = json.loads(resp_json)
    # JsonSchemeOperation.check_json_schema(resp_json, relative_path)
    type(JsonSchemeOperation.check_json_schema(resp_json, relative_path))
    print('***********')
