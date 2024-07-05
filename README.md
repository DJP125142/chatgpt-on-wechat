# 简介

> chatgpt-on-wechat（简称CoW）项目是基于大模型的智能对话机器人，支持微信公众号、企业微信应用、飞书、钉钉接入，可选择GPT3.5/GPT4.0/Claude/Gemini/LinkAI/ChatGLM/KIMI/文心一言/讯飞星火/通义千问/LinkAI，能处理文本、语音和图片，通过插件访问操作系统和互联网等外部资源，支持基于自有知识库定制企业AI应用。

### 原项目地址和快速开始文档：

#### 查阅chatgpt-on-wechat文档中的[项目简介](https://github.com/zhayujie/chatgpt-on-wechat#%E7%AE%80%E4%BB%8B) 和 [快速开始](https://github.com/zhayujie/chatgpt-on-wechat#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

## 此仓库支持功能如下：
-  ✅   **【bug修复】：** 修复了openai偶发的返回response为str类型时解析报错问题
-  ✅   **【多端启动】：** 新增了两个入口文件和配置文件支持同时启动微信号和公众号
-  ✅   **【bug修复】：** 修复了itchat无法发送webp格式图片问题
-  ✅   **【定时任务】：** 新增了定时任务插件timetask
-  ✅   **【KFC文案】：** 新增了随机生成KFC疯狂星期四文案生成器插件
-  ✅   **【常用工具】：** 新增了通过Apilot api查询早报、热榜、快递、天气等实用信息的插件
-  ✅   **【画图插件】：** 新增了replicate api画图的插件（因为openai的dall-e-3的画图经常失败）