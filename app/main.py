from fastapi import FastAPI
from app.api.v1 import tasks, users
from app.core.database import Base,engine
from app.models.task import TaskModel
from app.api.v1.tasks import task_routes
from app.api.v1.users import user_routes
from app.models.user import UserModel

Base.metadata.create_all(engine)

app = FastAPI(title="This is my Tesk Management Application")
app.include_router(user_routes) #its all connect with our task route
app.include_router(task_routes)

