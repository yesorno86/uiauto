# from selenium.webdriver.common.by import By
# todo:调试下appium api
from appium.webdriver.common.mobileby import By

from pages.AppBasePage import AppBasePage


class AppIndex(AppBasePage):
    def __init__(self, appnium_driver):
        super(AppIndex, self).__init__(appnium_driver)

        self.cal_one = (By.ANDROID_UIAUTOMATOR, r'text("1")')
        self.cal_two = (By.ANDROID_UIAUTOMATOR, r'text("2")')
        self.cal_three = (By.ANDROID_UIAUTOMATOR, r'text("3")')
        self.cal_four = (By.ANDROID_UIAUTOMATOR, r'text("4")')
        self.cal_five = (By.ANDROID_UIAUTOMATOR, r'text("5")')
