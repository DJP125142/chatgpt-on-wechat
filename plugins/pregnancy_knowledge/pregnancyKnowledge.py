# encoding:utf-8

import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
import re
from datetime import datetime, timedelta
import pytz



@plugins.register(
    name="PregnancyKnowledge",
    desire_priority=10,
    namecn="孕期知识推送",
    desc="A plugin for pregnancy knowledge push",
    version="1.0",
    author="jasper",
)

class PregnancyKnowledge(Plugin):
    def __init__(self):
        super().__init__()
        # 注册收到消息前置处理方法
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context

    # 帮助指引
    def get_help_text(self, **kwargs):
        help_text = f"发送【孕期第n周】获取相应的孕期知识。"
        return help_text

    # 收到消息前置处理
    def on_handle_context(self, e_context: EventContext):
        # 只处理文字消息
        if e_context["context"].type != ContextType.TEXT:
            return
        # 过滤掉内容的头尾空白符
        content = e_context["context"].content.strip()
        logger.debug(f"[PregnancyKnowledge] on_handle_context. content: {content}")

        if content.startswith("孕期第"):
            pregnancy_knowledge = ""
            week = 1
            # 计算孕期
            if content == "孕期第n周":
                conf = super().load_config()
                due_date = conf['due_date']
                days_until_due_date, current_pregnancy_week, current_pregnancy_day = self.calculatePregnancyDetails(
                    due_date)
                pregnancy_knowledge += f"我的小宝贝呀，当前孕{current_pregnancy_week}周{current_pregnancy_day}天，离预产期{days_until_due_date}天\n\n"
                week = current_pregnancy_week

            # 指定孕期
            match = re.search(r'孕期第(\d+|[零一二三四五六七八九十百]+)周', content)
            if match:
                week_str = match.group(1)
                if week_str.isdigit():
                    week = int(week_str)
                else:
                    week = self.chinese_to_arabic(week_str)

            reply = Reply()
            pregnancy_knowledge += self.getPregnancyKnowledge(week)
            result = pregnancy_knowledge
            if result is not None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "获取失败,等待修复⌛️"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS



    def getPregnancyKnowledge(self,week):
        # 获取当前脚本的目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接文件的绝对路径
        file_path = os.path.join(script_dir, 'pregnancy_knowledge.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["pregnancy_knowledge"].get(str(week), "该周没有相关信息")

    # 函数：将汉字数字转换为阿拉伯数字
    def chinese_to_arabic(self,chinese):
        chinese_numerals = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10
        }
        result = 0
        temp = 0
        unit = 1

        for char in chinese:
            if char in chinese_numerals:
                num = chinese_numerals[char]
                if num == 10:
                    if temp == 0:
                        temp = 1
                    result += temp * num
                    temp = 0
                    unit = 1
                else:
                    temp = temp * 10 + num
            else:
                result += temp * unit
                temp = 0
                unit = 1

        result += temp * unit
        return result

    def calculatePregnancyDetails(self,due_date_str):
        # 定义北京时间时区
        beijing_tz = pytz.timezone('Asia/Shanghai')

        # 将预产期字符串解析为datetime对象，并设置为北京时间
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").replace(tzinfo=beijing_tz)

        # 获取今天的日期，并设置为北京时间
        today = datetime.now(beijing_tz)

        # 计算距离预产期的天数
        days_until_due_date = (due_date - today).days + 1

        # 计算孕期开始的日期（预产期前40周）
        pregnancy_start_date = due_date - timedelta(weeks=40)

        # 计算今天距离孕期开始的天数
        days_since_start = (today - pregnancy_start_date).days

        # 计算当前孕期的周数和天数
        current_pregnancy_week = days_since_start // 7
        current_pregnancy_day = days_since_start % 7

        return days_until_due_date, current_pregnancy_week, current_pregnancy_day