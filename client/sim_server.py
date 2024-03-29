import random
import string

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


class MessageRequest(BaseModel):
    token: str
    message: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)


@app.get("/register")
def give_token() -> dict:
    # 随机的返回一些东西
    return {"token": "token", "status": "main", "wait": random.randint(1, 10), "message": ''.join(random.sample(string.ascii_letters + string.digits, 8))}


@app.get("/dsl")
def give_response(status: str, message: str):
    # 随机的返回一些东西
    return {"status": "main", "message": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
            "wait": random.randint(1, 10)}


if __name__ == '__main__':
    uvicorn.run(app='sim_server:app', host="127.0.0.1",
                port=8000, reload=True, debug=True)
