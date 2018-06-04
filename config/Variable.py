"""
    变量配置类
"""
# -*- coding:utf-8 -*-
WEBDRIVER_PATH_WINDOWS = "config/driver/chromedriver.exe"
WEBDRIVER_PATH_LINUX = "config/driver/chromedriver"

#测试用例json列表
TESTSUITE_WEB = ["cases/web/baidu_search.json"]
TESTSUITE_APP = ['cases/app/live_index.json']

MAILINFO = {
    "sender": 'sender@163.com',
    "receiver": ["receiver@163.com"],
    "subject": 'UI自动化测试报告',
    "username": 'sender@163.com',
    "password": 'password'
}

UT_REPORT_NAME = "webui-report.html"
UT_EXCEPTION_INFO_FILE = "exception_info.html"
QM_REPORT_PATH = "/srv/qm/cmfx/data/webuireport/"
QM_REPORT_PATH_PREFIX = "/srv/qm/cmfx/"

QM_SINGLE_RES_PATH = '/srv/qm/cmfx/data/webuireport/singletc/'

DB = {'host': 'localhost', 'port': 3306, 'user': 'root', 'passwd': '', 'db': 'techcms',
      'charset': 'utf8'}

UI_TEST_PLATFORM_DOMAIN = "domain.com"

SITE_DATA_PATH = "http://" + UI_TEST_PLATFORM_DOMAIN + "/"


ANDROID_SETTING = {'platformName': 'Android', 'platformVersion': '7.1.1', 'deviceName': '192.168.250.101:5555',
                   'appPackage': 'com.android.calculator2', 'appActivity': '.Calculator',
                   'driver_url': 'http://localhost:4723/wd/hub'}
WEB_HOSTS = {}
