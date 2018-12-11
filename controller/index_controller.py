# coding:utf-8

from app import app
from flask import render_template


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

