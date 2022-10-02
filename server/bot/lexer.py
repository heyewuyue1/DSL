from enum import IntEnum
from lib2to3.pgen2.tokenize import TokenError

tokenTypeStr = [
    "Keyword",
    "Status", 
    "constNum", 
    "constStr", 
    "Error"
    ]

keywordStr = [
    "Status",
    "Speak",
    "Wait",
    "Hear",
    "Default",
    "Timeout"
]

class TokenType(IntEnum):
    Keyword = 0
    Status = 1
    ConstNum = 2
    ConstStr = 3
    Error = 4

class Token(object):
    def __init__(self, type: TokenType=TokenType.Error, attr: str="") -> None:
        self._type = type
        self._attr = attr

    def __str__(self) -> str:
        return '<'+tokenTypeStr[self._type]+', '+ self._attr + '>'


class Lexer(object):
    def __init__(self, filePath: str="server/test/Hello.bot") -> None:
        self.token_list = []
        self.input = open(filePath, mode='r', encoding="utf-8")

    def lex(self) -> list:
        buf = self.input.read().split()
        i = 0
        while i < len(buf):
            if buf[i].isalpha():
                if buf[i] in keywordStr:
                    self.token_list.append(Token(TokenType.Keyword, buf[i]))
                else:
                    self.token_list.append(Token(TokenType.Status, buf[i]))
                i += 1
            elif buf[i].isdigit():
                self.token_list.append(Token(TokenType.ConstNum, buf[i]))
                i += 1
            elif buf[i][0] == '"':
                const_str = buf[i]
                i += 1
                while const_str[-1] != '"' and i < len(buf):
                    const_str += ' ' + buf[i]
                    i += 1
                if const_str[-1] != '"':
                    self.token_list.append(Token(TokenType.Error, "Unclosed string constant: " + const_str))
                else:
                    self.token_list.append(Token(TokenType.ConstStr, const_str))
        return self.token_list
    
    def show_list(self) -> None:
        for token in self.token_list:
            print(token)

if __name__ == "__main__":
    bot_lexer = Lexer()
    bot_lexer.lex()
    bot_lexer.show_list()
