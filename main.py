from fastapi import FastAPI, HTTPException, Path, Query
from typing import Annotated, Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

engine = create_engine("sqlite:///todo.db")
Base = declarative_base()

class Assignments(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    status = Column(String)
    estimated_time = Column(Integer)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

@app.post("/assignment/create/")
async def create_assignment(
    title1: Annotated[str, Query(title="name of title")],
    status1: Annotated[str, Query(title="status of title (Done,Undone)")],
    estimated_time1: Annotated[int, Query(title="time to complete assignment in hours", ge=1, lt=50)]
):
    db = SessionLocal()
    new_assignment = Assignments(title=title1, status=status1, estimated_time=estimated_time1)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    db.close()
    return {
        "Message": "new assignment created",
        "id": new_assignment.id,
        "title": title1,
        "status": status1,
        "time to complete assignment": estimated_time1
    }

@app.get("/assignment/")
async def show_all_assignments():
    db = SessionLocal()
    assignments = db.query(Assignments).all()
    db.close()
    return [{
        "id of assignment": a.id,
        "name of assignment": a.title,
        "status of assignment": a.status,
        "time to complete assignment": a.estimated_time
    } for a in assignments]

@app.get("/assignment/{assign_id}/")
async def assignment_by_id(assign_id: Annotated[int, Path(title="id of assignment", ge=1)]):
    db = SessionLocal()
    res = db.query(Assignments).filter(Assignments.id == assign_id).first()
    db.close()
    if not res:
        raise HTTPException(status_code=404, detail="no assignment with this id")
    return {
        "id": assign_id,
        "name of assignment": res.title,
        "status of assignment": res.status,
        "time to complete assignment": res.estimated_time
    }

@app.delete("/assignment/delete/{assign_id}")
async def delete_assignment(assign_id: Annotated[int, Path(title="id of assignment", ge=1)]):
    db = SessionLocal()
    res = db.query(Assignments).filter(Assignments.id == assign_id).first()
    if not res:
        db.close()
        raise HTTPException(status_code=404, detail="no assignment with this id")
    db.delete(res)
    db.commit()
    db.close()
    return {
        "Message": "assignment deleted",
        "id": assign_id,
        "name of assignment": res.title,
        "status": res.status,
        "time to complete assignment": res.estimated_time
    }

@app.put("/assignment/update/{assign_id}")
async def update_assignment(
    assign_id: Annotated[int, Path(title="id of assignment", ge=1)],
    new_title: Annotated[str, Query(title="new title of assignment")],
    new_status: Annotated[str, Query(title="new status of assignment (Done,Undone)")],
    new_estimated_time: Annotated[int, Query(title="new estimated time", ge=1)]
):
    db = SessionLocal()
    res = db.query(Assignments).filter(Assignments.id == assign_id).first()
    if not res:
        db.close()
        raise HTTPException(status_code=404, detail="no assignment with this id")
    res.title = new_title
    res.status = new_status
    res.estimated_time = new_estimated_time
    db.commit()
    db.refresh(res)
    db.close()
    return {
        "Message": "assignment updated",
        "id": assign_id,
        "name of assignment": new_title,
        "status": new_status,
        "time to complete assignment": new_estimated_time
    }

@app.patch("/assignment/update/some/{assign_id}")
async def update_some_assignment(
    assign_id: Annotated[int, Path(title="id of assignment", ge=1)],
    new_title: Annotated[Optional[str], Query(title="new title of assignment")] = None,
    new_status: Annotated[Optional[str], Query(title="new status of assignment (Done,Undone)")] = None,
    new_estimated_time: Annotated[Optional[int], Query(title="new estimated time", ge=1)] = None
):
    db = SessionLocal()
    res = db.query(Assignments).filter(Assignments.id == assign_id).first()
    if not res:
        db.close()
        raise HTTPException(status_code=404, detail="no assignment with this id")

    if new_title is not None:
        res.title = new_title
    if new_status is not None:
        res.status = new_status
    if new_estimated_time is not None:
        res.estimated_time = new_estimated_time

    db.commit()
    db.refresh(res)
    db.close()
    return {
        "Message": "assignment updated",
        "id": assign_id,
        "name of assignment": res.title,
        "status": res.status,
        "time to complete assignment": res.estimated_time
    }
