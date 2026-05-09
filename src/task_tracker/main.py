import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

TASKS_FILE = "tasks.json"


class Task:
    def __init__(self, task_id: str, description: str, status: str = "todo"):
        self.id = task_id
        self.description = description
        self.status = status
        self.createdAt = datetime.now().isoformat()
        self.updatedAt = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        task = cls(data["id"], data["description"], data["status"])
        task.createdAt = data["createdAt"]
        task.updatedAt = data["updatedAt"]
        return task


def get_task_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    max_id = max(int(task.id) for task in tasks)
    return max_id + 1


def load_tasks() -> List[Task]:
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        tasks_data = json.load(f)
        return [Task.from_dict(task_data) for task_data in tasks_data]


def save_tasks(tasks: List[Task]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        tasks_data = [task.to_dict() for task in tasks]
        json.dump(tasks_data, f, indent=2)


def add_task(description: str) -> Task:
    tasks = load_tasks()
    tid = str(get_task_id(tasks))
    new_task = Task(tid, description)
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


def list_tasks(status_filter: Optional[str] = None) -> List[Task]:
    tasks = load_tasks()
    if not status_filter:
        return tasks
    filtered_tasks = [task for task in tasks if task.status == status_filter]
    return filtered_tasks


def display_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("Задачи не найдены.")
        return

    print("Задачи:")
    print("-" * 50)
    for task in tasks:
        print(f"ID: {task.id}")
        print(f"Описание: {task.description}")
        print(f"Статус: {task.status}")
        print(f"Создано: {task.createdAt}")
        print(f"Обновлено: {task.updatedAt}")
        print("-" * 50)


def help_msg() -> str:
    return """Task Tracker CLI - Использование:

Commands:
    add <description>       Добавить задачу
    update <id> <description> Обновить описание задачи
    delete <id>             Удалить задачу
    mark-in-progress <id>   Пометить задачу как в процессе
    mark-done <id>          Пометить задачу как выполненную
    list [status]           Посмотреть список задач (all, todo, in-progress, done)
    help                    Показать это сообщение
"""


def main():
    if len(sys.argv) < 2:
        print("Ошибка: Команда не указана")
        print(help_msg())
        return

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    try:
        if command == "help":
            print(help_msg())
        elif command == "add":
            if len(args) < 1:
                print("Ошибка: Требуется описание задачи")
                print(help_msg())
                return
            description = " ".join(args)
            task = add_task(description)
            print(f"Задача успешно добавлена (ID: {task.id})")
        elif command == "list":
            status_filter = None
            if args:
                status_filter = args[0]
            tasks = list_tasks(status_filter)
            display_tasks(tasks)
        else:
            print(f"Неизвестная команда: {command}")
            print(help_msg())
            return
    except Exception as e:
        print(f"Ошибка {e}")
        return


if __name__ == "__main__":
    main()
