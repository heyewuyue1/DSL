from pydantic import BaseModel

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
        self.user_list[token] = "main"
        return self.tree["main"]["Speak"]


    def handle_message(self, msg_req: MessageRequest) -> str:
        if self.tree[self.user_list[msg_req.token]].get("Hear"):  # 如果当前状态有Hear属性
            next_status = self.tree[self.user_list[msg_req.token]]["Hear"].get(msg_req.message)
            if next_status:
                self.user_list[msg_req.token] = next_status
            else:
                next_status = self.tree[self.user_list[msg_req.token]].get("Default")
                if next_status: 
                    self.user_list[msg_req.token] = next_status
                else:
                    return ""
            if self.tree[next_status].get("Speak"): 
                return self.tree[next_status]["Speak"]
        return ""
        