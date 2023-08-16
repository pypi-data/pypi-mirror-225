# _*_ coding: utf-8 _*_
# @Time : 2023/2/23
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : common-lingxing-sign-api
# @Desc :
import copy
import time
import urllib
from typing import Union

import requests
from orjson import orjson
from digiCore.utils import EncryptTool
from digiCore.model import ErrorEnum, UrlEnum
from digiCore import Decorate


class SignBase(object):

    @classmethod
    def generate_sign(cls, encrypt_key: str, request_params: dict) -> str:
        """
        生成签名
        """
        canonical_querystring = cls.format_params(request_params)
        md5_str = EncryptTool.md5_encrypt(canonical_querystring).upper()
        sign = EncryptTool.aes_encrypt(encrypt_key, md5_str)
        return sign

    @classmethod
    def format_params(cls, request_params: Union[None, dict] = None) -> str:
        """
        格式化 params
        """
        if not request_params or not isinstance(request_params, dict):
            return ''

        canonical_strs = []
        sort_keys = sorted(request_params.keys())
        for k in sort_keys:
            v = request_params[k]
            if v == "":
                continue
            elif isinstance(v, (dict, list)):
                # 如果直接使用 json, 则必须使用separators=(',',':'), 去除序列化后的空格, 否则 json中带空格就导致签名异常
                # 使用 option=orjson.OPT_SORT_KEYS 保证dict进行有序 序列化(因为最终要转换为 str进行签名计算, 需要保证有序)
                canonical_strs.append(f"{k}={orjson.dumps(v, option=orjson.OPT_SORT_KEYS).decode()}")
            else:
                canonical_strs.append(f"{k}={v}")
        return "&".join(canonical_strs)


class OpenApi(object):
    """"
    获取 sign签名，完成必要参数的获取
    返回字典数据
    data = {
            'api_name': self.api_name, # 传参
            'params': params,
            'lingxing_api': full_api
        }
    :param api_route 领星开发文档的接口路由地址，通过数据库dim_lingxing_api_info_a_mannal 可以查看
    :param access_token 领星接口数据请求 必须参数
    :param app_id   获取 access_token 的必须参数
    :param secret_key   获取 access_token 的必须参数
    """

    def __init__(self,
                 req_body: dict,
                 api_route: str,
                 access_token: str
                 ):
        self.req_body = req_body
        self.api_route = api_route
        self.access_token = access_token
        self.app_id = "ak_lFD8lAGGV0BCi"
        self.base_url = "https://openapi.lingxing.com/erp/sc"

    def get_req_params(self, req_params=None):
        """
        根据传参进行签名，并将签名加入到参数中
        :param req_params:
        :return:
        """
        req_params = req_params or {}
        gen_sign_params = copy.deepcopy(self.req_body) if self.req_body else {}
        if req_params:
            gen_sign_params.update(req_params)

        sign_params = {
            "app_key": self.app_id,
            "access_token": self.access_token,
            "timestamp": f'{int(time.time())}'
        }
        gen_sign_params.update(sign_params)
        sign = SignBase.generate_sign(self.app_id, gen_sign_params)
        sign_params["sign"] = sign
        req_params.update(sign_params)
        return req_params

    def get_full_api_url(self, params):
        """
        获取完整的怕拼接url
        :param params: 经过sign签名获取到的参数字典
        :return:
        """
        base_url = self.base_url + self.api_route
        str_params = urllib.parse.urlencode(params)
        return f'{base_url}?{str_params}'

    def get_lingxing_api(self):
        """
        返回接口请求数据
        :return: dict
        """

        params = self.get_req_params()
        full_api = self.get_full_api_url(params)
        data = {
            'params': params,
            'lingxing_api': full_api
        }
        return data

    @Decorate.def_retry('请求lingxing api失败！', error_type={})
    def sync_lingxing_data(self, api, param_data):
        """
        请求lingxing_api，获取response
        :return:
        """
        headers = UrlEnum.headers
        response = requests.post(url=api, headers=headers, json=param_data, timeout=20).json()
        return response
