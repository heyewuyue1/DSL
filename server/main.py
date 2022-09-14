from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jose import jwt
from datetime import datetime, timedelta

from pydantic import BaseModel
import uvicorn

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

class MessageRequest(BaseModel):
    token: str
    message: str


@app.post("/dsl")
def give_response(msg_request: MessageRequest):
    print(msg_request)
    if 'a' in msg_request.message:
        return "Contains a!"
    else:
        return "nope"

@app.get("/token")
def give_token():
    limit = datetime.utcnow() + timedelta(3600)
    token_source = {
        "exp": limit,
        "sub": KEY,
        "uid": str(len(req_list))
    }
    token = jwt.encode(token_source, KEY)
    req_list[token] = "q0"
    return token

if __name__ == '__main__':
    uvicorn.run(app='DSL', host="127.0.0.1", port=8000, reload=True, debug=True)