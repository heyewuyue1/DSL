import unittest
from bot.interpreter import Robot, RuntimeError
from bot.parser import WaitType


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
            'Wait': WaitType.Forever,
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
        self.assertEqual(robot.handle_message("main", "a"),
                         {"status": "aProc",
                          "wait": WaitType.Forever,
                          "message": "money: %money%?",
                          "var": {}
                          })

    def test_undefined_status(self):
        robot = Robot(self.stub)
        with self.assertRaises(RuntimeError):
            robot.handle_message("main", "b")

    def test_timeout(self):
        robot = Robot(self.stub)
        self.assertEqual(robot.handle_message("main", "!!!timeout"),
                         {"status": "main",
                          "wait": 5,
                          "message": "What can I help you, %name%?",
                          "var": {
                              '%name%': 'He Jiahao',
                              '%num%': '0'
                          }
                          })

    def test_default(self):
        robot = Robot(self.stub)
        self.assertEqual(robot.handle_message("main", "default"),
                         {"status": "main",
                          "wait": 5,
                          "message": "What can I help you, %name%?",
                          "var": {
                              '%name%': 'He Jiahao',
                              '%num%': '0'
                          }
                          })


if __name__ == "__main__":
    unittest.main()
