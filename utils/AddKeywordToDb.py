#!/usr/bin/env python3
# coding:utf8

from sys import path

import pymysql


class SqlDriver():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.password = 'root123'
        self.database = 'techcms'

    def get_conn(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               # passwd=self.password,
                               db=self.database,
                               charset='utf8')
        return conn

    def execute_sql(self, sql):
        """执行mysql修改操作."""
        conn = self.get_conn()
        try:
            cur = conn.cursor()
            if cur:
                result = cur.execute(sql)
                conn.commit()
                return result
        except:
            conn.rollback()
            print('execute sql error, please check database connect or sql format!')


def add_path_to_env(file_list):
    """将文件目录添加到环境"""
    for file in file_list:
        path.insert(0, file)


def add_keywords_to_db():
    # 引入目录下的 Keywords.py

    keyword = Keywords
    object_dict = keyword.Keywords.__dict__
    sql = "delete from ui_file where filename='Keyword.py'"
    driver.execute_sql(sql)
    for key, value in object_dict.items():
        # 排除内置对象
        if '__' not in key:
            sql = r"insert into ui_file set filename='%s', `type`='1', function='%s',state=1 " % (
                'Keyword.py', str(key))
            driver.execute_sql(sql)


def add_app_keywords_to_db():
    # 引入目录下的 AppKeywords.py

    app = AppKeywords
    object_dict = app.AppKeywords.__dict__
    sql = "delete from ui_file where filename='AppKeywords.py'"
    driver.execute_sql(sql)
    for key, value in object_dict.items():
        # 排除内置对象
        if '__' not in key:
            sql = r"insert into ui_file set filename='%s', `type`='2', function='%s',state=1 " % (
                'AppKeywords.py', str(key))
            driver.execute_sql(sql)


def add_base_keywords_to_db():
    # 引入目录下的 BaseKeywords.py

    base = BaseKeywords
    object_dict = base.BaseKeywords.__dict__
    sql = "delete from ui_file where filename='BaseKeywords.py'"
    driver.execute_sql(sql)
    for key, value in object_dict.items():
        # 排除内置对象
        if '__' not in key:
            sql = r"insert into ui_file set filename='%s', `type`='3', function='%s',state=1 " % (
                'BaseKeywords.py', str(key))
            driver.execute_sql(sql)


if __name__ == "__main__":
    # 引入文件目录设置
    file_list = [r"/srv/live-ui-test/keywords/", "/srv/live-ui-test", '/srv/live-ui/test/verify/']
    add_path_to_env(file_list)
    # 引入 keywords目录下py class
    import Keywords
    import AppKeywords
    import BaseKeywords

    # 初始化SqlDriver
    driver = SqlDriver()
    # 添加class.def to database
    add_keywords_to_db()
    add_app_keywords_to_db()
    add_base_keywords_to_db()

    # 添加verify
    import verify.Verify
    sql = "delete from ui_file where filename='Verify.py'"
    driver.execute_sql(sql)
    for key in verify.Verify.__dict__.keys():
        if "assert" in key:
            sql = r"insert into ui_file set filename='%s', `type`='4', function='%s',state=1 " % (
                'Verify.py', str(key))
            driver.execute_sql(sql)