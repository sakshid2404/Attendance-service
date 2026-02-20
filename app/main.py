from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import Base, engine, get_db
from app.models import Attendance
from app.schemas import AttendanceCreate, AttendanceResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


# 1️⃣ Mark Attendance
@app.post("/attendance/create", response_model=AttendanceResponse)
def create_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    new_att = Attendance(**data.dict())
    db.add(new_att)
    db.commit()
    db.refresh(new_att)
    return new_att


# 0️⃣ Get ALL attendance
@app.get("/attendance")
def get_all_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()


# 2️⃣ Get attendance of a user
@app.get("/attendance/user/{user_id}")
def get_user_attendance(user_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.user_id == user_id).all()


# 3️⃣ Get attendance of a date
@app.get("/attendance/date/{attendance_date}")
def get_by_date(attendance_date: date, db: Session = Depends(get_db)):
    """
    Example URL:
    http://127.0.0.1:8000/attendance/date/2025-01-15
    Format must be YYYY-MM-DD
    """
    return db.query(Attendance).filter(Attendance.date == attendance_date).all()



# 4️⃣ Update attendance
@app.put("/attendance/update/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, data: AttendanceCreate, db: Session = Depends(get_db)):
    att = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not att:
        raise HTTPException(status_code=404, detail="Attendance not found")

    for key, value in data.dict().items():
        setattr(att, key, value)

    db.commit()
    db.refresh(att)
    return att


# 5️⃣ Delete attendance entry
@app.delete("/attendance/delete/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    att = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not att:
        raise HTTPException(status_code=404, detail="Attendance not found")

    db.delete(att)
    db.commit()
    return {"message": "Attendance deleted successfully"}
