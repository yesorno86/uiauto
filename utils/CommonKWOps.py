from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.Variable import *
import selenium.common.exceptions
from utils import DBUtils
from selenium.webdriver.common.by import By

# 重写元素定位方法
def find_element(self, *loc):
    #        return self.driver.find_element(*loc)
    try:
        # 确保元素是可见的。
        # 注意：以下入参为元组的元素，需要加*。Python存在这种特性，就是将入参放在元组里。
        #            WebDriverWait(self.driver,10).until(lambda driver: driver.find_element(*loc).is_displayed())
        # 注意：以下入参本身是元组，不需要加*
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(loc))
        return self.driver.find_element(*loc)
    except Exception as e:
        print(u"%s 页面中未能找到 %s 元素" % (self, loc))


def find_elements(self, *loc):
    try:
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(loc))
        return self.driver.find_elements(*loc)
    except:
        print(u"%s 页面中未能找到 %s 元素" % (self, loc))


def check_element(self, *loc, timeout=3):
    """
    检查元素是否存在
    :param loc: 元素 json对象
    :param timeout: 查找元素超时时间
    :return: 元素是否存在
    """
    try:
        WebDriverWait(self.driver, timeout=timeout).until(EC.visibility_of_element_located(loc))
        return True
    except selenium.common.exceptions.ElementNotVisibleException:
        return False
    except selenium.common.exceptions.TimeoutException:
        return False


def get_element_info(self, element_info):
    element_info_tuple = ()
    element_info = element_info.split(".")

    if(self.project_id != -1):
        sql_sentence = 'select bytype, byvalue from ui_page, ui_page_element where ui_page.tprojectid=' + str(
            self.project_id) + ' and  ui_page.name="' + element_info[1] + '" and ui_page_element.name="' + \
                       element_info[2] + '"'
        element_info_in_db = list(DBUtils.db_query(DB, sql_sentence))
        if(len(element_info_in_db) != 0):
            element_info_tuple = (getattr(By, element_info_in_db[0][0].split('.')[1]), element_info_in_db[0][1])

    if(len(element_info_tuple) == 0):
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_info_tuple = getattr(page_obj, element_info[2])

    return element_info_tuple
