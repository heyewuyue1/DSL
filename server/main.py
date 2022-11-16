'''
Description: 后端应答模块，采用FastAPI实现
Author: He Jiahao
Date: 2022-09-09 17:05:54
LastEditTime: 2022-11-16 13:36:11
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bot.interpreter import Robot
import uvicorn

from bot.lexer import Lexer
from bot.parser import Parser

import sys

file_path = "test/lex/Hello.bot"
if len(sys.argv) >= 2:
    file_path = sys.argv[1]
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
description: 接受客户端消息并返回应答
param {str} status 客户端当前状态
param {str} message 用户输入
return {dict} 客户端下一个状态，要输出的信息，等待的时间和变量赋值表
'''
@app.get("/dsl")
def give_response(status: str, message: str) -> dict:
    return robot.handle_message(status, message)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1",
                port=8000, reload=True, debug=True)
