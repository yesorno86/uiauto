#!/usr/bin/env python3
# coding: utf-8
import pymysql

def db_insert(db, sql_sentence):
    conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'],
                           charset=db['charset'])
    cursor = conn.cursor()

    result = True
    try:
        cursor.execute(sql_sentence)
        id = conn.insert_id()
        conn.commit()
    except:
        result = False
        conn.rollback()
    conn.close()

    return (result, id)


def db_query(db, sql_sentence, fields = None):
    conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'],
                           charset=db['charset'])
    cursor = conn.cursor()
    results = []

    try:
        cursor.execute(sql_sentence)  # 执行sql语句
        results = cursor.fetchall()  # 获取查询的所有记录
        if(fields != None):
            results_list = []
            for res in results:
                temp = {}
                for i in range(len(fields)):
                    temp[fields[i]] = res[i]
                results_list.append(temp)
            results = results_list

    except Exception as e:
        print(str(e))
        results = []
    finally:
        conn.close()  # 关闭连接

    return results

def db_delete(db, sql_sentence):
    conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'],
                           charset=db['charset'])
    cursor = conn.cursor()

    result = True
    try:
        cursor.execute(sql_sentence)  # 像sql语句传递参数
        # 提交
        conn.commit()
    except Exception as e:
        # 错误回滚
        result = False
        conn.rollback()
    finally:
        conn.close()

    return  result


def db_update(db,sql_sentence):
    conn = pymysql.connect(host=db['host'], port=db['port'], user=db['user'], passwd=db['passwd'], db=db['db'],
                           charset=db['charset'])
    cursor = conn.cursor()

    result = True
    try:
        cursor.execute(sql_sentence)  # 像sql语句传递参数
        # 提交
        conn.commit()
    except Exception as e:
        # 错误回滚
        result = False
        conn.rollback()
    finally:
        conn.close()

    return result






