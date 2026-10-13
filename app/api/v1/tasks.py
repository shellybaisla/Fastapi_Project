from  fastapi import APIRouter,Depends,status
from fastapi.security import APIKeyHeader
from app.services import task_service
from app.schemas.task import TaskSchema,TaskResponseSchema
from app.core.database import get_db
from typing import List
from sqlalchemy.orm import Session
from app.core.security import is_authenticated
from app.models.user import UserModel

task_routes = APIRouter(prefix="/tasks")
# task_routes = APIRouter(prefix="/tasks", tags=["Tasks"])
# task_routes = APIRouter(prefix="/task", dependencies=[Depends(is_authenticated)])


@task_routes.post("",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return task_service.create_tasks(body,db,user)

@task_routes.get("",response_model=List[TaskResponseSchema],status_code=status.HTTP_200_OK)
def get_all_tasks(db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return task_service.get_tasks(db,user)

@task_routes.get("/{task_id}",response_model=TaskResponseSchema,status_code=status.HTTP_200_OK)
def get_one_task(task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return task_service.get_one_task(task_id,db,user)

@task_routes.put("/{task_id}",response_model=TaskResponseSchema,status_code=status.HTTP_200_OK)
def update_task(body:TaskSchema,task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return task_service.update_task(body,task_id,db,user)

@task_routes.delete("/{task_id}",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return task_service.delete_task(task_id,db,user)

