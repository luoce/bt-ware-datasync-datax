#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from app import db


class JobDefine(db.Document):
    name = db.StringField(max_length=255, required=True)
    displayName = db.StringField()
    defJson = db.StringField()
    isIncrement = db.BooleanField()
    incrementParam = db.StringField(max_length=255)
    incrementParamStart = db.StringField(max_length=255)
    jobCron = db.StringField()
    createTime = db.DateTimeField(default=datetime.datetime.now, required=True)
    isDelete = db.BooleanField(default=False)
    isRun = db.BooleanField(default=False)


