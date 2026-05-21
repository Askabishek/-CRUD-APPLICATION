from typing import Optional, Tuple, List
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate, owner_id: int) -> Task:
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        owner_id=owner_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(
    db: Session,
    owner_id: int,
    completed: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
) -> Tuple[List[Task], int, int]:
    query = db.query(Task).filter(Task.owner_id == owner_id)
    
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()
    return tasks, total, total_pages


def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def update_task(db: Session, task: Task, updates: TaskUpdate) -> Task:
    if updates.title is not None:
        task.title = updates.title
    if updates.description is not None:
        task.description = updates.description
    if updates.completed is not None:
        task.completed = updates.completed
    
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
