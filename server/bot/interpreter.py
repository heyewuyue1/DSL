'''
Description: 依照语法树解释执行机器人逻辑
Author: He Jiahao
Date: 2022-09-23 14:38:49
LastEditTime: 2022-11-15 19:41:23
'''
import re

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
    def __init__(self, tree: dict) -> None:
        self.tree = tree

    '''
    description: 处理一条来自前端的消息
    param {*} self
    param {MessageRequest} msg_req 接收到的前端的消息
    return {dict} 返回一个字典，代表处理的结果
    '''
    def handle_message(self, status: str, message: str) -> dict:
        transfer = True
        # 先决定接受到这条消息之后转移到哪个状态
        if status == "_START_":
            next_status = "main"
        # 如果是超时消息，转移到Timeout状态
        elif message == "!!!timeout":
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
                    transfer = False

        # 转移到新状态之后，先为变量赋值
        if not self.tree.get(next_status):
            raise RuntimeError("Undefined status: " + next_status)
        var_assign = self.tree[next_status]["Operate"]
        # 再决定等待时间和应答消息
        wait = self.tree[next_status]["Wait"]
        message = ""
        if transfer and self.tree[next_status].get("Speak"):
            message = self.tree[next_status]["Speak"]
        return {"status": next_status, "wait": wait, "message": message, "var": var_assign}
