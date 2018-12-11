#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import time
import uuid

from apscheduler.triggers.cron import CronTrigger
from mongoengine import Q

from app import app, scheduler
from models.job_define import JobDefine
from models.job_increment_param_record import JobIncrementParamRecord
from models.job_instance import JobInstance


def to_job_instance(jobName=None):
    app.logger.info(u'%s 准备开始运行', jobName)
    extendJobDefine = JobDefine.objects((Q(name=jobName))).first()

    if extendJobDefine is None:
        app.logger.error(u'%s 任务定义不存在，执行失败', jobName)
        return

    # job json 增量参数替换
    jobJson = extendJobDefine.defJson
    if extendJobDefine.isIncrement:
        app.logger.info(u'%s 任务是增量任务', jobName)
        # 找到增量参数最大值
        jobIncrementParamRecord = JobIncrementParamRecord.objects(Q(jobName=extendJobDefine.name) &
                                                                  Q(incrementParam=extendJobDefine.incrementParam)
                                                                  ).order_by('-recordingTime').first()

        # 增量参数没有记录，则使用job定义的起始值
        if not jobIncrementParamRecord:
            jobJson = jobJson.replace(extendJobDefine.incrementParam, extendJobDefine.incrementParamStart)
            app.logger.info(u'%s 任务是增量任务，但没找到增量参数最大值，因此使用job定义的起始值 %s', jobName, extendJobDefine.incrementParamStart)
        else:
            jobJson = jobJson.replace(extendJobDefine.incrementParam, jobIncrementParamRecord.incrementVal)
            app.logger.info(u'%s 任务是增量任务，找到了增量参数最大值 %s', jobName, jobIncrementParamRecord.incrementVal)

    # 将job json存入文件，执行job并记录instance记录和执行记录
    newInstanceUUID = str(uuid.uuid1())
    app.logger.info(u'%s 任务生成唯一实例标识 %s， 并开始写入json文件', jobName, newInstanceUUID)

    jsonFilePath = app.config['DATAX_JOB_JSON_FILE_PATH'] + newInstanceUUID + '.json'
    jsonFile = open(jsonFilePath, 'w')
    jsonFile.write(jobJson)
    jsonFile.close()

    app.logger.info(u'%s 任务写入json文件完成，目录为：%s', jobName, jsonFilePath)

    localTime = time.localtime()
    fmtTime = time.strftime('%Y-%m-%d %H:%M:%S', localTime)  # 时间往前提，尽量覆盖同步任务执行时产生的新数据

    # 组织Datax的执行命令
    datax_execute_cmd = app.config['DATAX_PY_PATH'] + ' ' + jsonFilePath

    execute_time = time.time() * 1000

    # 精髓所在就在这一句了
    try:
        (status, output) = commands.getstatusoutput(datax_execute_cmd)
        app.logger.info(u'%s 任务执行完成status= %s', jobName, status)
    except KeyError, e:
        app.logger.error(u'%s 任务执行时出现异常 %s', jobName, e.message)
        status = -20
        output = e.message

    end_time = time.time() * 1000

    newJobInstance = JobInstance(instanceId=newInstanceUUID, jobName=jobName,
                                 jobDisplayName=extendJobDefine.displayName,
                                 jobJson=jobJson, jobJsonPath=jsonFilePath, result=status, executeOutput=output,
                                 executeTime=execute_time, endTime=end_time)

    newJobIncrementParamRecord = JobIncrementParamRecord(jobName=extendJobDefine.name, fromInstance=newInstanceUUID,
                                                         incrementParam=extendJobDefine.incrementParam,
                                                         incrementVal=fmtTime)

    try:
        newJobInstance.save()
        newJobIncrementParamRecord.save()
    except KeyError, e:
        app.logger.error(u'%s 任务执行完成，但记录保存时出现错误: %s', jobName, e.message)



