import unittest
import requests
import random
from bot.parser import WaitType
from threading import Thread

class PerformanceTest(unittest.TestCase):
    url = "http://127.0.0.1:5000"
    message = ['abbc', 'bccd', 'c']
    def sim_client(self):
        res = requests.get(self.url + '/token')
        self.assertEqual(res.status_code, 200)
        token = eval(res.text)["token"]
        sel = random.randint(0, 2)
        
        res = requests.post(self.url + '/dsl', json={"token": token, "message": self.message[sel]})
        self.assertEqual(res.status_code, 200)
        if sel == 0:
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "This is status a.")
        elif sel == 1:
            self.assertEqual(eval(res.text)["wait"], 5)
            self.assertEqual(eval(res.text)["message"], "This is status b.")
        elif sel == 2:
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
