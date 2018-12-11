#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

from app import db


class JobInstance(db.Document):
    instanceId = db.StringField()
    jobName = db.StringField()
    jobDisplayName = db.StringField()
    jobJson = db.StringField()     # 来自哪个job实例
    jobJsonPath = db.StringField()
    result = db.IntField()
    executeOutput = db.StringField()    # 输出结果
    executeTime = db.DecimalField(default=time.time, required=True)    # 执行时间
    endTime = db.DecimalField(default=time.time, required=True)     #执行结束时间
