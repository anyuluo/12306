import os
"""
  读取站点信息
"""


def get_station_info(station):
    f = open(os.path.join(os.path.dirname(__file__)) + '/station.txt', 'r', encoding='utf8')  # 打开12306站点信息文件
    stations = f.read()
    f.close()  # 关闭文件对象
    station_list = stations.split('|')
    for index in range(1, len(station_list), 5):
        if station_list[index] == station:
            return station + ',' + station_list[index + 1]


if __name__ == '__main__':
    print(get_station_info('北京'))
    # print('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&' + 'fs={}&ts={}&date={}&flag=N,N,Y'.format(get_station_info('北京'),
    #                                                             get_station_info('上海'),
    #                                                             '2019-05-02'))
