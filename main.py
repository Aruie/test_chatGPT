from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from api import OpenaiChat


app = FastAPI()
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