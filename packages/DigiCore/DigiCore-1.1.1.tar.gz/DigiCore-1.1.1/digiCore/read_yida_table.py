# _*_ coding:utf-8 _*_
import json
from typing import List

from alibabacloud_dingtalk.yida_1_0.client import Client as dingtalkyida_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.yida_1_0 import models as dingtalkyida__1__0_models
from alibabacloud_tea_util import models as util_models


class ReadYidaTable():
    """
    读取宜搭表格数据
    : access_token:钉钉access_token
    : user_id
    : app_type
    : system_token
    : page_size
    : form_uuid
    """

    @staticmethod
    def create_client() -> dingtalkyida_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkyida_1_0Client(config)

    @staticmethod
    def read_yida_table(
            app_type: str = "",
            system_token: str = "",
            access_token: str = "",
            user_id: str = "",
            form_uuid: str = "",
            current_page: int = 1,
            page_size: int = 100,
            data: list = [],
            language: str = "en_US",
            dynamic_order: str = '{}'
    ) -> list:
        """
        获取宜搭表格所有数据
        :param app_type: 应用编码（必传）
        :param system_token: 应用密钥（必传）
        :param access_token: 钉钉应用访问凭证（必传）
        :param user_id: 钉钉用户userid（必传）
        :param form_uuid: 表单id（必传）
        :param current_page:分页参数,当前页（默认第一页开始）
        :param page_size:每页显示条数（最多100）
        :param data:[]
        :param language:语言，默认英文
        :param dynamic_order:指定排序字段

        """
        client = ReadYidaTable.create_client()
        search_form_datas_headers = dingtalkyida__1__0_models.SearchFormDatasHeaders()
        search_form_datas_headers.x_acs_dingtalk_access_token = access_token
        search_form_datas_request = dingtalkyida__1__0_models.SearchFormDatasRequest(
            app_type=app_type,
            system_token=system_token,
            user_id=user_id,
            language=language,
            form_uuid=form_uuid,
            current_page=current_page,
            page_size=page_size,
            dynamic_order=dynamic_order
        )
        try:
            response = client.search_form_datas_with_options(search_form_datas_request, search_form_datas_headers,
                                                             util_models.RuntimeOptions())
            res = response.body.to_map()
            total_count = res.get('totalCount')
            data += res.get('data')
            if len(data) < total_count:
                ReadYidaTable.read_yida_table(app_type, system_token, access_token, user_id, form_uuid,
                                              current_page + 1,
                                              page_size, data)
            return data
        except Exception as err:
            return []
