#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands

import time
import uuid

import datetime

import operator
from apscheduler.triggers.cron import CronTrigger
from flask import render_template
from flask import request, session
from mongoengine import Q

from app import app
from common.xa_result import XaResult
from common.string_util import StringUtil
from common.json_util import JsonUtil
from models.job_define import JobDefine
from common.page import Page
from common.datatable_result import DataTableResult
from app import scheduler
from models.job_increment_param_record import JobIncrementParamRecord
from models.job_instance import JobInstance
import job_task_load


@app.route('/job_define', methods=['GET'])
def to_job_define():
    return render_template('job_define.html')


@app.route('/job_define/create', methods=['POST'])
def create():
    name = request.form['name'] if 'name' in request.form else ''
    displayName = request.form['displayName'] if 'displayName' in request.form else ''
    defJson = request.form['defJson'] if 'defJson' in request.form else ''
    isIncrement = request.form['isIncrement'] if 'isIncrement' in request.form else 0
    incrementParam = request.form['incrementParam'] if 'incrementParam' in request.form else ''
    incrementParamStart = request.form['incrementParamStart'] if 'incrementParamStart' in request.form else ''
    jobCron = request.form['jobCron'] if 'jobCron' in request.form else ''

    if StringUtil.isBlank(name):
        return XaResult.error(msg=u'请输入任务名称')
    if StringUtil.isBlank(displayName):
        return XaResult.error(msg=u'请输入任务用于显示的中文名称')
    if StringUtil.isBlank(defJson):
        return XaResult.error(msg=u'请输入任务Json模板')

    isIncrement = True if isIncrement and int(isIncrement) == 1 else False

    if isIncrement and StringUtil.isBlank(incrementParam):
        return XaResult.error(msg=u'增量同步任务，请指明Json模板中的参数名称')
    if isIncrement and StringUtil.isBlank(incrementParamStart):
        return XaResult.error(msg=u'增量同步任务，请指明Json模板中的参数起始值')
    if not JsonUtil.is_json(defJson):
        return XaResult.error(msg=u'请确保Json格式正确（先委屈一下，界面化配置后面马上开发）')
    if StringUtil.isBlank(jobCron):
        return XaResult.error(msg=u'请输入任务cron表达式')

    extendJobDefine = JobDefine.objects(Q(name=name) | Q(displayName=displayName)).first()

    if extendJobDefine is None:
        jobDefine = JobDefine(name=name, displayName=displayName, defJson=defJson, isIncrement=isIncrement,
                              incrementParam=incrementParam, incrementParamStart=incrementParamStart, jobCron=jobCron)
        jobDefine.save()
    else:
        return XaResult.error(msg=u'任务名称和用于显示的中文名称不可重复')

    return XaResult.success()


@app.route('/job_define/get', methods=['POST'])
def getone():
    name = request.values['name'] if 'name' in request.values else ''
    extendJobDefine = JobDefine.objects((Q(name=name))).first()
    if extendJobDefine is None:
        return XaResult.error(msg=u'请提供正确且存在的任务名称')
    return XaResult.success(extendJobDefine)


