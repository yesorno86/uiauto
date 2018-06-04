# coding:utf8

"""
Created on 2018-01-23
@author: peter
Description: 直播web导航
"""

from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class BaiduIndex(BasePage):
    """直播web顶部导航"""

    def __init__(self, selenium_driver):
        super(BaiduIndex, self).__init__(selenium_driver)

        #定义百度首页搜索输入框和搜索按钮
        self.search_text = (By.XPATH, r'//*[@id="kw"]')
        self.search_button = (By.XPATH, r'//*[@id="su"]')
        #定义百度搜索结果页面‘更多’链接
        self.more_link = (By.XPATH, r'//*[@id="s_tab"]/a[9]')
