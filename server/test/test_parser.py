import unittest
from bot.lexer import Token, TokenType
from bot.parser import Parser, ParseError


class ParserTest(unittest.TestCase):
    # 正常输入
    stub1 = [
        Token(TokenType.Identifier, "%name%"),
        Token(TokenType.Operator, "="),
        Token(TokenType.ConstStr, "He Jiahao"),
        Token(TokenType.Identifier, "%num%"),
        Token(TokenType.Operator, "="),
        Token(TokenType.ConstNum, "0"),
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
        Token(TokenType.Keyword, "Speak"),
        Token(TokenType.ConstStr, "What can I help you, %name%?"),
        Token(TokenType.Keyword, "Wait"),
        Token(TokenType.ConstNum, "5"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "ab*c"),
        Token(TokenType.Status, "aProc"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "bc*d"),
        Token(TokenType.Status, "bProc"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "quit"),
        Token(TokenType.Status, "quitProc"),
        Token(TokenType.Keyword, "Default"),
        Token(TokenType.Status, "defaultProc"),
        Token(TokenType.Keyword, "Timeout"),
        Token(TokenType.Status, "quitProc")
    ]
    
    # 正常输出
    result1 = {
    'main': {
        'Speak': 'What can I help you, %name%?',
        'Wait': 5,
        'Hear':{
            'ab*c': 'aProc',
            'bc*d': 'bProc',
            'quit': 'quitProc'
            }, 
        'Default': 'defaultProc',
        'Timeout': 'quitProc',
        'Operate': {
            '%name%':'He Jiahao',
            '%num%': '0'
            }
        }
    }

    # Status后面没有跟状态名
    stub2 = [
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Keyword, "Speak"),
        Token(TokenType.ConstStr, "What can I help you, %name%?"),
        Token(TokenType.Keyword, "Wait"),
        Token(TokenType.ConstNum, "5"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "ab*c"),
        Token(TokenType.Status, "aProc"),
        Token(TokenType.Keyword, "Default"),
        Token(TokenType.Status, "defaultProc"),
        Token(TokenType.Keyword, "Timeout"),
        Token(TokenType.Status, "quitProc")
    ]

    # 重复的状态名
    stub3 = [
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
        Token(TokenType.Keyword, "Speak"),
        Token(TokenType.ConstStr, "What can I help you, %name%?"),
        Token(TokenType.Keyword, "Wait"),
        Token(TokenType.ConstNum, "5"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "ab*c"),
        Token(TokenType.Status, "aProc"),
        Token(TokenType.Keyword, "Default"),
        Token(TokenType.Status, "defaultProc"),
        Token(TokenType.Keyword, "Timeout"),
        Token(TokenType.Status, "quitProc"),
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
    ]

    # 在期望得到字符串的时候没有得到字符串
    stub4 = [
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
        Token(TokenType.Keyword, "Speak"),
        Token(TokenType.Keyword, "Wait"),
        Token(TokenType.ConstNum, "5"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "ab*c"),
        Token(TokenType.Status, "aProc"),
        Token(TokenType.Keyword, "Default"),
        Token(TokenType.Status, "defaultProc"),
        Token(TokenType.Keyword, "Timeout"),
        Token(TokenType.Status, "quitProc"),
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
    ]

    # 有Wait语句而没有Timeout语句
    stub5 = [
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
        Token(TokenType.Keyword, "Speak"),
        Token(TokenType.ConstStr, "What can I help you, %name%?"),
        Token(TokenType.Keyword, "Wait"),
        Token(TokenType.ConstNum, "5"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "ab*c"),
        Token(TokenType.Status, "aProc"),
        Token(TokenType.Keyword, "Default"),
        Token(TokenType.Status, "defaultProc"),
    ]

    # 期望得到一个标识符或者关键字的时候得到了一个字符串
    stub6 = [
        Token(TokenType.ConstStr, "What can I help you, %name%?"),
        Token(TokenType.Keyword, "Status"),
        Token(TokenType.Status, "main"),
        Token(TokenType.Keyword, "Speak"),
        Token(TokenType.ConstStr, "What can I help you, %name%?"),
        Token(TokenType.Keyword, "Wait"),
        Token(TokenType.ConstNum, "5"),
        Token(TokenType.Keyword, "Hear"),
        Token(TokenType.ConstStr, "ab*c"),
        Token(TokenType.Status, "aProc"),
        Token(TokenType.Keyword, "Default"),
        Token(TokenType.Status, "defaultProc"),
        Token(TokenType.Keyword, "Timeout"),
        Token(TokenType.Status, "quitProc"),
    ]

    # 没有main状态
    stub7 = [
            Token(TokenType.ConstStr, "What can I help you, %name%?"),
            Token(TokenType.Keyword, "Status"),
            Token(TokenType.Status, "m"),
            Token(TokenType.Keyword, "Speak"),
            Token(TokenType.ConstStr, "What can I help you, %name%?"),
            Token(TokenType.Keyword, "Wait"),
            Token(TokenType.ConstNum, "5"),
            Token(TokenType.Keyword, "Hear"),
            Token(TokenType.ConstStr, "ab*c"),
            Token(TokenType.Status, "aProc"),
            Token(TokenType.Keyword, "Default"),
            Token(TokenType.Status, "defaultProc"),
            Token(TokenType.Keyword, "Timeout"),
            Token(TokenType.Status, "quitProc"),
        ]

    def test_normal(self):
        parser = Parser(self.stub1)
        self.assertEqual(parser.parse(), self.result1)
    
    def test_no_sname(self):
        parser = Parser(self.stub2)
        with self.assertRaises(ParseError):
            parser.parse()
    
    def test_duplicate_status(self):
        parser = Parser(self.stub3)
        with self.assertRaises(ParseError):
            parser.parse()

    def test_no_string(self):
        parser = Parser(self.stub4)
        with self.assertRaises(ParseError):
            parser.parse()

    def test_no_timeout(self):
        parser = Parser(self.stub5)
        with self.assertRaises(ParseError):
            parser.parse()

    def test_no_keyword(self):
        parser = Parser(self.stub6)
        with self.assertRaises(ParseError):
            parser.parse()

    def test_no_main(self):
        parser = Parser(self.stub7)
        with self.assertRaises(ParseError):
            parser.parse()

if __name__ == "__main__":
    unittest.main()

        