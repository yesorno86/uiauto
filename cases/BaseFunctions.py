# -*- coding: utf-8 -*-
import re
import verify.Verify
from keywords.Keywords import Keywords
from keywords.AppKeywords import AppKeywords


def execute_step(self, steps):
    if (self.test_type == 'web'):
        keywords = Keywords(self)
    elif (self.test_type == 'app'):
        keywords = AppKeywords(self)
    for step in steps:
        func_keyword = None
        func_verify = None

        if ("description" in step):
            print(step['description'])

        if ("keyword" in step):
            func_keyword = getattr(keywords, step['keyword'])

        if ("verify" in step and step['verify'] != ''):
            func_verify = getattr(verify.Verify, step['verify'])

        pattern = r'\$\w+'

        if ('params' in step):
            if (isinstance(step['params'], dict)):
                if (len(step['params']) != 0):
                    for key, value in step['params'].items():
                        if (isinstance(value, str) and re.match(pattern, value)):
                            step['params'][key] = getattr(self, value[1:])
                    result = func_keyword(**step['params'])
                else:
                    result = func_keyword()
            elif (isinstance(step['params'], list)):
                if (len(step['params']) != 0):
                    for i in range(len(step['params'])):
                        if (re.match(pattern, str(step['params'][i]))):
                            step['params'][i] = getattr(self, step['params'][i][1:])
                    result = func_keyword(*step['params'])
                else:
                    result = func_keyword()
            else:
                result = func_keyword()
        elif (func_keyword != None):
            result = func_keyword()

        if ('result' in step and step['result'] != ''):
            setattr(self, step['result'][1:], result)

        if ('datatoverify' in step and func_verify != None):
            if (isinstance(step['datatoverify'], dict)):
                if (len(step['datatoverify']) != 0):
                    for key, value in step['datatoverify'].items():
                        if (isinstance(value, str) and re.match(pattern, value)):
                            step['datatoverify'][key] = getattr(self, value[1:])
                    func_verify(**step['datatoverify'])
                else:
                    func_verify()
            elif (isinstance(step['datatoverify'], list)):
                if (len(step['datatoverify']) != 0):
                    for i in range(len(step['datatoverify'])):
                        if (re.match(pattern, str(step['datatoverify'][i]))):
                            step['datatoverify'][i] = getattr(self, step['datatoverify'][i][1:])
                    func_verify(*step['datatoverify'])
                else:
                    func_verify()
            else:
                func_verify()
        elif (func_verify != None):
            func_verify()


def base_tc(self):
    execute_step(self, self.tc['steps'])



