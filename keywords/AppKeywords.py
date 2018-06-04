# coding: utf-8
from utils import CommonKWOps
from keywords.BaseKeywords import BaseKeywords


class AppKeywords(BaseKeywords):
    def __init__(self, tsortc):
        super(AppKeywords, self).__init__(tsortc)

    def click_element(self, element_info, index=-1):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        if index == -1:
            element_obj = CommonKWOps.find_element(self.tsortc, *(getattr(page_obj, element_info[2])))
        else:
            element_obj = CommonKWOps.find_elements(self.tsortc, *(getattr(page_obj, element_info[2])))[index]
        element_obj.click()


    def send_keys(self, element_info, str_args):
        element_info = element_info.split(".")
        import_str = 'pages.' + element_info[1]
        page_module = __import__(import_str, fromlist=(element_info[1],))
        page_cls = getattr(page_module, element_info[1])
        page_obj = page_cls(self.driver)
        element_obj = CommonKWOps.find_element(self.tsortc, *(getattr(page_obj, element_info[2])))
        element_obj.send_keys(str_args)
        print(element_info, str_args)

