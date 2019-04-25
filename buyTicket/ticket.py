from common.getConfig import get_config
from selenium import webdriver
import time


class BuyTicket:
    """
        使用浏览器模拟用户登录购票
    """

    def __init__(self):
        data = get_config('info')  # 获取用户信息
        self.account = data['12306account']
        self.password = data['password']
        self.from_station = data['from_station']
        self.to_station = data['to_station']
        self.train_date = data['start_date']
        self.trains = data['trains']
        seat_types = data['seat_type']
        self.passengers = data['passengers']
        self.seat_type = []
        # 座位类型所在td位置
        for seat_type in seat_types:
            if seat_type == '商务座特等座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 1,
                    'seat_type_value': 9,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '一等座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 2,
                    'seat_type_value': 'M',
                }
                self.seat_type.append(seat)
            elif self.seat_type == '二等座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 3,
                    'seat_type_value': 'O',
                }
                self.seat_type.append(seat)
            elif self.seat_type == '高级软卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 4,
                    'seat_type_value': 6,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '软卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 5,
                    'seat_type_value': 4,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '动卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 6,
                    'seat_type_value': 'F',
                }
                self.seat_type.append(seat)
            elif self.seat_type == '硬卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 7,
                    'seat_type_value': 3,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '软座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 8,
                    'seat_type_value': 2,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '硬座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 9,
                    'seat_type_value': 1,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '无座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 10,
                    'seat_type_value': 1,
                }
                self.seat_type.append(seat)
            elif self.seat_type == '其他':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 11,
                    'seat_type_value': 1,
                }
                self.seat_type.append(seat)
            else:
                # 席别信息配置有误，系统将自动为您预定硬座
                print('席别信息配置有误，系统将自动为您预定硬座！')
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 7,
                    'seat_type_value': 3,
                }
                self.seat_type.append(seat)

        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'  # 登录页面
        self.my_index_url = 'https://kyfw.12306.cn/otn/view/index.html'  # 登录成功页面
        self.index_url = 'https://www.12306.cn/index/index.html'  # 购票首页
        self.reserve_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'  # 车票预定页面

        self.driver_info = get_config('driver')  # 获取驱动信息
        if self.driver_info['name'].lower() == 'chrome':
            self.web_driver = webdriver.Chrome(self.driver_info['path'])
        elif self.driver_info['name'].lower() == 'firefox':
            self.web_driver = webdriver.Firefox(self.driver_info['path'])
        elif self.driver_info['name'].lower() == 'edge':
            self.web_driver = webdriver.Edge(self.driver_info['path'])
        elif self.driver_info['name'].lower() == 'opera':
            self.web_driver = webdriver.Opera(self.driver_info['path'])
        elif self.driver_info['name'].lower() == 'safari':
            self.web_driver = webdriver.Safari(self.driver_info['path'])
        else:
            print('很遗憾！ 暂不支持您配置的浏览器，建议使用Google Chrome！')
            exit()  # 用户配置的浏览器不可用，直接退出程序
        self.flag = False  # 订票标记， 订票成功时设置为True

    '''  登录12306官网  '''

    def login(self):
        # 访问登录页面
        self.web_driver.get(self.login_url)
        time.sleep(1)  # 等待加载网页
        if self.account != '' and self.password != '':  # 账户密码不为空时自动填写
            self.web_driver.find_element_by_xpath('//ul/li[@class="login-hd-account"]/a').click()  # 模拟点击账号登录
            time.sleep(0.2)
            self.web_driver.find_element_by_id('J-userName').send_keys(self.account)  # 填写账户
            self.web_driver.find_element_by_id('J-password').send_keys(self.password)  # 填写密码

            print('请手动识别验证码！完成后请点击登录。如果登录失败，请扫码登录')
        else:
            print('您没有配置登录账户信息！建议您扫描二维码登录。')
        # 判断登录是否登录成功
        # 登录失败时返回登录
        while True:
            if self.web_driver.current_url == self.my_index_url:
                break
            else:
                time.sleep(1)
        # 登录成功，开始查询车票
        self.search_ticket()

    '''  查询车票  '''

    def search_ticket(self):
        # 访问查票页面
        self.web_driver.get(self.index_url)
        time.sleep(0.2)  #
        # 填写出发地、到达地、出发日期等信息
        self.web_driver.find_element_by_id('fromStationText').send_keys(self.from_station)
        self.web_driver.find_element_by_id('toStationText').send_keys(self.to_station)
        self.web_driver.find_element_by_id('train_date').send_keys(self.train_date)

        # 模拟点击查询
        self.web_driver.find_element_by_id('search_one').click()
        time.sleep(1)  # 等待页面加载
        print('开始查询车票。。。')
        self.check_ticket()

    '''  检查是否有余票  '''

    def check_ticket(self):
        count = 0  # 记录查询次数
        while True:
            count += 1
            print('正在进行第{}次查询。。。'.format(count))
            try:
                for train in self.trains:
                    print('开始查询车次：{}'.format(train))
                    # preceding-sibling：选取当前节点之前的所有某同级节点
                    # preceding-sibling::tr 这里是从当前节点向前查找所有同级tr节点，所以上一个tr节点的索引为1
                    train_tr = self.web_driver.find_element_by_xpath(
                        '//tr[@datatran="' + train + '"]/preceding-sibling::tr[1]')
                    if train_tr:
                        # 查询到车次， 开始检测余票
                        for seat in self.seat_type:
                            # 依次查看用户配置的系别是否有票
                            if train_tr.find_element_by_tag_name('td')[seat['seat_type_index']].text == '--':
                                print('当前车次：{} 暂无席别：{}'.format(train, seat))
                            elif train_tr.find_element_by_tag_name('td')[seat['seat_type_index']].text == '无':
                                print('当前车次：{} 席别：{} 无票， 正在为您检测其他席别或车次。。。'.format(train, seat))
                            else:
                                print('当前车次：{} 席别：{} 有票， 正在为您预定车票'.format(train, seat))
                                # 这里开始预定车票
                                train_tr.find_element_by_xpath('.//a[@class="btn72"]').click()
                                time.sleep(0.8)
                                self.reserve_ticket()  # 开始预定车票

                    else:
                        print('未查询到当前车次：{}'.format(train))
                        # 删除无效车次
                        self.trains.remove(train)

            except Exception as e:
                print('出现异常情况，异常信息：', e)

            # 所有车次无效时退出程序
            if not self.trains:
                print('很遗憾! 没有查询到您配置的任何车次， 请检查您的配置信息是否正确。')
                print('应用程序将在3秒后退出。。。')
                time.sleep(3)
                break
            # 订票成功
            if self.flag:
                break

    '''  预定车票  '''

    def reserve_ticket(self):
        if self.web_driver.current_url == self.reserve_url:
            print('开始选择乘客。。。')
            for passenger in self.passengers:
                try:
                    self.web_driver.find_element_by_xpath('//label[contains(text(), "{}")]'.format(passenger['name'])).click()  # 选择乘客

                except Exception as e:
                    print('在选择乘客：{}时发生异常：'.format(passenger), e)
                    print('请确认您在12306官网是否录入“{}”乘客的相关信息。。。'.format(passenger))


if __name__ == '__main__':
    BuyTicket().login()
