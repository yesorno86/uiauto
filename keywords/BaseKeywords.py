# coding: utf-8
import json
import re
import time

import requests
from selenium.webdriver.common.action_chains import ActionChains

from config.Variable import *


class BaseKeywords():
    def __init__(self, tsortc):
        self.driver = tsortc.driver
        self.screenshot_path = tsortc.screenshot_path
        self.tsortc = tsortc

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

    def get_value_from_json(self, json_data, value_path):
        result = json_data
        indexs = value_path.split('.')
        for index in indexs:
            result = result[index]
        return result

    def sleep(self, t=2):
        """强制等待"""
        time.sleep(int(t))
