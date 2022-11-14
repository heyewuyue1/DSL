'''
Description: 词法分析模块，将从文件读入字符流转换成为一个记号流
Author: He Jiahao
Date: 2022-09-30 15:31:54
LastEditTime: 2022-11-13 22:49:54
'''

from enum import IntEnum

keyword_str = [
    "Status",
    "Speak",
    "Wait",
    "Hear",
    "Default",
    "Timeout",
    "Identifier",
    "Operator"
]


class LexError(Exception):
    '''
    description: 用于报出词法分析阶段的错误
    param {*} self
    param {str} error_msg 错误信息
    return {*}
    '''

    def __init__(self, error_msg: str) -> None:
        self.msg = error_msg


class TokenType(IntEnum):
    Keyword = 0
    Status = 1
    ConstNum = 2
    ConstStr = 3
    Error = 4
    Identifier = 5
    Operator = 6


class Token(object):
    '''
    description: 一个表示记号的二元组
    param {*} self
    param {TokenType} type 记号的属性
    param {str} attr 记号的属性值
    return {*}
    '''

    def __init__(self, type: TokenType = TokenType.Error, attr: str = "") -> None:
        self._type = type
        self._attr = attr

    '''
    description: 为了方便调试，设计了记号类的字符串输出格式
    param {*} self
    return {*}
    '''

    def __str__(self) -> str:
        return '<' + str(self._type) + ', ' + self._attr + '>'


class Lexer(object):
    '''
    description: 词法分析器
    param {*} self
    param {str} filePath 输入文件路径
    return {*}
    '''

    def __init__(self, filePath: str) -> None:
        self.token_list = []
        self.input = open(filePath, mode='r', encoding="utf-8")

    '''
    description: 进行词法分析
    param {*} self
    return {list[Token]} 返回输出的记号流
    '''

    def lex(self) -> list[Token]:
        # 先将输入流按照空格分开为一个个单词
        buf = self.input.read().split()
        i = 0
        while i < len(buf):
            # 如果一个单词全部由字母组成，说明他是关键字或者状态名
            if buf[i].isalpha():
                if buf[i] in keyword_str:
                    self.token_list.append(Token(TokenType.Keyword, buf[i]))
                else:
                    self.token_list.append(Token(TokenType.Status, buf[i]))
                i += 1
            elif buf[i].isdigit():
                self.token_list.append(Token(TokenType.ConstNum, buf[i]))
                i += 1
            # 检测到双引号，说明是一个字符串常量
            elif buf[i][0] == '"':
                const_str = buf[i]
                i += 1
                # 处理字符串中的空格
                while const_str[-1] != '"' and i < len(buf):
                    const_str += ' ' + buf[i]
                    i += 1
                # 未闭合的字符串
                if const_str[-1] != '"':
                    raise LexError("Unclosed string constant")
                else:
                    self.token_list.append(
                        Token(TokenType.ConstStr, eval(const_str)))
            # 检测到%，说明是一个标识符
            elif buf[i][0] == '%':
                id_name = buf[i]
                # 未闭合的标识符
                if buf[i][-1] != '%':
                    raise LexError("Unclosed identifier")
                else:
                    self.token_list.append(
                        Token(TokenType.Identifier, id_name))
                i += 1
            # 检测到赋值运算符
            elif buf[i] == '=':
                i += 1
                self.token_list.append(Token(TokenType.Operator, '='))
            else:
                raise LexError("Unexpected word " + buf[i]) 

        return self.token_list

    '''
    description: 打印输出产生的记号流
    param {*} self
    return {*}
    '''

    def show_list(self) -> None:
        for token in self.token_list:
            print(token)
    
    def __del__(self) -> None:
        self.input.close()

