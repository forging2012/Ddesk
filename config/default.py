# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = False

    # Status
    QUESTION_STATUS = {0: '待确认', 1: '待处理', 2: '处理中', 3: '已完结'}
    DEMAND_STATUS = {100: '不实现', 1: '待确认', 2: '待调研', 3: '产品排期中', 4: '设计中', 5: '研发排期中', 6: '研发实现中',
                     9: '搁置', 10: '已实现'}
