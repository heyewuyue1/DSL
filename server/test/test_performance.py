import unittest
import requests
import random
from threading import Thread

class PerformanceTest(unittest.TestCase):
    url = "http://127.0.0.1:8000/"
    message = ['abbc', 'bccd', 'default']
    def sim_client(self):
        token = requests.get(self.url + "register")
        self.assertEqual(token.status_code, 200)
        # 随机发送消息
        sel = random.randint(0, 2)
        res = requests.get(self.url + "dsl", {"token": eval(token.text)["token"], "status": "main", "message": self.message[sel]})
        self.assertEqual(res.status_code, 200)
        # 根据发送的不同消息，判断相应的回复
        if sel == 0:
            self.assertEqual(eval(res.text)["status"], "aProc")
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "This is status a.")
        elif sel == 1:
            self.assertEqual(eval(res.text)["status"], "bProc")
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "This is status b.")
        else:
            self.assertEqual(eval(res.text)["status"], "defaultProc")
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "I don't understand.")

    
    def test_pressure(self):
        thread_pool = []
        for i in range(500):
            thread_pool.append(Thread(target=self.sim_client))
            thread_pool[i].start()
        for i in range(500):
            thread_pool[i].join()

if __name__ == "__main__":
    unittest.main()
