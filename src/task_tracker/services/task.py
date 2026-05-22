from typing import List, Optional
from task_tracker.models.task import Task, TaskCreate, TaskUpdate
from task_tracker.repositories.task import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def create_task(self, new_task: TaskCreate) -> Task:
        task = Task(
            id=None, status=None, created_at=None, updated_at=None, **vars(new_task)
        )
        self.repo.add(task)
        return task

    def list_task(self, status_filter: Optional[str] = None) -> List[Task]:
        tasks = self.repo.get_all()
        if not status_filter:
            return tasks
        return [task for task in tasks if task.status == status_filter]

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        task = Task(id=None, created_at=None, updated_at=None, **vars(task_update))
        return self.repo.update(task_id, task)

    def delete(self, task_id: int) -> bool:
        return self.repo.delete(task_id)
