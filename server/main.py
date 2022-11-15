"""
Description: 后端应答模块，采用FastAPI实现
Author: He Jiahao
Date: 2022-09-09 17:05:54
LastEditTime: 2022-11-13 15:33:55
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jose import jwt
from time import time

from bot.interpreter import MessageRequest, Robot
import uvicorn

from bot.lexer import Lexer
from bot.parser import Parser

import sys

file_path = "test/lex/Hello.bot"
expire_time = 3600
key = "jasonhe"
if len(sys.argv) >= 2:
    filePath = sys.argv[1]
token_list = Lexer(file_path).lex()
tree = Parser(token_list).parse()
robot = Robot(tree)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)

'''
description: 接收到前端发来的消息之后给出应答
param {MessageRequest} msg_request 接收到的用户消息
return {dict} 等待时间和要回复的消息
'''

@app.post("/dsl")
def give_response(msg_request: MessageRequest):
    return robot.handle_message(msg_request)

'''
description: 接收到前端发来的请求token之后删除user_list中已经超时的会话，再给请求者发一个token
return {dict} token，main状态的等待时间和要回复的消息
'''

@app.get("/token")
def give_token():
    return robot.add_user()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
