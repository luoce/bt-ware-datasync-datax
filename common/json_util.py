#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


class JsonUtil(object):

    @staticmethod
    def is_json(jsonStr):
        try:
            json.loads(jsonStr)
        except ValueError:
            return False
        return True

