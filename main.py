from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from markdown import markdown

from api import OpenaiChat
from domain.user import user_router

import logging

logging.basicConfig(
    level=logging.INFO,  # 로그 레벨 설정
    filename="logs.log",  # 로그 파일 이름
    filemode="a",  # 로그 파일 모드 (a: append)
    format="%(asctime)s - %(levelname)s - %(message)s",
    # 로그 출력 형식 설정
)


app = FastAPI()
app.include_router(user_router.router)
templates = Jinja2Templates(directory="templates")
api = OpenaiChat()

@app.get("/", response_class=HTMLResponse)
async def chatroom(request: Request):
    return templates.TemplateResponse("chatroom.html", {"request": request, 'messages': api.history})

@app.post("/")
async def send_message(request: Request):
    form_data = await request.form()
    message = form_data.get('message')
    api.send_message(message)
    return templates.TemplateResponse("chatroom.html", {"request": request, 'messages': api.history})

@app.get("/reset")
async def reset_message(request: Request):
    api.clear_message()
    return RedirectResponse(url="/")

@app.get('/samhang')
async def samhang(request: Request):
    return templates.TemplateResponse("samhang.html", {"request": request})



@app.get('/listen', response_class=HTMLResponse)
async def listen(request: Request):
    return templates.TemplateResponse("listen.html", {'request': request})