from bot.lexer import Token, TokenType

class ParseError(Exception):
    def __init__(self, _msg: str) -> None:
        self.msg = _msg

class Parser(object):
    def __init__(self, token_list: list[Token]) -> None:
        self.current_status = ""
        self.idx = 0
        self._token_list = token_list
        self.tree = {}
    
    def parse_status(self) -> None:
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.Status or self.idx >= len(self._token_list):
            raise ParseError("Expected a Status name.")
        self.tree[self._token_list[self.idx]._attr] = {
            "Speak": "",
            "Wait": None,
            "Hear": {},
            "Default": "",
            "Timeout": ""
        }
        self.current_status = self._token_list[self.idx]._attr
        self.idx += 1


    def parse_speak(self):
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.ConstStr or self.idx >= len(self._token_list):
            raise ParseError("Expected a string constant")
        self.tree[self.current_status]["Speak"] = eval(self._token_list[self.idx]._attr)
        self.idx += 1

    def parse_hear(self):
        self.idx += 1
        # 将来新增TokenType.condition
        if self._token_list[self.idx]._type != TokenType.ConstStr or self.idx >= len(self._token_list):
            raise ParseError("Expected a string constant")
        condition = eval(self._token_list[self.idx]._attr)
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.Status or self.idx >= len(self._token_list):
            raise ParseError("Expected a status to transfer")
        next_status = self._token_list[self.idx]._attr
        self.tree[self.current_status]["Hear"][condition] = next_status
        self.idx += 1

    def parse_wait(self):
        self.idx += 1
        if self._token_list[self.idx]._type != TokenType.ConstNum or self.idx >= len(self._token_list):
            raise ParseError("Expected a wait time")
        self.tree[self.current_status]["Wait"] = self._token_list[self.idx]._attr
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
            else:
                raise ParseError("Expected a keyword")
        return self.tree
