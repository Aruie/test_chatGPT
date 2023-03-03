from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


logger = logging.getLogger(__name__)

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1))
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) 
    ).first()