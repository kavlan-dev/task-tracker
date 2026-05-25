import os

from task_tracker.config import Config
from task_tracker.repositories.task import ITaskRepository, JsonFileTaskRepository
from task_tracker.routers.task import TaskRouter
from task_tracker.services.task import TaskService


def get_config() -> Config:
    return Config(os.getenv("TASKS_PATH", "tasks.json"))


def get_json_file_task_repository(path: str) -> ITaskRepository:
    return JsonFileTaskRepository(path)


def get_task_service(repo: ITaskRepository) -> TaskService:
    return TaskService(repo)


def get_task_router(service: TaskService) -> TaskRouter:
    return TaskRouter(service)
