import unittest
from bot.interpreter import Robot


class InterpreterTest(unittest.TestCase):
    stub = {
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
            'Speak': 'money: %money%?',
            'Wait': -1,
            'Hear': {
                'a': 'aProc',
                'b': 'bProc',
            },
            'Timeout': 'main',
            'Default': 'main',
            'Operate': {},
        }
    }
    
    def test_normal(self):
        robot = Robot(self.stub)
        token = robot.add_user("jasonhe", 3600)
        self.assertEqual(robot.handle_message(token, "main", "a", "jasonhe"),
                         {"status": "aProc",
                          "wait": -1,
                          "message": "money: %money%?",
                          })

    def test_timeout(self):
        robot = Robot(self.stub)
        token = robot.add_user("jasonhe", 3600)
        self.assertEqual(robot.handle_message(token, "main", "_timeout_","jasonhe"),
                         {"status": "main",
                          "wait": 5,
                          "message": "What can I help you, He Jiahao?",
                          })

    def test_default(self):
        robot = Robot(self.stub)
        token = robot.add_user("jasonhe", 3600)
        self.assertEqual(robot.handle_message(token, "main", "default", "jasonhe"),
                         {"status": "main",
                          "wait": 5,
                          "message": "What can I help you, He Jiahao?"
                          })


if __name__ == "__main__":
    unittest.main()
