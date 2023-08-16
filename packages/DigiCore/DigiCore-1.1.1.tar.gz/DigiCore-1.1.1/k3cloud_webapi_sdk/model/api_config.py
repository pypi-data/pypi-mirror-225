#!/usr/bin/python
# -*- coding:UTF-8 -*-


class ApiConfig:
    Xor_Code = ''

    def __init__(self):
        self.server_url = 'https://api.kingdee.com/galaxyapi/'
        self.dcid = ''
        self.user_name = ''
        self.app_id = ''
        self.app_secret = ''
        self.lcid = 2052
        self.org_num = 0
        self.connect_timeout = 120
        self.request_timeout = 120
        self.proxy = ''