@app.route('/job_define/modify', methods=['POST'])
def modify():
    # 不能修改名称和用于显示的中文名称，你传了我也不会改
    name = request.form['name'] if 'name' in request.form else ''

    defJson = request.form['defJson'] if 'defJson' in request.form else ''
    isIncrement = int(request.form['isIncrement']) if 'isIncrement' in request.form else 0
    incrementParam = request.form['incrementParam'] if 'incrementParam' in request.form else ''
    incrementParamStart = request.form['incrementParamStart'] if 'incrementParamStart' in request.form else ''
    jobCron = request.form['jobCron'] if 'jobCron' in request.form else ''

    if StringUtil.isBlank(name):
        return XaResult.error(msg=u'请提供需要修改的任务名称')
    if StringUtil.isBlank(defJson):
        return XaResult.error(msg=u'请输入任务Json模板')
    if isIncrement and StringUtil.isBlank(incrementParam):
        return XaResult.error(msg=u'增量同步任务，请指明Json模板中的参数名称')
    if isIncrement and StringUtil.isBlank(incrementParamStart):
        return XaResult.error(msg=u'增量同步任务，请指明Json模板中的参数起始值')
    if not JsonUtil.is_json(defJson):
        return XaResult.error(msg=u'请确保Json格式正确（先委屈一下，界面化配置后面马上开发）')
    if StringUtil.isBlank(jobCron):
        return XaResult.error(msg=u'请输入任务cron表达式')

    extendJobDefine = JobDefine.objects((Q(name=name))).first()

    if extendJobDefine is None:
        return XaResult.error(msg=u'请提供正确且存在的任务名称')

    # 这里有并发更新覆盖的问题(这也是我对mongodb一直不太明白的地方)
    JobDefine.objects(name=name).update_one(defJson=defJson,
                                            isIncrement=True if isIncrement == 1 else False,
                                            incrementParam=incrementParam,
                                            incrementParamStart=incrementParamStart,
                                            jobCron=jobCron)

    return XaResult.success()


@app.route('/job_define/list', methods=['POST'])
def find_list():
    display_start = int(request.form['iDisplayStart']) if 'iDisplayStart' in request.form else 1
    per_page = int(request.form['iDisplayLength']) if 'iDisplayLength' in request.form else 10

    page = display_start / per_page

    search = request.form['sSearch'] if 'sSearch' in request.form else ''

    q_list = [Q(isDelete=False)]

    if StringUtil.isNotBlank(search):
        q_list.append(Q(name__contains=search) | Q(displayName__contains=search))

    jobDefines = JobDefine.objects(reduce(operator.and_, q_list)).paginate(page=page + 1 if page > 0 else 1,
                                                                           per_page=per_page)

    return DataTableResult.format(Page.from_paginate(jobDefines).json_serialize())


@app.route('/job_define/delete', methods=['POST'])
def delete():
    name = request.form['name'] if 'name' in request.form else ''

    extendJobDefine = JobDefine.objects((Q(name=name))).first()

    if not extendJobDefine:
        return XaResult.error(msg=u'请提供正确且存在的任务名称')

    if extendJobDefine.isOpen:
        return XaResult.error(msg=u'该任务正在运行中，请停止后再删除')

    JobDefine.objects(name=name).update_one(isDelete=True)

    return XaResult.success()


@app.route('/job_instance/startup', methods=['POST'])
def startup():
    name = request.values['name'] if 'name' in request.values else ''
    extendJobDefine = JobDefine.objects((Q(name=name))).first()

    if extendJobDefine is None:
        return XaResult.error(msg=u'请提供正确且存在的任务名称')
    try:
        cron = CronTrigger.from_crontab(extendJobDefine.jobCron)

        scheduler.add_job(id=name, func=job_task_load.to_job_instance, trigger=cron, args=(name,))
        JobDefine.objects(name=name).update_one(isRun=True)
        app.logger.info(u'%s 任务启动成功！', name)
    except Exception, e:
        app.logger.error(u'%s 任务启动失败！错误信息：%s', name, e.message)
        return XaResult.error(msg=e.message)

    return XaResult.success()


@app.route('/job_instance/stop', methods=['POST'])
def stop():
    name = request.values['name'] if 'name' in request.values else ''
    extendJobDefine = JobDefine.objects((Q(name=name))).first()

    if extendJobDefine is None:
        return XaResult.error(msg=u'请提供正确且存在的任务名称')

    try:
        scheduler.remove_job(id=name)
        app.logger.info(u'%s 任务停止成功！', name)
    except KeyError, e:
        app.logger.error(u'%s 任务停止遇到错误，错误信息：%s', name, e.message)

    JobDefine.objects(name=name).update_one(isRun=False)
    return XaResult.success()



