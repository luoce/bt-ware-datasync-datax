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


@app.route('/job_increment_param_record', methods=['GET'])
def to_job_increment_param_record():
    return render_template('job_increment_param_record.html')


@app.route('/job_increment_param_record/list', methods=['POST'])
def increment_param_record_list():
    display_start = int(request.form['iDisplayStart']) if 'iDisplayStart' in request.form else 1
    per_page = int(request.form['iDisplayLength']) if 'iDisplayLength' in request.form else 10

    page = display_start / per_page

    search = request.form['sSearch'] if 'sSearch' in request.form else ''

    limit_time = (datetime.datetime.now() - datetime.timedelta(days=3))

    q_list = [Q(recordingTime__gt=limit_time)]
    if StringUtil.isNotBlank(search):
        q_list.append(Q(jobName__contains=search))

    jobIncrementParamRecords = JobIncrementParamRecord.objects(reduce(operator.and_, q_list)).order_by('-recordingTime').paginate(page=page + 1 if page > 0 else 1, per_page=per_page)
    return DataTableResult.format(Page.from_paginate(jobIncrementParamRecords).json_serialize())
