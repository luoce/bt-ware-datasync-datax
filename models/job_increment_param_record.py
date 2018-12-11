#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from app import db


class JobIncrementParamRecord(db.Document):
    jobName = db.StringField(max_length=255, required=True)
    fromInstance = db.StringField()     # 来自哪个job实例
    incrementParam = db.StringField(max_length=255, required=True)
    incrementVal = db.StringField(max_length=255, required=True)    # 增量参考值建议都采用最后修改时间，便于更新、逻辑删除的处理
    recordingTime = db.DateTimeField(default=datetime.datetime.now, required=True)
