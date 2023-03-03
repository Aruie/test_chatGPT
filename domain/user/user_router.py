from fastapi import APIRouter, HTTPException
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette import status
from fastapi.templating import Jinja2Templates

from database import get_db
from domain.user import user_crud, user_schema

router = APIRouter(
    prefix="/api/user",
)

templates = Jinja2Templates(directory="templates")

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db, user_create=_user_create)


@router.get("/register", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(username: str, password: str, password_confirm: str):
    if password != password_confirm:
        return {"result": "비밀번호가 일치하지 않습니다."}
    # 이름, 비밀번호를 데이터베이스에 저장하는 코드를 여
