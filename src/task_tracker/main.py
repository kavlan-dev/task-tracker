from abc import ABC, abstractmethod
import json
import os
import sys
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

TASK_STATUS = {"todo": "todo", "in-progress": "in-progress", "done": "done"}


@dataclass
class Task:
    id: int = 0
    description: str = ""
    status: str = TASK_STATUS["todo"]
    createdAt: str = datetime.now().isoformat()
    updatedAt: str = datetime.now().isoformat()


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass


class JsonFileTaskRepository(TaskRepository):
    def __init__(self, path: str = "tasks.json") -> None:
        self.path = path

        if not os.path.exists(self.path):
            self._tasks = []
            return

        with open(self.path, "r", encoding="utf-8") as f:
            self._tasks = [Task(**task_data) for task_data in json.load(f)]

    def _save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([task.__dict__ for task in self._tasks], f, indent=2)

    def _generate_id(self) -> int:
        if not self._tasks:
            return 1

        return max(task.id for task in self._tasks) + 1

    def add(self, task: Task) -> None:
        task.id = self._generate_id()
        self._tasks.append(task)
        self._save()

    def get_all(self) -> List[Task]:
        return [task_data for task_data in self._tasks]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def update(self, task: Task) -> None:
        for i, t in enumerate(self._tasks):
            if t.id == task.id:
                self._tasks[i] = task
                self._save()
                return

    def delete(self, task_id: int) -> bool:
        for i, t in enumerate(self._tasks):
            if t.id == task_id:
                self._tasks.pop(i)
                self._save()
                return True
        return False


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def create_task(self, desc: str) -> Task:
        task = Task(description=desc)
        self.repo.add(task)
        return task

    def list_task(self, status_filter: Optional[str] = None) -> List[Task]:
        tasks = self.repo.get_all()
        if not status_filter:
            return tasks
        return [task for task in tasks if task.status == status_filter]

    def update_task_description(self, task_id: int, new_desc: str) -> Optional[Task]:
        task = self.repo.get_by_id(task_id)
        if not task:
            return
        task.description = new_desc
        task.updatedAt = datetime.now().isoformat()
        self.repo.update(task)
        return task

    def update_task_status(self, task_id: int, new_status: str) -> Optional[Task]:
        task = self.repo.get_by_id(task_id)
        if not task:
            return
        task.status = new_status
        task.updatedAt = datetime.now().isoformat()
        self.repo.update(task)
        return task

    def delete(self, task_id: int) -> bool:
        return self.repo.delete(task_id)


class Handler:
    def __init__(self, service: TaskService) -> None:
        self.service = service
        self.command = {
            "add": self.cmd_add,
            "list": self.cmd_list,
            "update": self.cmd_update,
            "mark-in-progress": self.cmd_in_progress,
            "mark-done": self.cmd_done,
            "delete": self.cmd_del,
        }

    def cmd_add(self, args: List[str]) -> None:
        desc = " ".join(args)
        if not desc:
            print("Ошибка: нужно указать описание задачи")
        task = self.service.create_task(desc)
        print(f"Задача успешно добавлена (ID: {task.id})")

    def cmd_list(self, args: List[str]) -> None:
        status_filter = None
        if args and args[0] in TASK_STATUS:
            status_filter = args[0]
        tasks = self.service.list_task(status_filter)
        if not tasks:
            print("Задачи не найдены")
            return

        print("Задачи:")
        print("-" * 50)
        for t in tasks:
            print(f"ID: {t.id}")
            print(f"Описание: {t.description}")
            print(f"Статус: {t.status}")
            print(f"Создано: {t.createdAt}")
            print(f"Обновлено: {t.updatedAt}")
            print("-" * 50)

    def cmd_update(self, args: List[str]) -> None:
        if len(args) < 2:
            print("Ошибка: укажите id и новое описание задачи")
            return
        tid = int(args[0])
        new_desc = " ".join(args[1:])
        task = self.service.update_task_description(tid, new_desc)
        if task:
            print("Задача обновлена успешно")
            return
        print("Не удалось обновить задачу")

    def cmd_in_progress(self, args: List[str]) -> None:
        if len(args) < 1:
            print("Ошибка: укажите id")
            return
        tid = int(args[0])
        task = self.service.update_task_status(tid, TASK_STATUS["in-progress"])
        if task:
            print("Задача успешно отмечена как в процессе")
            return
        print("Задача не отмечена как в процессе")

    def cmd_done(self, args: List[str]) -> None:
        if len(args) < 1:
            print("Ошибка: укажите id")
            return
        tid = int(args[0])
        task = self.service.update_task_status(tid, TASK_STATUS["done"])
        if task:
            print("Задача успешно отмечена как выполненная")
            return
        print("Задача не отмечена как выполненная")

    def cmd_del(self, args: List[str]) -> None:
        if len(args) < 1:
            print("Ошибка: укажите id")
            return
        tid = int(args[0])
        ok = self.service.delete(tid)
        if ok:
            print("Задача удалена успешно")
            return
        print("Не удалось удалить задачу")

    def cmd_help(self, args: List[str] = []) -> None:
        print("""Task Tracker CLI - Использование:

Commands:
    add <description>       Добавить задачу
    update <id> <description> Обновить описание задачи
    delete <id>             Удалить задачу
    mark-in-progress <id>   Пометить задачу как в процессе
    mark-done <id>          Пометить задачу как выполненную
    list [status]           Посмотреть список задач (all, todo, in-progress, done)
    help                    Показать это сообщение""")

    def route(self):
        if len(sys.argv) < 2:
            self.cmd_help()
            return
        cmd, args = sys.argv[1].lower(), sys.argv[2:]
        func = self.command.get(cmd)
        if func:
            try:
                func(args)
                return
            except ValueError as e:
                print(f"Ошибка: id должно быть числом.\n\nПодробнее: {e}")
                return
            except Exception as e:
                print(f"Произошла ошибка. Подробнее: {e}")
                return
        print(f"Не известная команда '{cmd}'. Введите 'help")


def main():
    repo = JsonFileTaskRepository()
    service = TaskService(repo)
    handler = Handler(service)
    handler.route()


if __name__ == "__main__":
    main()
