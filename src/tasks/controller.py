from datetime import datetime
from src.tasks.dtos import TaskCreateDTO
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException, status


def create_task(body: TaskCreateDTO, db: Session):
    data = body.model_dump()
    print(data)

    task = TaskModel(title=data["title"], 
                     description=data["description"], 
                     status=data["status"],
                     created_at = datetime.now(),
                     updated_at = datetime.now()
                     )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"message": "Task created successfully...", "task": task}


def get_all_tasks(db: Session):
    tasks = db.query(TaskModel).all()
    task_count = len(tasks)
    return {"message": "All tasks fetched successfully...", "Total Count": task_count, "tasks": tasks}

def get_task_by_id(task_id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        return {"message": "Task fetched successfully...", "task": task}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task id not found.")


def update_task(task_id: int, body: TaskCreateDTO, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        data = body.model_dump()
        task.title = data["title"]
        task.description = data["description"]
        task.status = data["status"]
        task.updated_at = datetime.now()
        db.commit()
        db.refresh(task)
        return {"message": "Task updated successfully...", "task": task}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task id not found.")    


def delete_task(task_id: int, db: Session):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully..."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task id not found.")

    