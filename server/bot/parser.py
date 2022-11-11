from bot.lexer import Token, TokenType
from enum import IntEnum
import warnings


class ParseError(Exception):
    def __init__(self, _msg: str) -> None:
        self.msg = _msg


class WaitType(IntEnum):
    Forever = 0
    Immediate = -1


class Parser(object):
    def __init__(self, token_list: list[Token]) -> None:
        self.current_status = ""
        self.idx = 0
        self._token_list = token_list
        self.tree = {
            "__GLOBAL__":{},
            "main":{
                 "Speak": "",
                "Wait": None,
                "Hear": {},
                "Default": "",
                "Timeout": "",
                "Operate":{}
            }
        }

    def parse_status(self) -> None:
        if self.current_status != "":
            self.status_check()
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.Status or self.idx >= len(self._token_list):
            raise ParseError("Expected a Status name.")
        if self._token_list[self.idx]._attr != "main":
            self.tree[self._token_list[self.idx]._attr] = {
                "Speak": "",
                "Wait": None,
                "Hear": {},
                "Default": "",
                "Timeout": "",
                "Operate":{}
            }
        self.current_status = self._token_list[self.idx]._attr
        self.idx += 1

    def parse_speak(self):
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.ConstStr or self.idx >= len(self._token_list):
            raise ParseError("Expected a string constant")
        self.tree[self.current_status]["Speak"] = self._token_list[self.idx]._attr
        self.idx += 1

    def parse_hear(self):
        self.idx += 1
        # 将来新增TokenType.condition
        if self._token_list[self.idx]._type != TokenType.ConstStr or self.idx >= len(self._token_list):
            raise ParseError("Expected a string constant")
        condition = self._token_list[self.idx]._attr
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.Status or self.idx >= len(self._token_list):
            raise ParseError("Expected a status to transfer")
        next_status = self._token_list[self.idx]._attr
        self.tree[self.current_status]["Hear"][condition] = next_status
        self.idx += 1

    def parse_wait(self):
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.ConstNum or self.idx >= len(self._token_list):
            raise ParseError("Expected a wait time.")
        if eval(self._token_list[self.idx]._attr) < 0:
            raise ParseError(
                "Wait time can only be an integer greater than 0.")
        self.tree[self.current_status]["Wait"] = eval(
            self._token_list[self.idx]._attr)
        self.idx += 1

    def parse_default(self):
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.Status or self.idx >= len(self._token_list):
            raise ParseError("Expected a default status")
        self.tree[self.current_status]["Default"] = self._token_list[self.idx]._attr
        self.idx += 1

    def parse_timeout(self):
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.Status or self.idx >= len(self._token_list):
            raise ParseError("Expected a timeout status")
        self.tree[self.current_status]["Timeout"] = self._token_list[self.idx]._attr
        self.idx += 1
    
    def parse_variable(self):
        id_name = self._token_list[self.idx]._attr
        self.idx += 1
        next_token = self._token_list[self.idx]
        # 在外部定义的全局变量
        if next_token._type == TokenType.Operator and next_token._attr == '=':
            self.idx += 1
            next_token = self._token_list[self.idx]
            if next_token._type == TokenType.ConstNum or next_token._type == TokenType.ConstStr:
                value = next_token._attr
                self.tree["__GLOBAL__"][id_name] = value
                op_state = self.current_status
                if op_state == "":
                    op_state = "main"
                self.tree[op_state]["Operate"][id_name] = value
                self.idx += 1
            else:
                raise ParseError("Expected a number or a string constant")
        else:
            self.tree["__GLOBAL__"][id_name] = None

    def status_check(self):
        wait = self.tree[self.current_status].get("Wait")
        if not wait and self.tree[self.current_status].get("Timeout"):
            warnings.warn('Status "'+self.current_status +
                          '" has to wait forever before goto the timeout status.', UserWarning)
        if wait and wait > 0 and not self.tree[self.current_status].get("Timeout"):
            raise ParseError('Status "'+self.current_status +
                             '" has a valid wait time but no Timeout status set.')
        if not self.tree[self.current_status].get("Speak"):
            warnings.warn('Status "'+self.current_status +
                          '" has nothing to speak.', UserWarning)

    def parse(self) -> dict:
        while self.idx < len(self._token_list):
            if self._token_list[self.idx]._attr == "Status":
                self.parse_status()
            elif self._token_list[self.idx]._attr == "Speak":
                self.parse_speak()
            elif self._token_list[self.idx]._attr == "Wait":
                self.parse_wait()
            elif self._token_list[self.idx]._attr == "Hear":
                self.parse_hear()
            elif self._token_list[self.idx]._attr == "Default":
                self.parse_default()
            elif self._token_list[self.idx]._attr == "Timeout":
                self.parse_timeout()
            elif self._token_list[self.idx]._type == TokenType.Identifier:
                self.parse_variable()
            else:
                raise ParseError("Expected a keyword")
        self.status_check()
        return self.tree
