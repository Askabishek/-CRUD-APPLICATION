from typing import Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    task = Task(**task_data.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Optional[Task]:
    return (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == owner_id)
        .first()
    )


def get_tasks(
    db: Session,
    owner_id: int,
    completed: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(Task).filter(Task.owner_id == owner_id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    total = query.count()
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size

    return tasks, total, total_pages


def update_task(db: Session, task: Task, updates: TaskUpdate) -> Task:
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
