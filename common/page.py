#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Page(object):
    def __init__(self, has_next=False, has_prev=False, pages=0, next_num=0, prev_num=0, total=0, items=None):
        self.items = items
        self.total = total
        self.prev_num = prev_num
        self.pages = pages
        self.has_prev = has_prev
        self.has_next = has_next
        self.next_num = next_num
        self.has_next = has_next

    def json_serialize(self):
        return {
            'has_next': self.has_next,
            'has_prev': self.has_prev,
            'pages': self.pages,
            'next_num': self.next_num,
            'prev_num': self.prev_num,
            'total': self.total,
            'items': self.items
        }

    @staticmethod
    def from_paginate(paginate):
        return Page(has_next=paginate.has_next, has_prev=paginate.has_prev, pages=paginate.pages,
                    next_num=paginate.next_num, prev_num=paginate.prev_num, total=paginate.total,
                    items=paginate.items)
