# coding:utf8

"""
Created on 2018-01-23
@author: peter
Description: 直播web导航
"""

from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class BaiduResult(BasePage):
    """直播web顶部导航"""

    def __init__(self, selenium_driver):
        super(BaiduResult, self).__init__(selenium_driver)

        #定义百度搜索结果页面‘更多’链接
        self.more_link = (By.XPATH, r'//*[@id="s_tab"]/a[9]')
        # 定义百度搜索结果页面搜索按钮
        self.search_button = (By.XPATH, r'//*[@id="su"]')
