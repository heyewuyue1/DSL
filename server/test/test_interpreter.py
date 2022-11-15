import unittest
from bot.interpreter import Robot, RuntimeError, MessageRequest
from bot.parser import WaitType


class InterpreterTest(unittest.TestCase):
    stub = {
        '__GLOBAL__': {
            '%name%': 'He Jiahao',
            '%num%': '0'
        },
        'main': {
            'Speak': 'What can I help you, %name%?',
            'Wait': 5,
            'Hear': {
                'a': 'aProc',
                'b': 'bProc',
            }, 
            'Timeout': 'main',
            'Default': 'main',
            'Operate': {
                '%name%': 'He Jiahao',
                '%num%': '0'
            }
        },
        'aProc': {
            'Operate': {},
            'Speak': 'money: %money%?',
        }
    }

    def test_normal(self):
        robot = Robot(self.stub)
        self.assertEqual(robot.add_user("undefined_var"),
                         {"message": "What can I help you, He Jiahao?", "wait": 5})
        self.assertEqual(robot.handle_message(MessageRequest(token="undefined_var", message="a")),
                         {"message": "money: %money%?", "wait": WaitType.Forever})
    
    def test_undefined_status(self):
        robot = Robot(self.stub)
        self.assertEqual(robot.add_user("undefined_status"), 
            {"message": "What can I help you, He Jiahao?", "wait": 5})
        with self.assertRaises(RuntimeError):
            robot.handle_message(MessageRequest(token="undefined_status", message="b"))
    
    def test_timeout(self):
        robot = Robot(self.stub)
        self.assertEqual(robot.add_user("test_timeout"),
                         {"message": "What can I help you, He Jiahao?", "wait": 5})
        self.assertEqual(robot.handle_message(MessageRequest(token="test_timeout", message="!!!timeout")),
                         {"message": "What can I help you, He Jiahao?", "wait": 5})
    
    def test_default(self):
        robot = Robot(self.stub)
        self.assertEqual(robot.add_user("test_default"),
                         {"message": "What can I help you, He Jiahao?", "wait": 5})
        self.assertEqual(robot.handle_message(MessageRequest(token="test_default", message="default")),
                         {"message": "What can I help you, He Jiahao?", "wait": 5})


if __name__ == "__main__":
    unittest.main()
