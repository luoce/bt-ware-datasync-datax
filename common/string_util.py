#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StringUtil(object):
    @staticmethod
    def isNotBlank(s):
        if s.strip() == '':
            return False
        return True

    @staticmethod
    def isBlank(s):
        return not StringUtil.isNotBlank(s)

