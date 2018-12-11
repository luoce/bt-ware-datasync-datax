#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import logging

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # MongoDB 配置
    MONGODB_SETTINGS = {'db': 'datasync_datax',
                        'host': '192.168.100.85',
                        'port': 27017
                        }
    # 启动调度任务Api
    SCHEDULER_API_ENABLED = True

    # DataX 任务脚本存放目录
    DATAX_JOB_JSON_FILE_PATH = '/Users/huan/software/datax/job/'

    # DataX 运行文件目录
    DATAX_PY_PATH = '/Users/huan/software/datax/bin/datax.py'

    # 日志目录
    LOG_FILE_PATH = '/Users/huan/sources/python-sources/bt-ware-datasync-datax/bt-ware-datasync-datax.log'

    # 日志级别
    LOG_LEVEL = logging.DEBUG
