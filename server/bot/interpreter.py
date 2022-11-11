from pydantic import BaseModel
from bot.parser import WaitType
import re


class MessageRequest(BaseModel):
    token: str
    message: str


class RuntimeError(Exception):
    def __init__(self, _msg: str) -> None:
        self.msg = _msg


class Robot(object):
    def __init__(self, _tree: dict) -> None:
        self.user_list = {}
        self.tree = _tree
        if self.tree.get("main") == None:
            raise RuntimeError("No main status to begin with.")

    def add_user(self, token: str) -> str:
        user_info = {
            "status": "main",
            "__GLOBAL__": {}
        }
        user_info["__GLOBAL__"] = self.tree["__GLOBAL__"]
        self.user_list[token] = user_info
        for var in self.tree["main"]["Operate"]:
            self.user_list[token]["__GLOBAL__"][var] = self.tree["main"]["Operate"][var]
        print(self.user_list[token]["__GLOBAL__"])
        message = ""
        wait = WaitType.Forever
        if self.tree["main"].get("Speak"):
            message = self.tree["main"]["Speak"]
            for var in self.user_list[token]["__GLOBAL__"]:
                message = message.replace(var, str(self.user_list[token]["__GLOBAL__"][var]))
        if self.tree["main"].get("Wait"):
            wait = self.tree["main"]["Wait"]
        return {"wait": wait, "message": message}

    def handle_message(self, msg_req: MessageRequest) -> dict:
        transfer = True
        # 先决定接受到这条消息之后转移到哪个状态
        if msg_req.message == "!!!timeout":
            next_status = self.tree[self.user_list[msg_req.token]["status"]]["Timeout"]
            self.user_list[msg_req.token]["status"] = next_status
        # 先看有没有Hear属性
        elif self.tree[self.user_list[msg_req.token]["status"]].get("Hear"):
            next_status = None
            for pattern in self.tree[self.user_list[msg_req.token]["status"]]["Hear"]:
                if (re.match(pattern, msg_req.message)):
                    next_status = self.tree[self.user_list[msg_req.token]["status"]]["Hear"][pattern]
            if next_status:  # 再看是否是Hear接受的输入
                self.user_list[msg_req.token]["status"] = next_status
            else:  # 如果不是Hear接受的输入
                next_status = self.tree[self.user_list[msg_req.token]["status"]].get(
                    "Default")
                if next_status:   # 再看有没有Default属性
                    self.user_list[msg_req.token]["status"] = next_status
                else:  # 没有default就不转移状态
                    next_status = self.user_list[msg_req.token]
                    transfer = False
        else:  # 如果没有Hear
            next_status = self.tree[self.user_list[msg_req.token]["status"]].get(
                "Default")
            if next_status:   # 看有没有Default属性
                self.user_list[msg_req.token]["status"] = next_status
            else:  # 没有default就不转移状态
                next_status = self.user_list[msg_req.token]
                transfer = False

        for var in self.tree[next_status]["Operate"]:
            self.user_list[msg_req.token]["__GLOBAL__"][var] = self.tree[next_status]["Operate"][var]
        # 再决定返回什么值
        message = ""
        wait = WaitType.Forever
        if transfer and self.tree[next_status].get("Speak"):
            message = self.tree[next_status]["Speak"]
            print(self.user_list[msg_req.token])
            for var in self.user_list[msg_req.token]["__GLOBAL__"]:
                message = message.replace(var, str(self.user_list[msg_req.token]["__GLOBAL__"][var]))
        if self.tree[next_status].get("Wait"):
            wait = self.tree[next_status]["Wait"]
        return {"wait": wait, "message": message}
