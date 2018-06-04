#!/usr/bin/env python3
# coding: utf-8
import os.path
import time

import pymysql
from config.Variable import *
from config import Variable
import argparse
from utils import RunUtil
from cases import TestSuite
from utils import DBUtils
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
import json
import re
import smtplib
from email.mime.text import MIMEText


def runtc(ts_data, qm_report_path, test_type='web'):
    """
    to execute  test cases
    :param qm_report_path: place to put the test report
    :return: report path, test_result
    """
    while_condition = False
    while (not while_condition):
        try:
            report_path = qm_report_path + time.strftime('%Y%m%d', time.localtime(time.time())) + str(
                int(time.time())) + '/'
            os.makedirs(report_path)
        except:
            while_condition = False
        else:
            while_condition = True

    testsuite = TestSuite.gen_test_suite(ts_data, False, report_path, test_type)
    test_result = TestSuite.gen_suite_report(testsuite, False, report_path)

    return (report_path, test_result)


# def insert_report_to_db(data, db, report_path):
#     conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'],
#                            charset=db['charset'])
#     cursor = conn.cursor()
#     date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     summary = "Ran:{0}, Pass:{1}, Fail:{2}, Error:{3}".format(data.testsRun, data.success_count, data.failure_count,
#                                                               data.error_count)
#
#     sql_sentence = 'insert into `webui_report`(`projectid`, `reporttime`, `duration`,' \
#                    ' `summary`, `report`) values(1,"' + date + '","' + str(
#         data.duration) + '","' + summary + '","' + report_path + '")'
#
#     result = True
#     try:
#         cursor.execute(sql_sentence)
#         id = conn.insert_id()
#         conn.commit()
#     except:
#         result = False
#         db.rollback()
#     conn.close()
#
#     return (result, id)


