'''
Description: 后端应答模块，采用FastAPI实现
Author: He Jiahao
Date: 2022-09-09 17:05:54
LastEditTime: 2022-11-17 21:32:20
'''

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import sys

from bot.interpreter import Robot
from bot.lexer import Lexer
from bot.parser import Parser

file_path = "test/lex/Hello.bot"  # 要读取的脚本文件路径
key = "jasonhe"  # 加密用的密钥
time_out = 3600
if len(sys.argv) >= 2:
    file_path = sys.argv[1]
    if len(sys.argv) >= 3:
        key = sys.argv[2]
        if len(sys.argv) >= 4:
            time_out = eval(sys.argv[3])

# 生成语法树和机器人对象
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
description: 处理客户端注册会话请求
return {dict} 一个token，客户端下一个状态，等待的时间和要输出的信息
'''


@app.get("/register")
def give_token() -> dict:
    token = robot.add_user(key, time_out)
    data = robot.handle_transfered(token, True, "main", "")
    return {"token": token, "status": data["status"], "wait": data["wait"], "message": data["message"]}


'''
description: 接受客户端消息并返回应答
param {str} token 客户端token
param {str} status 客户端当前状态
param {str} message 用户输入
return {dict} 客户端下一个状态，等待的时间和要输出的信息
'''


@app.get("/dsl")
def give_response(token: str, status: str, message: str) -> dict:
    print(str(robot.user_var))
    return robot.handle_message(token, status, message, key)


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1",
                port=8000, reload=False, debug=True)
