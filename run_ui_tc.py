#!/usr/bin/env python3
# coding: utf-8
import os.path
import re
import smtplib
import time
from email.mime.text import MIMEText

import pymysql
import cases.TestSuite
from config.Variable import *
import argparse
import sys

def runtc(qm_report_path, test_type = 'web'):
    """
    to execute  test cases
    :param qm_report_path: place to put the test report
    :return: report path, test_result
    """
    report_path = qm_report_path + time.strftime('%Y%m%d', time.localtime(time.time())) + str(int(time.time())) + '/'
    while_condition = False
    while (not while_condition):
        try:
            os.makedirs(report_path)
        except:
            while_condition = False
        else:
            while_condition = True

    test_result = cases.TestSuite.main(report_path, test_type)

    return (report_path, test_result)


def send_email(report_path):
    """
    send report email
    :return: none
    """
    sender = MAILINFO['sender']
    receiver = MAILINFO['receiver']
    subject = MAILINFO['subject']
    username = MAILINFO['username']
    password = MAILINFO['password']

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


def insert_report_to_db(data, db, report_path):
    conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'],
                           charset=db['charset'])
    cursor = conn.cursor()
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    summary = "Ran:{0}, Pass:{1}, Fail:{2}, Error:{3}".format(data.testsRun, data.success_count, data.failure_count,
                                                              data.error_count)

    sql_sentence = 'insert into `ui_report`(`tsids`, `reporttime`, `duration`,' \
                   ' `summary`, `report`, `status`) values("1","' + date + '","' + str(
        data.duration) + '","' + summary + '","' + report_path + '", "2")'

    result = True
    try:
        cursor.execute(sql_sentence)
        id = conn.insert_id()
        conn.commit()
    except:
        result = False
        db.rollback()
    conn.close()

    return (result, id)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run ui test cases.')
    parser.add_argument("-t", "--test_type", help='test type, available value: web, app')
    args = parser.parse_args()
    test_type = "web"
    if args.test_type:
        test_type = args.test_type

    ut_report_name = UT_REPORT_NAME
    qm_report_path = QM_REPORT_PATH
    qm_report_path_prefix = QM_REPORT_PATH_PREFIX
    db = DB

    (report_path, test_result) = runtc(qm_report_path, test_type)

    temp_path = report_path
    if (qm_report_path_prefix != None):
        temp_path = report_path.replace(qm_report_path_prefix, '')
    path_in_db = temp_path + ut_report_name

    # report写入数据库
    (result, id) = insert_report_to_db(test_result, db, path_in_db)
    if (result):
        print('Report record was saved to database!')
    else:
        print('Report record was failed to save to database!')

    report_id = str(id)
    report_files = [report_path + 'casetable', report_path + 'passtable']

    for file in report_files:
        with open(file, 'r', encoding='utf-8') as report:
            lines = report.readlines()
            report_str = "".join(lines)
            (report_str, num) = re.subn(r'###reportid###', report_id, report_str)
        with open(file, 'w', encoding='utf-8') as report:
            report.write(report_str)

    send_email(report_path)
    print("Report email was sent.")
