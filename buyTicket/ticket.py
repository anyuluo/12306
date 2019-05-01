from common.get_config import get_config
from common.get_station import get_station_info
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
        self.from_data = data['start_date']
        self.trains = data['trains']
        seat_types = data['seat_type']
        self.passengers = data['passengers']
        self.seat_type = []
        # 座位类型所在td位置
        for seat_type in seat_types:
            seat = {}
            if seat_type == '商务座特等座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 1,
                    'seat_type_value': 9,
                }
            elif seat_type == '一等座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 2,
                    'seat_type_value': 'M',
                }
            elif seat_type == '二等座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 3,
                    'seat_type_value': 'O',
                }
            elif seat_type == '高级软卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 4,
                    'seat_type_value': 6,
                }
            elif seat_type == '软卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 5,
                    'seat_type_value': 4,
                }
            elif seat_type == '动卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 6,
                    'seat_type_value': 'F',
                }
            elif seat_type == '硬卧':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 7,
                    'seat_type_value': 3,
                }
            elif seat_type == '软座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 8,
                    'seat_type_value': 2,
                }
            elif seat_type == '硬座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 9,
                    'seat_type_value': 1,
                }
            elif seat_type == '无座':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 10,
                    'seat_type_value': 1,
                }
            elif seat_type == '其他':
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 11,
                    'seat_type_value': 1,
                }
            else:
                # 席别信息配置有误，系统将自动为您预定硬卧
                print('席别信息配置有误，系统将自动为您预定硬卧！')
                seat = {
                    'seat_type': seat_type,
                    'seat_type_index': 7,
                    'seat_type_value': 3,
                }
            self.seat_type.append(seat)

        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'  # 登录页面
        self.my_index_url = 'https://kyfw.12306.cn/otn/view/index.html'  # 登录成功页面
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'  # 购票首页
        self.reserve_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'  # 车票预定页面
        self.show_ticket_message_url = 'https://kyfw.12306.cn/otn//payOrder/init'  # 显示车票信息url

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

    def login(self):
        """  登录12306官网  """

        # 访问登录页面
        self.web_driver.get(self.login_url)
        time.sleep(1)  # 等待加载网页
        if self.account != '' and self.password != '':  # 账户密码不为空时自动填写
            self.web_driver.find_element_by_xpath('//ul/li[@class="login-hd-account"]/a').click()  # 模拟点击账号登录
            time.sleep(0.2)
            self.web_driver.find_element_by_id('J-userName').send_keys(self.account)  # 填写账户
            time.sleep(1)
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

    def search_ticket(self):
        """  查询车票  """

        # 访问查票页面
        search_ticket_url = self.ticket_url + '&fs={}&ts={}&date={}&flag=N,N,Y'.format(
            get_station_info(self.from_station),
            get_station_info(self.to_station),
            self.from_data)
        self.web_driver.get(search_ticket_url)
        time.sleep(2)  #
        # # 将出发地、到达地、出发日期等信息加载到cookie中
        # self.web_driver.add_cookie({'name': '_jc_save_fromStation', 'value': self.from_station})
        # self.web_driver.add_cookie({'name': '_jc_save_toStation', 'value': self.to_station})
        # self.web_driver.add_cookie({'name': '_jc_save_fromDate', 'value': self.from_data})

        print('开始查询车票。。。')
        count = 0  # 记录查询次数
        while True:
            try:
                count += 1
                print('正在进行第{}次查询。。。'.format(count))
                if self.ticket_url in self.web_driver.current_url:
                    self.web_driver.find_element_by_id('query_ticket').click()  # 点击查询车票
                else:
                    self.web_driver.get(search_ticket_url)  # 不在查询页面的情况
                time.sleep(1)

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
                            if train_tr.find_element_by_xpath('.//td[{}]'.format(seat['seat_type_index'])).text == '--':
                                print('当前车次：{} 暂无席别：{}'.format(train, seat['seat_type']))
                            elif train_tr.find_element_by_xpath(
                                    './/td[{}]'.format(seat['seat_type_index'])).text == '无':
                                print('当前车次：{} 席别：{} 无票， 正在为您检测其他席别或车次。。。'.format(train, seat['seat_type']))
                            else:
                                print('当前车次：{} 席别：{} 有票， 正在为您预定车票'.format(train, seat['seat_type']))
                                # 这里开始预定车票
                                train_tr.find_element_by_xpath('.//a[@class="btn72"]').click()
                                time.sleep(1)
                                self.reserve_ticket(seat)  # 开始预定车票

                    else:
                        print('未查询到当前车次：{}'.format(train))
                        # 删除无效车次
                        self.trains.remove(train)

            except Exception as e:
                print('出现异常情况，异常信息：', e)
                # 发生异常情况， 可能出现网络延迟或12306服务器压力过大导致页面加载时间过长
                # 遇到异常情况时等待1s后继续尝试
                time.sleep(1)

            # 所有车次无效时退出程序
            if not self.trains:
                print('很遗憾! 没有查询到您配置的任何车次， 请检查您的配置信息是否正确。')
                print('应用程序将在3秒后退出。。。')
                time.sleep(3)
                break
            # 订票成功
            if self.flag:
                break

    def reserve_ticket(self, seat):
        """  预定车票  """

        if self.web_driver.current_url == self.reserve_url:
            print('开始选择乘客。。。')
            num = 0  # 用于记录乘客序号
            for passenger in self.passengers:
                # 乘客序号 +1
                num += 1
                try:
                    self.web_driver.find_element_by_xpath(
                        '//label[contains(text(), "{}")]'.format(passenger['name'])).click()  # 选择乘客
                    time.sleep(0.1)
                    try:
                        # 处理确认的弹框信息
                        alert = self.web_driver.find_element_by_id('qd_closeDefaultWarningWindowDialog_id')
                        if alert:
                            alert.click()
                            time.sleep(0.1)
                    except Exception as e:
                        pass

                    # 选择票种
                    if passenger['ticket_type'] != '成人票':
                        self.web_driver.find_element_by_xpath(
                            '//select[@id="ticketType_{}"]/option[contains(text(),"{}")]'.format(num, passenger[
                                'ticket_type'])).click()
                        print('已经为乘客："{}"选择票种："{}"。。。'.format(passenger, passenger['ticket_type']))
                        # 处理温馨提示消息消息
                        self.web_driver.find_elements_by_xpath('//a[@class="btn92s"]')[-1].click()

                    # 选择席别
                    print('开始为乘客："{}"选择席别。。。'.format(passenger))
                    self.web_driver.find_element_by_xpath(
                        '//select[@id="seatType_{}"]/option[@value="{}"]'.format(num, seat['seat_type_value'])).click()
                    time.sleep(0.1)

                except Exception as e:
                    print('在选择乘客：{}时发生异常：'.format(passenger), e)
                    print('请确认您在12306官网是否录入“{}”乘客的相关信息。。。'.format(passenger))

            # 提交订单
            print('正在提交订单。。。')
            self.web_driver.find_element_by_id('submitOrder_id').click()
            time.sleep(0.5)
            # 确认提交订单
            qr_submit = self.web_driver.find_element_by_id('qr_submit_id')
            if qr_submit:
                qr_submit.click()
            else:
                print('提交失败！')
                return

            time.sleep(2)
            # 返回确认订单是否提交成功
            if self.show_ticket_message_url in self.web_driver.current_url:
                if self.web_driver.find_element_by_id('show_ticket_message'):
                    # 订单提交成功
                    self.flag = True
                else:
                    # 订单生成失败
                    return


if __name__ == '__main__':
    BuyTicket().login()
