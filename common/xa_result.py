#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

success_res = dict()
error_res = dict()


class XaResult(object):
    @staticmethod
    def success(data=None):
        success_res['data'] = data
        success_res['level'] = 'success'
        success_res['title'] = 'Success'
        return jsonify(success_res)

    @staticmethod
    def error(msg=''):
        error_res['level'] = 'danger'
        error_res['title'] = 'Danger！'
        error_res['msg'] = msg
        return jsonify(error_res)
