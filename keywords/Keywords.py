# -*- coding: utf-8 -*-
import json
import re
import time

import requests
from selenium.webdriver.common.action_chains import ActionChains

from utils import CommonKWOps
from config.Variable import *
from keywords.BaseKeywords import BaseKeywords


class Keywords(BaseKeywords):
    def __init__(self, tsortc):
        super(Keywords, self).__init__(tsortc)

    # 打开页面，并校验页面链接是否加载正确
    # 以单下划线_开头的方法，在使用import *时，该方法不会被导入，保证该方法为类私有的。
    def open_page(self, url, pagetitle):
        # 使用get打开访问链接地址
        self.driver.get(url)
        # self.driver.maximize_window()
        time.sleep(2)
        # 使用assert进行校验，打开的窗口title是否与配置的title一致。调用on_page()方法
        assert self._on_page(pagetitle), u"打开页面失败 %s" % url

    # 通过title断言进入的页面是否正确。
    # 使用title获取当前窗口title，检查输入的title是否在当前title中，返回比较结果（True 或 False）
    def _on_page(self, pagetitle):
        return pagetitle in self.driver.title

    def scroll_to_bottom(self):
        # 翻滚页面至底部
        start_point = 0
        while start_point < 7000:
            time.sleep(0.3)
            to_point = start_point + 1000
            js_scroll_bottom = r'window.scrollTo(%s,%s)' % (start_point, to_point)
            self.driver.execute_script(js_scroll_bottom)
            start_point = to_point

    def send_request(self, **request):
        status_code = None
        json_result = {}
        text = None
        if request.get("data"):
            request["data"] = json.dumps(request["data"])
        try:
            r = requests.request(**request)
            status_code = r.status_code
            json_result = r.json()
            text = r.text
        except Exception as e:
            print(e)
            json_result = {"text": text}
        return json_result

    def get_page_element_attribute(self, element_info):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_obj = CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2])))
        pattern = r'([A-Za-z0-9_\-]+)(\(")([A-Za-z0-9_\-]+)("\))'
        groups = re.match(pattern, element_info[3])
        element_method = getattr(element_obj, groups.group(1))
        return element_method(groups.group(3))

    def get_page_element_text(self, element_info):
        element_info_list = element_info.split(".")
        # import_str = 'pages.' + element_info[1]
        # page_module = __import__(import_str, fromlist=(element_info[1],))
        # page_cls = getattr(page_module, element_info[1])
        # page_obj = page_cls(self.driver)
        # element_obj = CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2])))
        element_info_tuple = CommonKWOps.get_element_info(self.tsortc, element_info)
        element_obj = CommonKWOps.find_element(self, *element_info_tuple)
        element_text = getattr(element_obj, element_info_list[3])
        return element_text

    def get_value_from_json(self, json_data, value_path):
        result = json_data
        indexs = value_path.split('.')
        for index in indexs:
            result = result[index]
        return result

    def get_page_element_count(self, element_info):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_objs = CommonKWOps.find_elements(self, *(getattr(page_obj, element_info[2])))

        return len(element_objs)

    def move_to_element(self, element_info):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_obj = CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2])))
        ActionChains(self.driver).move_to_element(element_obj).perform()

    def click_element(self, element_info):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_obj = CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2])))
        element_obj.click()

    def click_element_unnecessary(self, element_info, timeout):
        """特殊事件说明：
        若该元素可出现，可不出现，则走此方法
        """
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        is_show = CommonKWOps.check_element(self, *(getattr(page_obj, element_info[2])), timeout=timeout)
        if is_show:
            CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2]))).click()

    def send_keys(self, element_info, str_args):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_obj = CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2])))
        element_obj.send_keys(str_args)

    def del_cookie(self, key_name):
        self.driver.delete_cookie("%s" % key_name)

    def refresh_page(self):
        """刷新页面"""
        self.driver.refresh()

    def sleep(self, t=2):
        """强制等待"""
        time.sleep(int(t))

    def switch_to_frame(self, element_info):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_obj = CommonKWOps.find_element(self, *(getattr(page_obj, element_info[2])))
        self.driver.switch_to.frame(element_obj)

    def swtich_to_default_frame(self):
        """返回frame的上一级目录"""
        self.driver.switch_to.default_content()

    def switch_to_windows(self, target_window=-1):
        """
        切换浏览器窗口
        :param target_window: index of window, start with 0, end with -1
        :return:
        """
        self.driver.switch_to.window(self.driver.window_handles[target_window])

    def switch_to_active_element(self):
        """
        switch to focus element.
        :return:
        """
        return self.driver.switch_to.active_element

    def switch_to_alert(self):
        """
        switch to alert or dialog
        """
        return self.driver.switch_to.alert

    def maximize_window(self, target_window=-1):
        """
        窗口最大化
        maximize_window
        """
        self.driver.maximize_window()

    def get_screenshot_as_file(self, filename):
        """
        按照testcase描述截图
        """
        self.driver.get_screenshot_as_file(self.screenshot_path + '%s.png' % filename)

    def close(self):
        """
        关闭当前窗口
        """
        self.driver.close()

    def excute_js(self, js):
        self.driver.execute_script(js)

    def check_element_exist(self, element_info):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        result = CommonKWOps.check_element(self, *(getattr(page_obj, element_info[2])))
        if result:
            return 'true'
        return 'false'

    def get_url(self):
        """获取当前页面的url"""
        return self.driver.current_url

    def get_window_title(self, target_window=-1):
        """ 获取窗口title"""
        self.switch_to_windows(target_window)
        return self.driver.title
