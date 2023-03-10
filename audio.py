from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketDisconnect
import os
import logging

from api import speech_to_text


logging.basicConfig(
    level=logging.INFO,  # 로그 레벨 설정
    filename="logs.log",  # 로그 파일 이름
    filemode="a",  # 로그 파일 모드 (a: append)
    format="%(asctime)s - %(levelname)s - %(message)s",
    # 로그 출력 형식 설정
)



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class WebSocketRecorder:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def run(self):
        await self.websocket.accept()
        await self.websocket.send_text("녹음을 시작합니다.")
        await self.websocket.receive()

        try:
            while True:
                message = await self.websocket.receive()
                if message["type"] == "websocket.receive":
                    audio_data = message.get("bytes")
                    if audio_data:
                        self.websocket.app.state.audio_data[self.websocket.client.host] += audio_data
                else:
                    break
        except WebSocketDisconnect:
            pass

        audio_data = self.websocket.app.state.audio_data[self.websocket.client.host]
        del self.websocket.app.state.audio_data[self.websocket.client.host]

        if audio_data:
            audio_file = os.path.join("static", f"{self.websocket.client.host}.wav")
            with open(audio_file, "wb") as f:
                f.write(audio_data)

            try:
                text = speech_to_text(audio_file)
            except Exception as e:
                text = str(e)

            await self.websocket.send_text(text)


class WebSocketState:
    def __init__(self):
        self.audio_data = {}


@app.middleware("http")
async def add_websocket_state(request: Request, call_next):
    response = await call_next(request)
    if "Upgrade" in response.headers:
        state = WebSocketState()
        request.app.state.websocket_states[id(response)] = state
    return response


@app.websocket_route("/ws")
async def ws(websocket: WebSocket):
    recorder = WebSocketRecorder(websocket)
    recorder.websocket.app.state.websocket_states[id(websocket)] = recorder.websocket.app.state.websocket_states.get(id(websocket), WebSocketState())
    await recorder.run()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("recoding.html", {"request": request, "host": request.client.host})


@app.on_event("startup")
async def startup():
    app.state.websocket_states = {}


@app.on_event("shutdown")
async def shutdown():
    for state in app.state.websocket_states.values():
        for audio_data in state.audio_data.values():
            del audio_data
        del state
    del app.state.websocket_states
