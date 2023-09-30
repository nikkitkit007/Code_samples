from fastapi import APIRouter, Depends
from typing import List, Union

from sqlalchemy import select, insert, delete, text

from utils import module_url
from context import session
import schema
from db.model import User


r = APIRouter()
BASE = module_url(__name__)

max_limit = 100


@r.get(BASE + '/', response_model=List[schema.User])
async def get_emotions():
    """
    Вернуть всех пользователей
    """
    workers = (await session().execute(select(User))).scalars()
    return workers
