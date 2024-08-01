import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

@plugins.register(name="Olympic",
                  desc="巴黎奥运会金牌榜",
                  version="1.0",
                  author="Jasper",
                  desire_priority=100)
class Olympic(Plugin):
    content = None

    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【奥运会金牌榜】查看实时金牌榜"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()

        if self.content in ["奥运会金牌榜", "金牌榜"]:
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.GetOlympicMedal()
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

    def GetOlympicMedal(self):
        conf = super().load_config()
        url = conf['api_host']
        params = {"year_city":"paris-2024"}
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            response = requests.get(url=url, params=params, headers=headers, timeout=2)
            if response.status_code == 200:
                json_data = response.json()
                logger.info(f"接口返回的数据：{json_data}")
                if json_data.get('codeid') == 10000 and json_data.get('retdata'):
                    medal = json_data['retdata']
                    result = []
                    text = "2024巴黎奥运会金牌榜\n"
                    for index, item in enumerate(medal[:20], start=1):
                        result.append(
                            f"No.{index} {item['country']}\n🏅{item['olympic_gold']} 🥈{item['olympic_silver']} 🥉{item['olympic_bronze']}\n")

                    resultStr = "".join(result)
                    text += resultStr
                    logger.info(f"主接口获取成功：{text}")
                    return text
                else:
                    logger.error(f"主接口返回值异常:{json_data}")
                    raise ValueError('not found')
            else:
                logger.error(f"主接口请求失败:{response.text}")
                raise Exception('request failed')
        except Exception as e:
            logger.error(f"接口异常：{e}")
        logger.error("所有接口都挂了,无法获取")
        return None

if __name__ == "__main__":
    olympic_plugin = Olympic()
    result = olympic_plugin.GetOlympicMedal()
    if result:
        print("获取到的文案内容：", result)
    else:
        print("获取失败")

