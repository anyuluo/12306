# 12306抢票程序
基于Selenium的12306自动抢票脚本
## 适用对象
- 有一定的python基础，了解yaml语法，了解爬虫的python初学者
- 具有xpath开发经验，或熟悉正则表达式
- 熟悉HTTP库requests、自动化测试框架Selenium
## 技术栈
- python3.x
- 自动化测试技术、自动化测试工具Selenium
- 爬虫技术xpath、正则表达式、requests
## 使用方法
1. 下载源码，配置项目运行环境：**python3 + Selenium**
2. 安装requirements.txt依赖：**pip install -r requirements.txt**
3. 下载浏览器驱动，并根据浏览器驱动保存位置配置config.yaml中浏览器相关路劲、名称
4. 配置config.yaml中用户相关信息，驱动信息（driver）、用户相关信息（info）、邮箱相关信息（email）
## 更新日志
- 2019-04-25 创建项目
- 2019-04-28 完成项目主体功能开发
- 2019-05-15 添加站点实时更新功能，添加未完成订单检测功能，处理UBG（订票成功不能正常发送邮件），优化订票成功检测方法
