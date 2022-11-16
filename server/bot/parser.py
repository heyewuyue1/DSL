'''
Description: 语法分析模块，将输入的记号流转化为语法树
Author: He Jiahao
Date: 2022-10-01 11:43:32
LastEditTime: 2022-11-16 13:57:16
'''

from bot.lexer import Token, TokenType
import warnings

class ParseError(Exception):
    '''
    description: 用于报出语法分析阶段的错误
    param {*} self
    param {str} error_msg 错误信息
    return {*}
    '''

    def __init__(self, error_msg: str) -> None:
        self.msg = error_msg


class Parser(object):
    '''
    description: Parser类的构造函数，从中可以看出一个语法树的基本结构。
    param {*} self
    param {list} token_list 输入的记号表
    return {*}
    '''

    def __init__(self, token_list: list[Token]) -> None:
        self.current_status = ""
        self.idx = 0
        self.token_list = token_list
        self.has_main = False
        self.tree = {
            "main": {
                "Speak": "",
                "Wait": -1,
                "Hear": {},
                "Default": "",
                "Timeout": "",
                "Operate": {}
            }
        }

    '''
    description: 当读取到关键字"Status"时采取的行为
    param {*} self
    return {*}
    '''

    def parse_status(self) -> None:
        if self.current_status != "":
            self.status_check()
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.Status or self.idx >= len(self.token_list):
            raise ParseError("Expected a Status name.")
        if self.token_list[self.idx]._attr != "main" or self.token_list[self.idx]._attr == "main" and self.has_main:
            if self.tree.get(self.token_list[self.idx]._attr) != None:
                raise ParseError("Duplicate Status name: " +
                                 self.token_list[self.idx]._attr)
            self.tree[self.token_list[self.idx]._attr] = {
                "Speak": "",
                "Wait": -1,
                "Hear": {},
                "Default": "",
                "Timeout": "",
                "Operate": {}
            }
        self.current_status = self.token_list[self.idx]._attr
        self.idx += 1

    '''
    description: 当读取到关键字"Speak"时采取的行为
    param {*} self
    return {*}
    '''

    def parse_speak(self) -> None:
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.ConstStr or self.idx >= len(self.token_list):
            raise ParseError("Expected a string constant")
        self.tree[self.current_status]["Speak"] = self.token_list[self.idx]._attr
        self.idx += 1

    '''
    description: 当读取到关键字"Hear"时采取的行为
    param {*} self
    return {*}
    '''

    def parse_hear(self) -> None:
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.ConstStr or self.idx >= len(self.token_list):
            raise ParseError("Expected a string constant")
        condition = self.token_list[self.idx]._attr
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.Status or self.idx >= len(self.token_list):
            raise ParseError("Expected a status to transfer")
        next_status = self.token_list[self.idx]._attr
        self.tree[self.current_status]["Hear"][condition] = next_status
        self.idx += 1

    '''
    description: 当读取到关键字"Wait"时采取的行为
    param {*} self
    return {*}
    '''

    def parse_wait(self) -> None:
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.ConstNum or self.idx >= len(self.token_list):
            raise ParseError("Expected a wait time.")
        if eval(self.token_list[self.idx]._attr) < 0:
            raise ParseError(
                "Wait time can only be an integer greater than 0.")
        self.tree[self.current_status]["Wait"] = eval(
            self.token_list[self.idx]._attr)
        self.idx += 1

    '''
    description: 当读取到关键字"Default"时采取的行为
    param {*} self
    return {*}
    '''

    def parse_default(self) -> None:
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.Status or self.idx >= len(self.token_list):
            raise ParseError("Expected a Status name")
        self.tree[self.current_status]["Default"] = self.token_list[self.idx]._attr
        self.idx += 1

    '''
    description: 当读取到关键字"Timeout"时采取的行为
    param {*} self
    return {*}
    '''

    def parse_timeout(self) -> None:
        self.idx += 1
        if self.token_list[self.idx]._type != TokenType.Status or self.idx >= len(self.token_list):
            raise ParseError("Expected a Status name")
        self.tree[self.current_status]["Timeout"] = self.token_list[self.idx]._attr
        self.idx += 1

    '''
    description: 当读取到一个标识符时采取的行为
    param {*} self
    return {*}
    '''

    def parse_variable(self) -> None:
        id_name = self.token_list[self.idx]._attr
        self.idx += 1
        next_token = self.token_list[self.idx]
        # 在外部定义的全局变量
        if next_token._type == TokenType.Operator and next_token._attr == '=':
            self.idx += 1
            next_token = self.token_list[self.idx]
            if next_token._type == TokenType.ConstNum or next_token._type == TokenType.ConstStr:
                value = next_token._attr
                op_state = self.current_status
                if op_state == "":
                    op_state = "main"
                self.tree[op_state]["Operate"][id_name] = value
                self.idx += 1
            else:
                raise ParseError("Expected a number or a string constant")

    '''
    description: 在每一次解析完一个状态之后运行的状态检查
    param {*} self
    return {*}
    '''

    def status_check(self) -> None:
        if self.current_status == "main":
            self.has_main = True
        wait = self.tree[self.current_status].get("Wait")
        if wait == -1 and self.tree[self.current_status].get("Timeout"):
            warnings.warn('Status "' + self.current_status +
                          '" has to wait forever before goto the timeout status.', UserWarning)
        if wait and wait > 0 and not self.tree[self.current_status].get("Timeout"):
            raise ParseError('Status "' + self.current_status +
                             '" has a valid wait time but no Timeout status set.')
        if not self.tree[self.current_status].get("Speak"):
            warnings.warn('Status "' + self.current_status +
                          '" has nothing to speak.', UserWarning)

    '''
    description: 根据当前读到的符号选择不同语句的处理函数
    param {*} self
    return {*}
    '''

    def parse(self) -> dict:
        while self.idx < len(self.token_list):
            if self.token_list[self.idx]._attr == "Status":
                self.parse_status()
            elif self.token_list[self.idx]._attr == "Speak":
                self.parse_speak()
            elif self.token_list[self.idx]._attr == "Wait":
                self.parse_wait()
            elif self.token_list[self.idx]._attr == "Hear":
                self.parse_hear()
            elif self.token_list[self.idx]._attr == "Default":
                self.parse_default()
            elif self.token_list[self.idx]._attr == "Timeout":
                self.parse_timeout()
            elif self.token_list[self.idx]._type == TokenType.Identifier:
                self.parse_variable()
            else:
                raise ParseError("Expected a keyword or an Identifier")
        self.status_check()
        if not self.has_main:
            raise ParseError("No main status to begin with")
        return self.tree