def send_email(report_path):
    """
    send report email
    :return: none
    """
    sender = Variable.MAILINFO['sender']
    receiver = Variable.MAILINFO['receiver']
    subject = Variable.MAILINFO['subject']
    username = Variable.MAILINFO['username']
    password = Variable.MAILINFO['password']

    report_files = [report_path + 'totalreport', report_path + 'scenetable', report_path + 'casetable',
                    report_path + 'passtable']

    report_str = ""

    for file in report_files:
        with open(file, 'r', encoding='utf-8') as report:
            lines = report.readlines()
            report_str += ''.join(lines)

    msg = MIMEText(report_str, 'html', 'utf-8')
    msg['from'] = sender
    msg['to'] = ','.join(receiver)
    msg['Subject'] = subject

    smtp = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == "__main__":

    try:
        By.IOS_UIAUTOMATION = MobileBy.IOS_UIAUTOMATION
        By.IOS_PREDICATE = MobileBy.IOS_PREDICATE
        By.IOS_CLASS_CHAIN = MobileBy.IOS_CLASS_CHAIN
        By.ANDROID_UIAUTOMATOR = MobileBy.ANDROID_UIAUTOMATOR
        By.ACCESSIBILITY_ID = MobileBy.ACCESSIBILITY_ID

        parser = argparse.ArgumentParser(description='Run ui test cases.')
        parser.add_argument("-t", "--test_type", help='test type, available value: web, app', default='web')
        parser.add_argument("-c", "--tc", help='test case ids, value like: 1,2,3...')
        parser.add_argument("-s", "--ts", help='test suite ids, value like: 1,2,3...')
        parser.add_argument("-g", "--tag", help='test case tag, value like: tag1, tag2, tag3 ...')
        parser.add_argument("-e", "--envid", help='environment id in db, value live: 1')
        parser.add_argument("-m", "--is_multiple",
                            help='to run single or multiple test cases, available value: yes, no')
        parser.add_argument("-r", "--receiver",
                            help='report receiver emails, like: ukey86105@163.com')

        args = parser.parse_args()
        tc_ids = []
        ts_ids = []
        tags = []
        test_type = 'web'
        is_multiple = 'no'
        env_id = 0
        receivers = ''

        if args.test_type:
            test_type = args.test_type
        if args.tc:
            tc_ids = args.tc.split(',')
            tc_ids = [id.strip() for id in tc_ids]
        if args.ts:
            ts_ids = args.ts.split(',')
            ts_ids = [id.strip() for id in ts_ids]
        if args.tag:
            tags = args.tag.split(',')
            tags = [tag.strip() for tag in tags]
        if args.envid:
            env_id = args.envid
        if args.is_multiple:
            is_multiple = args.is_multiple
        if args.receiver:
            receivers = args.receiver

        db = DB

        env = []
        if (env_id != 0):
            if (test_type == "web"):
                env_fields = ["id", "projectid", "name", "hostip"]
                env_sql = 'select * from ui_hosts where id=' + env_id
            elif (test_type == "app"):
                env_fields = ["id", "projectid", "name", "platformName", "platformVersion", "deviceName",
                              "appPackage", "appActivity", "appiumUrl", "status"]
                env_sql = 'select * from ui_devices where id=' + env_id

            env = DBUtils.db_query(db, env_sql, env_fields)

        if (len(env) != 0):
            if (test_type == "web"):
                Variable.WEB_HOSTS = json.loads(env[0]['hostip'])
            elif (test_type == "app"):
                app_settings = {}
                app_settings['platformName'] = env[0]['platformName']
                app_settings['platformVersion'] = env[0]['platformVersion']
                app_settings['deviceName'] = env[0]['deviceName']
                app_settings['appPackage'] = env[0]['appPackage']
                app_settings['appActivity'] = env[0]['appActivity']
                app_settings['driver_url'] = env[0]['appiumUrl']
                Variable.ANDROID_SETTING = app_settings

        Variable.MAILINFO['receiver'] = []
        if (receivers != ''):
            receivers = [r.strip() for r in receivers.split(',')]
            Variable.MAILINFO['receiver'] = receivers

        ts_data = RunUtil.get_ts_data_in_db(db, tc_ids, ts_ids, tags)

        ut_report_name = UT_REPORT_NAME
        ut_exception_info_file = UT_EXCEPTION_INFO_FILE
        qm_report_path = QM_REPORT_PATH
        qm_report_path_prefix = QM_REPORT_PATH_PREFIX
        qm_single_res_path = QM_SINGLE_RES_PATH

        if (is_multiple == 'no'):
            testsuite = TestSuite.gen_test_suite(ts_data, False, qm_single_res_path, test_type)
            TestSuite.gen_suite_report(testsuite, True)
        else:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            ts_data_keys = [str(key) for key in list(ts_data.keys())]
            ts_ids_str = ','.join(ts_data_keys)

            sql_sentence = 'insert into `ui_report`(`tsids`, `reporttime`, `duration`,' \
                           ' `summary`, `report`, `status`,`envid`) values("' + ts_ids_str + '", "' + date + '", "", "", "", 1, "%s")' % env_id
            (result_new, id) = DBUtils.db_insert(db, sql_sentence)
            try:
                (report_path, test_result) = runtc(ts_data, qm_report_path, test_type)
            except:
                import traceback
                exception_str = traceback.format_exc()
                html_content = "<h3>异常信息</h3><p>" + exception_str + "</p>"
                while_condition = False
                while (not while_condition):
                    try:
                        report_path = qm_report_path + time.strftime('%Y%m%d', time.localtime(time.time())) + str(
                            int(time.time())) + '/'
                        os.makedirs(report_path)
                    except:
                        while_condition = False
                    else:
                        while_condition = True

                exception_file_path = report_path + ut_exception_info_file
                exception_file = open(exception_file_path, 'w', encoding='utf-8')
                exception_file.write(html_content)

                exception_path_in_db = exception_file_path
                if (qm_report_path_prefix != None):
                    exception_path_in_db = exception_file_path.replace(qm_report_path_prefix, '')

                sql_sentence = 'update `ui_report` set `summary` = "执行测试用例过程中发生异常",  `report` = "' + exception_path_in_db + '", `status`=2 where id=' + str(
                    id)

                # report写入数据库
                result = DBUtils.db_update(db, sql_sentence)
            else:
                temp_path = report_path
                if (qm_report_path_prefix != None):
                    temp_path = report_path.replace(qm_report_path_prefix, '')
                path_in_db = temp_path + ut_report_name

                summary = "Ran:{0}, Pass:{1}, Fail:{2}, Error:{3}".format(test_result.testsRun,
                                                                          test_result.success_count,
                                                                          test_result.failure_count,
                                                                          test_result.error_count)

                sql_sentence = 'update `ui_report` set `duration` = "' + str(
                    test_result.duration) + '", `summary` = "' + summary + '", `report` = "' + path_in_db + '", `status`=2 where id=' + str(
                    id)

                # report写入数据库
                result = DBUtils.db_update(db, sql_sentence)

                # 替换reportid placeholder为真实的reportid
                report_id = str(id)
                report_files = [report_path + 'casetable', report_path + 'passtable']
                for file in report_files:
                    with open(file, 'r', encoding='utf-8') as report:
                        lines = report.readlines()
                        report_str = "".join(lines)
                        (report_str, num) = re.subn(r'###reportid###', report_id, report_str)
                    with open(file, 'w', encoding='utf-8') as report:
                        report.write(report_str)

                if (len(Variable.MAILINFO['receiver']) != 0):
                    send_email(report_path)

            if (result):
                print('Report record was saved to database!')
            else:
                print('Report record was failed to save to database!')

    finally:
        if (test_type == "app" and env_id != 0):
            env_sql_update = "update ui_devices set status=1 where id=" + env_id
            DBUtils.db_update(db, env_sql_update)
