#!/usr/bin/env python
# -*- coding: utf-8 -*-
from apscheduler.triggers.cron import CronTrigger
from mongoengine import Q

from app import app, scheduler
from controller import job_define_controller
from controller import job_instance_controller
from controller import index_controller
from controller import job_increment_param_record_controller
from controller import job_task_load
from models.job_define import JobDefine

if __name__ == '__main__':
    app.run(debug=False)


