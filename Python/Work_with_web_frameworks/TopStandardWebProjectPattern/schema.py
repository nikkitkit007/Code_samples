from pydantic import BaseModel
from datetime import datetime


class Schema1(BaseModel):
    field1: int
    field2: str
    field3: datetime
