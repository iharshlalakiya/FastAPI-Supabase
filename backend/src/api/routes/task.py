from fastapi import APIRouter, Depends, HTTPException
from src.schemas.task import TaskCreate, TaskUpdate
from src.services import task_service
from src.core.security import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/create_task")
def create_task_endpoint(
    task: TaskCreate,
    user_data = Depends(get_current_user)
):
    client, user_id = user_data
    return task_service.create_task(client, user_id, task)

@router.get("/all_tasks")
def all_tasks_endpoint(
    user_data = Depends(get_current_user)
):
    client, user_id = user_data
    return task_service.get_tasks(client, user_id)

@router.put("/update_task/{task_id}")
def update_task_endpoint(
    task_id: str,
    task: TaskUpdate,
    user_data = Depends(get_current_user)
):
    client, user_id = user_data
    return task_service.update_task(client, user_id, task_id, task)

@router.delete("/delete_task/{task_id}")
def delete_task_endpoint(
    task_id: str,
    user_data = Depends(get_current_user)
):
    client, user_id = user_data
    return task_service.delete_task(client, user_id, task_id)