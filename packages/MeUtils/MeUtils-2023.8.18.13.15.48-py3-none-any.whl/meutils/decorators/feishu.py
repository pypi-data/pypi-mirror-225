#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : notice
# @Time         : 2021/4/2 3:46 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 
"""注意事项
1. wrapped(*args, **kwargs)不要重复执行


todo:
feishu keras callback: 训练日志通知

"""
import requests

from meutils.pipe import *


def feishu_hook(title='Task Done', text=None, hook_url=None):
    """装饰器里不可变参数

    :param title:
    :param text: 如果为空，用函数返回值填充
    :param hook_url: hook_url或者群名称
    :return:
    """
    hook_url = hook_url or "https://open.feishu.cn/open-apis/bot/v2/hook/f7cf6f2a-30da-4e7a-ae6f-b48c8bb1ecf8"

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        s = time.time()
        r = wrapped(*args, **kwargs)
        e = time.time()

        mins = (e - s) // 60

        logger.info(f"{title} done in {mins} m")

        if text is None:  # text没法直接赋值
            body = {"title": title, "text": str(r) + f"\n耗时 {mins} m"}
        else:
            body = {"title": title, "text": text + f"\n耗时 {mins} m"}

        requests.post(hook_url, json=body).json()

        return r

    return wrapper


# def feishu_catch(hook_url=get_zk_config('/push/bot')['logger']):
#     hook_url = get_zk_config('/push/bot').get(hook_url, hook_url)
#     assert hook_url.startswith('http'), '请填入hook_url或群名称'
#
#     @wrapt.decorator
#     def wrapper(wrapped, instance, args, kwargs):
#         try:
#             return wrapped(*args, **kwargs)
#
#         except Exception as e:
#             text = traceback.format_exc()
#
#             body = {"title": f"Exception: {wrapped.__name__}", "text": text}
#             requests.post(hook_url, json=body).json()
#
#     return wrapper


if __name__ == '__main__':
    @feishu_hook('catch hook')
    # @feishu_catch()
    def f():
        # 1 / 0
        print(time.time())
        # return 'RES'


    m = {
        "msg_type": "interactive",
        "card": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": "**西湖**，位于浙江省杭州市西湖区龙井路1号，杭州市区西部，景区总面积49平方千米，汇水面积为21.22平方千米，湖面面积为6.38平方千米。",
                        "tag": "lark_md"
                    }
                },
                # {
                #     "actions": [{
                #         "tag": "button",
                #         "text": {
                #             "content": "更多景点介绍 :玫瑰:",
                #             "tag": "lark_md"
                #         },
                #         "url": "https://www.example.com",
                #         "type": "default",
                #         "value": {}
                #     }],
                #     "tag": "action"
                # }
            ],
            "header": {
                "title": {
                    "content": "今日旅游推荐",
                    "tag": "plain_text"
                }
            }
        }
    }


    class Text(BaseModel):
        content: str
        tag: str = 'lark_md'


    class Element(BaseModel):
        text: Text
        tag: str = 'div'


    class Header(BaseModel):
        title: Text


    class Card(BaseModel):
        header: Header

        elements: List[Element]


    class Message(BaseModel):
        """模拟 https://open.feishu.cn/tool/cardbuilder?from=apireference&templateId=ctp_AAmj6jORJix1"""
        msg_type: str = 'interactive'
        card: Card


    source = """
        <details markdown="1">
            <summary>详情</summary>

    - [ ] 功能点
        - [x] 接入非结构化文档（已支持 pdf、docx 文件格式）
        - [ ] 增加多级缓存缓存

        </details>
        """.strip()

    m = Message(
        card=Card(
            header=Header(title=Text(content='这是一个标题')),
            elements=[
                Element(text=Text(content='**南京**')),
                # Element(text=Text(content="at所有人<at id=all></at> \n 换行消息")),
                Element(text=Text(content=source)),

            ]
        )
    )
    m = {
        "msg_type": "post",
        "content": {
            "zh_cn": {
                "title": "我是一个标题",
                "content": [
                    [{
                        "tag": "text",
                        "text": "第一行 :"
                    },
                        {
                            "tag": "at",
                            "user_id": "ou_xxxxxx",
                            "user_name": "tom"
                        }
                    ],
                    [{
                        "tag": "text",
                        "text": "第二行:"
                    },
                        {
                            "tag": "at",
                            "user_id": "all",
                            "user_name": "所有人"
                        }
                    ]
                ]
            }
        }
    }

    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f7cf6f2a-30da-4e7a-ae6f-b48c8bb1ecf8"
    r = requests.post(url, json=dict(m))
    print(r.text)
