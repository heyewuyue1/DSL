import unittest
from bot.lexer import Lexer, LexError


class LexerTest(unittest.TestCase):
    def test_lex_hello(self):
        test_hello = Lexer("test/lex/Hello.bot")
        test_hello.lex()
        with open("test/lex/result_hello.txt") as f:
            for token in test_hello.token_list:
                self.assertEqual(str(token), f.readline().strip())

    def test_unclosed_string(self):
        test_hello = Lexer("test/lex/test1.bot")
        with self.assertRaises(LexError):
            test_hello.lex()

    def test_unclosed_var(self):
        test_hello = Lexer("test/lex/test2.bot")
        with self.assertRaises(LexError):
            test_hello.lex()

    def test_unexpected_word(self):
        test_hello = Lexer("test/lex/test3.bot")
        with self.assertRaises(LexError):
            test_hello.lex()


if __name__ == "__main__":
    unittest.main()
