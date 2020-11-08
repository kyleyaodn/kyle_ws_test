class CommonTools:

    @classmethod
    def replace_value(cls, src_value: str, replace_dict: dict) -> str:
        """
        一个简单的替换字符串中特定字符的方法
        :param src_value:
        :param replace_dict:
        :return: src_value 替换后的src_value
        """
        for key, value in replace_dict.items():
            src_value = src_value.replace(f'${{{key}}}', value)
        return src_value
