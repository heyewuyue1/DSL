import unittest
import requests
import random
from bot.parser import WaitType
from threading import Thread

class PerformanceTest(unittest.TestCase):
    url = "http://127.0.0.1:8000/dsl"
    message = ['abbc', 'bccd', '!!!timeout', 'default']
    def sim_client(self):
        # 随机发送消息
        sel = random.randint(0, 3)
        res = requests.get(self.url, {"status": "main", "message": self.message[sel]})
        self.assertEqual(res.status_code, 200)
        # 根据发送的不同消息，判断相应的回复
        if sel == 0:
            self.assertEqual(eval(res.text)["status"], "aProc")
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "This is status a.")
            self.assertEqual(eval(res.text)["var"], {"%num%": '1'})
        elif sel == 1:
            self.assertEqual(eval(res.text)["status"], "bProc")
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "This is status b.")
            self.assertEqual(eval(res.text)["var"], {"%num%": '2'})
        elif sel == 2:
            self.assertEqual(eval(res.text)["status"], "quitProc")
            self.assertEqual(eval(res.text)["wait"], WaitType.Forever)
            self.assertEqual(eval(res.text)["message"], "Bye, %name%!The num is %num%.")
            self.assertEqual(eval(res.text)["var"], {"%name%": "Jiahao He"})
        else:
            self.assertEqual(eval(res.text)["status"], "defaultProc")
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "I don't understand.")
            self.assertEqual(eval(res.text)["var"], {"%num%": '3'})

    
    def test_pressure(self):
        thread_pool = []
        for i in range(10000):
            thread_pool.append(Thread(target=self.sim_client))
            thread_pool[i].start()
        for i in range(10000):
            thread_pool[i].join()

if __name__ == "__main__":
    unittest.main()
