# -*- coding: utf-8 -*-
import json
import platform
import unittest
from functools import wraps

from selenium.webdriver.chrome.options import Options
import cases.BaseFunctions
from config.Variable import *
from config import Variable
from utils.TestRunner import HTMLTestRunner
from browsermobproxy import Server


class BaseCase(unittest.TestCase):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1425x744')
    prefs = {"profile.default_content_setting_values.plugins": 1,
             "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
             "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
             "credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--ignore-certificate-errors')
    sysstr = platform.system()
    if (sysstr == "Windows"):
        webdriver_path = WEBDRIVER_PATH_WINDOWS
    else:
        webdriver_path = WEBDRIVER_PATH_LINUX

    desired_caps = {}
    desired_caps['platformName'] = Variable.ANDROID_SETTING['platformName']
    desired_caps['platformVersion'] = Variable.ANDROID_SETTING['platformVersion']
    desired_caps['deviceName'] = Variable.ANDROID_SETTING['deviceName']
    desired_caps['appPackage'] = Variable.ANDROID_SETTING['appPackage']
    desired_caps['appActivity'] = Variable.ANDROID_SETTING['appActivity']
    desired_caps['automationName'] = "uiautomator2"

    server = None
    proxy = None

    def __init__(self, *args, **kwargs):
        self.tc = kwargs.pop('tc', {})
        self.screenshot_path = kwargs.pop('screenshot_path', '')
        self.test_type = kwargs.pop('test_type', '')
        self.project_id = kwargs.pop('project_id', '')
        super(BaseCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.driver = None
        if (len(cls.ts_setup) != 0):
            if (cls.test_type == 'web'):
                from selenium import webdriver
                if (len(Variable.WEB_HOSTS) != 0):
                    cls.server = Server("/srv/browsermob-proxy-2.1.4/bin/browsermob-proxy")
                    cls.server.start()
                    cls.proxy = cls.server.create_proxy()
                    cls.proxy.clear_dns_cache()
                    cls.proxy.remap_hosts(hostmap=Variable.WEB_HOSTS)
                    cls.chrome_options.add_argument('--proxy-server={0}'.format(cls.proxy.proxy))
                cls.driver = webdriver.Chrome(chrome_options=cls.chrome_options, executable_path=cls.webdriver_path)
            elif (cls.test_type == 'app'):
                from appium import webdriver
                cls.driver = webdriver.Remote(Variable.ANDROID_SETTING['driver_url'], cls.desired_caps)

            cases.BaseFunctions.execute_step(cls, cls.ts_setup)

    def setUp(self):
        if (self.__class__.driver == None):
            if (self.test_type == 'web'):
                from selenium import webdriver
                if (self.__class__.proxy != None):
                    self.__class__.chrome_options.add_argument('--proxy-server={0}'.format(self.__class__.proxy.proxy))
                self.driver = webdriver.Chrome(chrome_options=self.__class__.chrome_options,
                                               executable_path=self.__class__.webdriver_path)
            elif (self.test_type == 'app'):
                from appium import webdriver
                self.driver = webdriver.Remote(Variable.ANDROID_SETTING['driver_url'], self.__class__.desired_caps)

        else:
            self.driver = self.__class__.driver
        cases.BaseFunctions.execute_step(self, self.tc['setup'])

    def tearDown(self):
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)

        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

        if not ok:
            img_name = self.__class__.__name__ + '.' + self._testMethodName
            self.driver.save_screenshot(self.screenshot_path + "%s.png" % img_name)
            # 截图路径 url , file_path
            screenshot_url = SITE_DATA_PATH + self.screenshot_path.replace(QM_REPORT_PATH_PREFIX,
                                                                           "") + img_name + '.png'
            print('失败截图路径：\n' + screenshot_url)

        cases.BaseFunctions.execute_step(self, self.tc['teardown'])
        if (self.__class__.driver == None):
            self.driver.quit()

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    @classmethod
    def tearDownClass(cls):
        cases.BaseFunctions.execute_step(cls, cls.ts_teardown)

        if (cls.server != None):
            cls.server.stop()

        if (cls.driver != None):
            cls.driver.quit()


def docit(doc=None):
    """ Document a function.

        >> @docit(doc='xxxx')
        >> def _GET(a, b):
        >>    assert a == b

        >> new_GET = docit(doc='foo')(_GET)
    """

    def wrapper(fn):
        @wraps(fn)  # python装饰器，加文档描述
        def func(*a, **kw):
            return fn(*a, **kw)

        func.__doc__ = doc
        return func

    return wrapper


def gen_test_suite(ts_raw_data, is_json_file=True, screenshot_path='', test_type='web'):
    testsuit = unittest.TestSuite()
    for ts_raw_info in ts_raw_data:
        ts_data = {}
        if (is_json_file):
            with open(ts_raw_info, 'r', encoding='utf-8') as f:
                ts_data = json.load(f)
        else:
            ts_data = ts_raw_data[ts_raw_info]
        # testsuite类 名称，类型，描述，传参
        if ('ts_setup' not in ts_data):
            ts_data['ts_setup'] = []
        if ('ts_teardown' not in ts_data):
            ts_data['ts_teardown'] = []

        project_id = -1
        if ('project_id' in ts_data):
            project_id = ts_data['project_id']

        ts_cls = type(ts_data['ts_name'], (BaseCase,),
                      {'__doc__': ts_data['ts_description'], 'ts_setup': ts_data['ts_setup'],
                       'ts_teardown': ts_data['ts_teardown'], 'screenshot_path': screenshot_path,
                       'test_type': test_type, 'project_id': project_id})
        cases_name = []

        if ('testcases' not in ts_data):
            ts_data['testcases'] = []

        # 创建testsuite类型
        for tc in ts_data['testcases']:
            method_name = tc['tc_name']
            test_method = getattr(cases.BaseFunctions, 'base_tc')
            test_method = docit(tc['tc_description'])(test_method)
            setattr(ts_cls, method_name, test_method)
            cases_name.append([method_name, tc])

        # 创建testsuite实例
        for method_name, tc in cases_name:
            project_id = -1
            if ('project_id' in ts_data):
                project_id = tc['project_id']
            t = ts_cls(method_name, tc=tc, screenshot_path=screenshot_path, test_type=test_type, project_id=project_id)
            testsuit.addTest(t)
    return testsuit


def gen_suite_report(testsuite, is_single_tc=False, report_path='', report_file_name='webui-report.html'):
    report_file_name = report_path + report_file_name

    if (is_single_tc):
        runner = unittest.TextTestRunner()
        result = runner.run(testsuite)
    else:
        with open(report_file_name, 'wb') as f:
            runner = HTMLTestRunner(stream=f, verbosity=1, title='UI Test', description='Web UI Test',
                                    report_path=report_path)
            result = runner.run(testsuite)

    return result


def main(report_path='', test_type='web'):
    if (test_type == 'web'):
        ts_json_files = TESTSUITE_WEB
    elif (test_type == 'app'):
        ts_json_files = TESTSUITE_APP
    testsuite = gen_test_suite(ts_json_files, True, report_path, test_type)
    return gen_suite_report(testsuite, False, report_path)


if __name__ == "__main__":
    main()
