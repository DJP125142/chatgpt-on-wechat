# encoding:utf-8

import plugins
from plugins import *
from bridge.context import ContextType


@plugins.register(
    name="MbtiTest",
    desire_priority=10,
    namecn="MBTI人格测试",
    desc="A plugin for MBTI personality test",
    version="1.0",
    author="jasper",
)

class MbtiTest(Plugin):

    def __init__(self):
        super().__init__()
        # 注册收到消息前置处理方法
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context

    # 帮助指引
    def get_help_text(self, **kwargs):
        help_text = f"发送【MBTI测试】开始你的MBTI人格测试。"
        return help_text

    # 收到消息前置处理
    def on_handle_context(self, e_context: EventContext):
        # 只处理文字消息
        if e_context["context"].type != ContextType.TEXT:
            return
        # 过滤掉内容的头尾空白符
        content = e_context["context"].content.strip()
        logger.debug(f"[mbti] on_handle_context. content: {content}")

        if content in ["mbti测试", "MBTI测试"]:
            # 定义prompt
            prompt = "现在你是一个MBTI测试老师，我将会回答你的问题，进行我的人格测试，请你根据MBTI测试问题进行提问10个问题，并且最后分析得出我是一个怎样的人格"
            e_context["context"].type = ContextType.TEXT
            e_context["context"].content = prompt
            e_context.action = EventAction.BREAK  # 事件结束，不跳过处理context的默认逻辑

