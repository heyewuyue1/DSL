from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jose import jwt
from datetime import datetime, timedelta

from bot.interpreter import MessageRequest, Robot
import uvicorn

from bot.lexer import Lexer
from bot.parser import Parser

import sys

filePath = "test/Hello.bot"
if len(sys.argv) >= 2:
    filePath = sys.argv[1]
token_list = Lexer(filePath).lex()
tree = Parser(token_list).parse()
robot = Robot(tree)

app = FastAPI()

KEY = "jasonhe"
origins = ["*"]
req_list = {}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)



@app.post("/dsl")
def give_response(msg_request: MessageRequest):
    return robot.handle_message(msg_request)

@app.get("/token")
def give_token():
    limit = datetime.utcnow() + timedelta(3600)
    token_source = {
        "exp": limit,
        "sub": KEY,
        "uid": str(len(req_list))
    }
    token = jwt.encode(token_source, KEY)
    ret = robot.add_user(token)
    return {"token": token, "wait": ret["wait"], "message": ret["message"]}

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
