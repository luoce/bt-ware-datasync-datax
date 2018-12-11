#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 启动时加载数据库中标记为   运行中  的job
from apscheduler.triggers.cron import CronTrigger
from mongoengine import Q

from app import scheduler, app
from controller import job_task_load
from models.job_define import JobDefine

jobDefines = JobDefine.objects(Q(isDelete=False) & Q(isRun=True))
if jobDefines:
    for jobDefine in jobDefines:
        cron = CronTrigger.from_crontab(jobDefine.jobCron)
        scheduler.add_job(id=jobDefine.name, func=job_task_load.to_job_instance, trigger=cron, args=(jobDefine.name,))
        JobDefine.objects(name=jobDefine.name).update_one(isRun=True)
        app.logger.info(u'%s 任务已启动，已在服务启动时加载成功！', jobDefine.name)
else:
    app.logger.info(u'在服务启动时，并没有发现需要加载的Job！')