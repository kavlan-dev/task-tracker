from abc import ABC, abstractmethod
from datetime import datetime
import os
from typing import List, Optional
import json
from task_tracker.models.task import TASK_STATUS, Task


class TaskRepository(ABC):
    @abstractmethod
    def add(self, new_task: Task) -> Task:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, task_id: int, task_update: Task) -> Optional[Task]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass


class JsonFileTaskRepository(TaskRepository):
    def __init__(self, path: str) -> None:
        self.path = path

        if not os.path.exists(self.path):
            self._tasks = []
            return

        with open(self.path, "r", encoding="utf-8") as f:
            self._tasks = [Task(**task_data) for task_data in json.load(f)]

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([vars(task) for task in self._tasks], f, indent=2)

    def _generate_id(self) -> int:
        if not self._tasks:
            return 1

        return max(task.id for task in self._tasks if task.id) + 1

    def add(self, new_task: Task) -> Task:
        tid = self._generate_id()
        now = datetime.now().isoformat()

        new_task.status = TASK_STATUS["todo"]
        new_task.id = tid
        new_task.created_at = now
        new_task.updated_at = now

        self._tasks.append(new_task)
        self._save()
        return new_task

    def get_all(self) -> List[Task]:
        return [task_data for task_data in self._tasks]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def update(self, task_id: int, task_update: Task) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            return
        for key, value in vars(task_update).items():
            if value:
                setattr(task, key, value)
        task.updated_at = datetime.now().isoformat()
        self._save()
        return task

    def delete(self, task_id: int) -> bool:
        for i, t in enumerate(self._tasks):
            if t.id == task_id:
                self._tasks.pop(i)
                self._save()
                return True
        return False
