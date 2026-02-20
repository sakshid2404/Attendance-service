from pydantic import BaseModel
from datetime import date, time

class AttendanceCreate(BaseModel):
    user_id: int
    date: date
    status: str
    time_in: time | None = None
    time_out: time | None = None


class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    date: date
    status: str
    time_in: time | None
    time_out: time | None

    class Config:
        orm_mode = True
