#!/usr/bin/env python3
# coding: utf-8
from utils import DBUtils
import json
from config.Variable import *

tc_fields = ['id', 'tsid', 'name', 'description', 'tag']
ts_fields = ['id', 'tprojectid', 'name', 'description']
step_fileds = ['id', 'description', 'istc', 'tcortsid', 'type', 'seq', 'keyword', 'params', 'result', 'verify',
               'datatoverify']


def get_ts_data_in_db(db, tc_ids, ts_ids, tags):
    ts_data = {}

    if (len(tc_ids) != 0):
        tc_ids_str = '(' + ','.join(tc_ids) + ')'
        tc_sql = ""
        if (len(tags) != 0):
            tags_str = '(' + ','.join(tags) + ')'
            tc_sql = 'select * from ui_tc where id in ' + tc_ids_str + ' and ' + 'tag in ' + tags_str
        else:
            tc_sql = 'select * from ui_tc where id in ' + tc_ids_str

        tc_in_db = DBUtils.db_query(db, tc_sql, tc_fields)

        for tc in tc_in_db:
            tc_ts_info = {}
            if (tc['tsid'] not in ts_data):
                tc_ts_sql = 'select * from ui_ts where id = {0}'.format(tc['tsid'])
                tc_ts_info = DBUtils.db_query(db, tc_ts_sql, ts_fields)
                tc_ts_info = tc_ts_info[0]
                ts_data[tc['tsid']] = {'ts_name': tc_ts_info['name'], 'ts_description': tc_ts_info['description'],
                                       'ts_setup': [], 'testcases': [], 'ts_teardown': [], 'project_id': tc_ts_info['tprojectid']}
                tc_ts_setup_steps_sql = 'select * from ui_step where istc=0 and tcortsid={0} and type=1 order by seq asc'.format(
                    tc_ts_info['id'])
                tc_ts_teardown_steps_sql = 'select * from ui_step where istc=0 and tcortsid={0} and type=3 order by seq asc'.format(
                    tc_ts_info['id'])
                tc_ts_setup_steps = DBUtils.db_query(db, tc_ts_setup_steps_sql, step_fileds)
                tc_ts_teardown_steps = DBUtils.db_query(db, tc_ts_teardown_steps_sql, step_fileds)
                for step in tc_ts_setup_steps:
                    ts_data[tc_ts_info['id']]['ts_setup'].append(get_step_dict(step))
                for step in tc_ts_teardown_steps:
                    ts_data[tc_ts_info['id']['ts_teardown']].append(get_step_dict(step))

            tc_data = get_tc_dict(db, tc)
            tc_data['project_id'] = ts_data[tc['tsid']]['project_id']
            ts_data[tc['tsid']]['testcases'].append(tc_data)

    elif (len(ts_ids) != 0):
        ts_ids_str = '(' + ','.join(ts_ids) + ')'
        ts_sql = 'select * from ui_ts where id in ' + ts_ids_str
        ts_in_db = DBUtils.db_query(db, ts_sql, ts_fields)

        for ts in ts_in_db:
            ts_data[ts['id']] = {'ts_name': ts['name'], 'ts_description': ts['description'], 'ts_setup': [],
                                 'testcases': [], 'teardown': [], 'project_id': ts['tprojectid']}

            ts_setup_steps_sql = 'select * from ui_step where istc=0 and tcortsid={0} and type=1 order by seq asc'.format(
                ts['id'])
            ts_teardown_steps_sql = 'select * from ui_step where istc=0 and tcortsid={0} and type=3 order by seq asc'.format(
                ts['id'])
            ts_setup_steps = DBUtils.db_query(db, ts_setup_steps_sql, step_fileds)
            ts_teardown_steps = DBUtils.db_query(db, ts_teardown_steps_sql, step_fileds)
            for step in ts_setup_steps:
                ts_data[ts['id']]['ts_setup'].append(get_step_dict(step))
            for step in ts_teardown_steps:
                ts_data[ts['id']['ts_teardown']].append(get_step_dict(step))

        ts_tc_sql = ''
        if (len(tags) != 0):
            tags_str = '(' + ','.join(tags) + ')'
            ts_tc_sql = 'select * from ui_tc where tsid in ' + ts_ids_str + ' and ' + 'tag in ' + tags_str
        else:
            ts_tc_sql = 'select * from ui_tc where tsid in ' + ts_ids_str

        ts_tc_info = DBUtils.db_query(db, ts_tc_sql, tc_fields)
        for tc in ts_tc_info:
            tc_data = get_tc_dict(db, tc)
            tc_data['project_id'] = ts_data[tc['tsid']]['project_id']
            ts_data[tc['tsid']]['testcases'].append(tc_data)

    return ts_data


def get_step_dict(step):
    step_dict = {"description": step['description'], "keyword": step["keyword"]}
    if ('params' in step):
        step_dict['params'] = json.loads(step['params']) if step["params"] != "" else []
    if ('result' in step):
        step_dict['result'] = step['result']
    if ('verify' in step):
        step_dict['verify'] = step['verify']
    if ('datatoverify' in step):
        step_dict['datatoverify'] = json.loads(step['datatoverify']) if step['datatoverify'] != "" else []
    return step_dict


def get_tc_dict(db, tc):
    tc_setup_steps_sql = 'select * from ui_step where istc=1 and tcortsid={0} and type=1 order by seq asc'.format(
        tc['id'])
    tc_teardown_steps_sql = 'select * from ui_step where istc=1 and tcortsid={0} and type=3 order by seq asc'.format(
        tc['id'])
    tc_steps_sql = 'select * from ui_step where istc=1 and tcortsid={0} and type=2 order by seq asc'.format(
        tc['id'])
    tc_setup_steps = DBUtils.db_query(db, tc_setup_steps_sql, step_fileds)
    tc_teardown_steps = DBUtils.db_query(db, tc_teardown_steps_sql, step_fileds)
    tc_steps = DBUtils.db_query(db, tc_steps_sql, step_fileds)

    tc_data = {'tc_name': tc['name'], 'tc_description': tc['description'], 'setup': [], 'steps': [],
               'teardown': []}

    for step in tc_setup_steps:
        tc_data['setup'].append(get_step_dict(step))
    for step in tc_steps:
        tc_data['steps'].append(get_step_dict(step))
    for step in tc_teardown_steps:
        tc_data['teardown'].append(get_step_dict(step))

    return tc_data
