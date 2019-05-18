
"""
  获取站点信息
"""
import requests


class Station:
    """  站点类方法，用于在所有站点信息中获取指定的站点信息
         通过向12306请求获取最新的站点信息以达到实时更新站点信息的目的
    """

    # 初始化站点信息为空
    stations_name = ''
    # 12306站点信息链接
    station_name_url = 'https://www.12306.cn/index/script/core/common/station_name_v10028.js'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }

    @staticmethod
    def get_station_info(station_name):
        """  根据用户提供的站点名称获取相应的站点给信息  """
        if Station.stations_name == '':
            Station.update_stations()
            print('小的获取站点信息去啦！请稍等。')

        station_list = Station.stations_name.split('|')
        for index in range(1, len(station_list), 5):
            if station_list[index] == station_name:
                return station_name + ',' + station_list[index + 1]



    @staticmethod
    def update_stations():
        """  更新站点信息  """
        res = requests.get(Station.station_name_url, headers=Station.headers)
        Station.stations_name = res.text.strip('var station_names =\';')


if __name__ == '__main__':
    print(Station.get_station_info('西昌'))
    print(Station.get_station_info('成都'))





import os
'''  原始方法，将站点信息放到station.txt文件中，不具备实时更新功能'''

# 从station.txt文件中读取站点信息，不具备实时更新站点信息功能，不在推荐使用
# def get_station_info(station):
#     f = open(os.path.join(os.path.dirname(__file__)) + '/station.txt', 'r', encoding='utf8')  # 打开12306站点信息文件
#     stations = f.read()
#     f.close()  # 关闭文件对象
#     station_list = stations.split('|')
#     for index in range(1, len(station_list), 5):
#         if station_list[index] == station:
#             return station + ',' + station_list[index + 1]
