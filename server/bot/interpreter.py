'''
Description: 依照语法树解释执行机器人逻辑
Author: He Jiahao
Date: 2022-09-23 14:38:49
LastEditTime: 2022-11-17 21:25:07
'''


import re
from threading import Lock
from jose import jwt
import datetime


class Robot(object):
    '''
    description: Robot类的构造函数
    param {*} self
    param {dict} _tree 语法分析阶段生成的语法树
    return {*}
    '''

    def __init__(self, tree: dict) -> None:
        self.tree = tree
        self.user_var = {}
        self.mutex = Lock()

    '''
    description: 注册一次会话
    param {*} self
    param {str} key 用于加密token的密钥
    param {int} time_out 一次对话的有效时长
    return {*}
    '''

    def add_user(self, key: str, time_out: int) -> str:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=time_out),
            "iss": "DSLUser",
        }
        token = jwt.encode(payload, key)
        self.mutex.acquire()
        self.user_var[token] = {}
        self.mutex.release()
        return token

    '''
    description: 处理一条来自前端的信息
    param {*} self
    param {str} token 客户端发来的令牌
    param {str} status 客户端所处的状态
    param {str} message 客户端发来的信息
    param {str} key 用于解码token的密钥
    return {*}
    '''

    def handle_message(self, token: str, status: str, message: str, key: str) -> dict:
        # 如果会话已经过期
        try:
            data = jwt.decode(token, key)
            if data["iss"] != "DSLUser":
                return {}
        except:
            return {}
        is_transferred = True
        # 先决定接受到这条消息之后转移到哪个状态
        # 如果是超时消息，转移到Timeout状态
        if message == "_timeout_":
            next_status = self.tree[status]["Timeout"]
        # 如果是普通消息，匹配Hear语句中的正则表达式
        else:
            hear = self.tree[status].get("Hear")
            next_status = None
            for pattern in hear:
                if (re.match(pattern, message)):
                    next_status = hear[pattern]
                    break
            if not next_status:  # 如果不是Hear接受的输入，转移到Default状态
                next_status = self.tree[status].get("Default")
                if not next_status:  # 如果没有Default状态，不进行转移
                    next_status = status
                    is_transferred = False
        return self.handle_transfered(token, is_transferred, next_status, message)

    def handle_transfered(self, token: str, is_transferred: bool, next_status: str, message: str) -> dict:
        self.mutex.acquire()
        # 转移到新状态之后，先为变量赋值
        for i in self.user_var[token]:
            if (self.user_var[token][i] == "_text_"):
                self.user_var[token][i] = message
        for i in self.tree[next_status]["Operate"]:
            if self.tree[next_status]["Operate"][i] != "_text_":
                self.user_var[token][i] = self.tree[next_status]["Operate"][i]
        # 再决定等待时间和应答消息
        wait = self.tree[next_status]["Wait"]
        message = ""
        if is_transferred and self.tree[next_status].get("Speak"):
            message = self.tree[next_status]["Speak"]
        for i in self.user_var[token]:
            if self.user_var[token][i] != "_text_":
                message = message.replace(i, self.user_var[token][i])
        # 特殊处理值为"_text_"的变量
        for i in self.tree[next_status]["Operate"]:
            if self.tree[next_status]["Operate"][i] == "_text_":
                self.user_var[token][i] = self.tree[next_status]["Operate"][i]
        self.mutex.release()
        return {"status": next_status, "wait": wait, "message": message}
