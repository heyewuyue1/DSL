'''
Description: 依照语法树解释执行机器人逻辑
Author: He Jiahao
Date: 2022-09-23 14:38:49
LastEditTime: 2022-11-13 15:33:04
'''
from pydantic import BaseModel
from bot.parser import WaitType
import re


class MessageRequest(BaseModel):
    token: str
    message: str


class RuntimeError(Exception):
    '''
    description: 用于报出解释执行阶段的错误
    param {*} self
    param {str} _msg 错误信息
    return {*}
    '''
    def __init__(self, _msg: str) -> None:
        self.msg = _msg


class Robot(object):
    '''
    description: Robot类的构造函数
    param {*} self
    param {dict} _tree 语法分析阶段生成的语法树
    return {*}
    '''
    def __init__(self, _tree: dict) -> None:
        self.user_list = {}
        self.tree = _tree
        self.user_cnt = 0
        

    '''
    description: 在Robot.user_list中注册一个指定token的用户
    param {*} self
    param {str} token 指定的token
    return {dict} 返回一个字典，代表"main"状态的执行结果
    '''
    def add_user(self, token: str) -> dict:
        user_info = {
            "status": "main",
            "__GLOBAL__": {}
        }
        user_info["__GLOBAL__"] = self.tree["__GLOBAL__"]
        self.user_list[token] = user_info
        for var in self.tree["main"]["Operate"]:
            self.user_list[token]["__GLOBAL__"][var] = self.tree["main"]["Operate"][var]
        message = ""
        wait = WaitType.Forever
        if self.tree["main"].get("Speak"):
            message = self.tree["main"]["Speak"]
            for var in self.user_list[token]["__GLOBAL__"]:
                message = message.replace(var, str(self.user_list[token]["__GLOBAL__"][var]))
        if self.tree["main"].get("Wait"):
            wait = self.tree["main"]["Wait"]
        self.user_cnt += 1
        return {"wait": wait, "message": message}

    '''
    description: 处理一条来自前端的消息
    param {*} self
    param {MessageRequest} msg_req 接收到的前端的消息
    return {dict} 返回一个字典，代表处理的结果
    '''
    def handle_message(self, msg_req: MessageRequest) -> dict:
        print (str(self.user_cnt))
        if not self.user_list.get(msg_req.token):
            return {"wait": WaitType.Forever, "message": "the conversation is over."}
        transfer = True
        # 先决定接受到这条消息之后转移到哪个状态
        # 如果是超时消息，转移到Timeout状态
        if msg_req.message == "!!!timeout":
            next_status = self.tree[self.user_list[msg_req.token]["status"]]["Timeout"]
            self.user_list[msg_req.token]["status"] = next_status
        # 如果是普通消息，匹配Hear语句中的正则表达式
        elif self.tree[self.user_list[msg_req.token]["status"]].get("Hear"):
            next_status = None
            for pattern in self.tree[self.user_list[msg_req.token]["status"]]["Hear"]:
                if (re.match(pattern, msg_req.message)):
                    next_status = self.tree[self.user_list[msg_req.token]["status"]]["Hear"][pattern]
                    break
            if next_status: 
                self.user_list[msg_req.token]["status"] = next_status
            else:  # 如果不是Hear接受的输入，转移到Default状态
                next_status = self.tree[self.user_list[msg_req.token]["status"]].get(
                    "Default")
                if next_status:   # 再看有没有Default属性
                    self.user_list[msg_req.token]["status"] = next_status
                else:  # 如果没有Default状态，不进行转移
                    next_status = self.user_list[msg_req.token]
                    transfer = False
        else:  # 如果没有Hear语句，直接转移到Default状态
            next_status = self.tree[self.user_list[msg_req.token]["status"]].get(
                "Default")
            if next_status:   # 看有没有Default属性
                self.user_list[msg_req.token]["status"] = next_status
            else:  # 没有default就不转移状态
                next_status = self.user_list[msg_req.token]
                transfer = False

        # 转移到新状态之后，先为变量赋值
        for var in self.tree[next_status]["Operate"]:
            self.user_list[msg_req.token]["__GLOBAL__"][var] = self.tree[next_status]["Operate"][var]
        # 再决定等待时间和应答消息
        message = ""
        wait = WaitType.Forever
        if transfer and self.tree[next_status].get("Speak"):
            message = self.tree[next_status]["Speak"]
            print(self.user_list[msg_req.token])
            for var in self.user_list[msg_req.token]["__GLOBAL__"]:
                message = message.replace(var, str(self.user_list[msg_req.token]["__GLOBAL__"][var]))
        if self.tree[next_status].get("Wait"):
            wait = self.tree[next_status]["Wait"]
        if not self.tree[next_status].get("Wait") and not self.tree[next_status].get("Default") and not self.tree[next_status].get("Hear"):
            self.user_cnt -= 1
            self.user_list.pop(msg_req.token)
        return {"wait": wait, "message": message}
