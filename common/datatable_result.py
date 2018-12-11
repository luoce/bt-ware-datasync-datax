#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify


success_res = dict()
error_res = dict()


class DataTableResult(object):
    @staticmethod
    def format(data=None):
        success_res['aaData'] = data['items']
        success_res['iTotalRecords'] = data['total']
        success_res['iTotalDisplayRecords'] = data['total']
        return jsonify(success_res)
