#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import logging
from flask_mongoengine import MongoEngine
from flask_apscheduler import APScheduler
from config import Config

app = Flask(__name__, static_folder='../static/assets', template_folder='../templates')

app.config.from_object(Config)

handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='UTF-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

app.logger.setLevel(app.config['LOG_LEVEL'])


db = MongoEngine(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()





