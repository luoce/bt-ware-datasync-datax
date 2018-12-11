#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time

import datetime

import operator
from flask import render_template, jsonify
from flask import request, session
from mongoengine import Q

from app import app
from common.datatable_result import DataTableResult
from common.xa_result import XaResult
from common.string_util import StringUtil
from common.json_util import JsonUtil
from models.job_define import JobDefine
from models.job_increment_param_record import JobIncrementParamRecord
from models.job_instance import JobInstance
from common.page import Page
from app import scheduler
import uuid
from models.job_instance import JobInstance


@app.route('/job_instance', methods=['GET'])
def to_job_instance():
    return render_template('job_instance.html')


@app.route('/job_instance/list', methods=['POST'])
def instanclist():
    display_start = int(request.form['iDisplayStart']) if 'iDisplayStart' in request.form else 1
    per_page = int(request.form['iDisplayLength']) if 'iDisplayLength' in request.form else 10

    page = display_start / per_page

    search = request.form['sSearch'] if 'sSearch' in request.form else ''

    limit_time = time.mktime((datetime.datetime.now() - datetime.timedelta(days=3)).timetuple()) * 1000

    q_list = [Q(executeTime__gt=limit_time)]

    if StringUtil.isNotBlank(search):
        q_list.append(Q(name__contains=search))

    jobInstances = JobInstance.objects(reduce(operator.and_, q_list)).order_by('-executeTime').paginate(
        page=page + 1 if page > 0 else 1, per_page=per_page)
    return DataTableResult.format(Page.from_paginate(jobInstances).json_serialize())


@app.route('/job_instance/get', methods=['POST'])
def instance_getone():
    instanceId = request.values['instanceId'] if 'instanceId' in request.values else ''
    jobInstance = JobInstance.objects((Q(instanceId=instanceId))).first()
    if jobInstance is None:
        return XaResult.error(msg=u'任务实例不存在')
    return XaResult.success(jobInstance)


