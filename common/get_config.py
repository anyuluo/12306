import yaml
import os


def get_config(key):
    """
    解析yaml读取用户配置信息
    :param key: 信息key
    :return: data
    """
    f = open(os.path.join(os.path.dirname(os.path.dirname(__file__))) + '/config.yaml', encoding='utf8')
    data = yaml.load(f)[key]
    f.close()  # 记得关闭文件对象
    return data


# if __name__ == '__main__':
#     for passenger in get_config('info')['passengers']:
#         print(passenger['name'])
#         print(passenger['ticket_type'])
print(get_config('email'))
