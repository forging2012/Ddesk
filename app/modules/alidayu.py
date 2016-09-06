# -*- coding: utf-8 -*-
"""
SDK for alidayu

requires: python3.x, requests

@author: raptor.zh@gmail.com

__Edit author__ = 'Zhipeng Du'
__mtime__ = '16/9/5' '15:06'

"""
import requests
import hashlib
from time import time
import json
import logging

logger = logging.getLogger(__name__)


class RestApi:
    def __init__(self, key, secret, sms_free_sign_name, url="https://gw.api.tbsandbox.com/router/rest",
                 sms_type='normal', partner_id=""):
        self.key = key
        self.secret = secret
        self.sms_type = sms_type
        self.sms_free_sign_name = sms_free_sign_name
        self.url = url
        self.partner_id = partner_id

    def sign(self, params):
        #===========================================================================
        # '''签名方法
        # @param parameters: 支持字典和string两种
        # '''
        #===========================================================================
        if isinstance(params, dict):
            params = "".join(["".join([k, v]) for k,v in sorted(params.items())])
            params = "".join([self.secret, params, self.secret])
        sign = hashlib.md5(params.encode("utf-8")).hexdigest().upper()
        return sign

    def send_sms(self, rec_num, sms_template_code, sms_param):
        sys_params = {
            "method": "alibaba.aliqin.fc.sms.num.send",
            "app_key": self.key,
            "timestamp": str(int(time() * 1000)),
            "format": "json",
            "v": "2.0",
            "partner_id": self.partner_id,
            "sign_method": "md5",
            'sms_type': self.sms_type,
            'sms_free_sign_name': self.sms_free_sign_name,
            'rec_num': rec_num,
            'sms_template_code': sms_template_code,
            'sms_param': str(sms_param)}
        sign_params = sys_params.copy()
        sys_params['sign'] = self.sign(sign_params)
        headers = {
                 'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                 "Cache-Control": "no-cache",
                 "Connection": "Keep-Alive",
        }
        logger.debug(json.dumps(sys_params))
        r = requests.post(self.url, params=sys_params, headers=headers)
        r.raise_for_status()
        return r.json()

