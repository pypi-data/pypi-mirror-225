# _*_ coding:utf-8 _*_
from loguru import logger
import json
import requests
from .model import Text, TextMsg, AtMobile, Markdown, MarkdownMsg, Link, LinkMsg
from digiCore import Decorate


class SendToGroup():
    """
    1、将消息发送到群
    2、消息类型包括
    文本、链接、markdown
    3、对于预警类消息，需要规范消息体结构（即校验参数）
    """
    def __init__(self, webhook: str):
        self.webhook = webhook

    def send_text(self, msg, at_mobiles=None):
        """
        发送文本类型消息
        msg: (1)str
            (2)dict
        msg需要包含以下字段
                project_title:str  项目介绍,
                subserver:str 子服务名称，
                msg:消息内容 + 群机器人指定关键字
        at_mobiles: list 需要at的人电话
        """
        if at_mobiles is None:
            at_mobiles = []
        if not msg:
            logger.info('参数缺失')
            return
        if isinstance(msg, dict):
            msg: TextMsg.construct()
            msg = json.dumps(dict(msg), indent=4, ensure_ascii=False)

        at = AtMobile.construct()
        at.atMobiles = at_mobiles

        text = Text.construct()
        text.text = {"content": msg}
        text.at = dict(at)

        data = dict(text)
        if self.post_message(data):
            logger.info('消息发送成功！')

    def send_markdown(self, msg=None, at_mobiles=None):
        """
        发送markdown类型的文件
        msg:dict 消息内容
        msg需要包含以下字段
            title： str
            text: str markdown格式的文本+ 群机器人指定关键字
        at_mobiles: list 需要at的人电话
        """
        if at_mobiles is None:
            at_mobiles = []
        if msg is None:
            msg = {}
        if not msg:
            logger.info('参数缺失')
            return
        msg: MarkdownMsg.construct()

        at = AtMobile.construct()
        at.atMobiles = at_mobiles

        markdown = Markdown.construct()
        markdown.markdown = dict(msg)
        markdown.at = dict(at)

        data = dict(markdown)

        if self.post_message(data):
            logger.info('消息发送成功！')

    def send_link(self, msg=None):
        """
        发送链接消息
        msg: dict 消息内容
        msg需要包含以下字段
            text:str,   文本 + 群机器人指定关键字
            title:str,  标题
            picUrl: str,    图片链接
            messageUrl:str 链接的文字链接
        """
        if msg is None:
            msg = {}
        if not msg:
            logger.info('参数缺失')
            return
        link = Link.construct()
        msg: LinkMsg()
        link.link = dict(msg)

        data = dict(link)
        if self.post_message(data):
            logger.info('消息发送成功！')

    @Decorate.def_retry(msg="消息发送失败，正在重试！")
    def post_message(self, data: dict):
        """
        调用发送消息接口
        data:dict 通过接口发送的消息，包含消息类型和消息体
        """
        headers = {'Content-Type': 'application/json'}
        data_new = json.dumps(data, indent=4, ensure_ascii=False).encode()
        r = requests.post(url=self.webhook, headers=headers, data=data_new)
        text = json.loads(r.text)
        error_code = text.get('errcode')
        if error_code != 0:
            logger.info(text.get('errmsg'))
            return
        logger.info(json.dumps(data, indent=4, ensure_ascii=False))
        return r.text
