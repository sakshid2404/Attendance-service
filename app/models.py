from sqlalchemy import Column, Integer, String, Date, Time
from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(Date, index=True)
    status = Column(String)                    # present / absent / leave
    time_in = Column(Time, nullable=True)
    time_out = Column(Time, nullable=True)
