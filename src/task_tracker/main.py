import json
import os
import sys
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

TASKS_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    description: str
    status: str = "todo"
    createdAt: str = datetime.now().isoformat()
    updatedAt: str = datetime.now().isoformat()


def load_tasks() -> List[Task]:
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        tasks_data = json.load(f)
        return [Task(**task_data) for task_data in tasks_data]


def save_tasks(tasks: List[Task]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump([task.__dict__ for task in tasks], f, indent=2)


def get_task_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1

    return max(task.id for task in tasks) + 1


def find_task_by_id(tasks: List[Task], task_id: int) -> Optional[Task]:
    for task in tasks:
        if task.id == task_id:
            return task

    return None


def add_task(args: List[str]) -> Optional[Task]:
    tasks = load_tasks()
    desc = " ".join(args)
    if not desc:
        return
    tid = get_task_id(tasks)
    new_task = Task(tid, desc)
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


def update_task(args: List[str]) -> Optional[Task]:
    tasks = load_tasks()
    tid = int(args[0])
    task = find_task_by_id(tasks, tid)
    if not task:
        return
    new_desc = " ".join(args[1:])
    task.description = new_desc
    task.updatedAt = datetime.now().isoformat()
    save_tasks(tasks)
    return task


def delete_task(args: List[str]) -> bool:
    tasks = load_tasks()
    tid = int(args[0])
    task = find_task_by_id(tasks, tid)
    if not task:
        return False

    tasks.remove(task)
    save_tasks(tasks)
    return True


def list_tasks(args: List[str] = []) -> List[Task]:
    tasks = load_tasks()
    if not args:
        return tasks
    status_filter = args[0]
    filtered_tasks = [task for task in tasks if task.status == status_filter]
    return filtered_tasks


def display_tasks(tasks: List[Task]) -> None:
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
            task = add_task(args)
            if not task:
                print("Ошибка: описание задачи не может быть пустым")
                return
            print(f"Задача успешно добавлена (ID: {task.id})")
        elif command == "list":
            tasks = list_tasks(args)
            if not tasks:
                print("Задачи не найдены.")
                return
            display_tasks(tasks)
        elif command == "update":
            if len(args) < 2:
                print("Ошибка: Требуется ID задачи и новое описание")
                print(help_msg())
                return
            task = update_task(args)
            if not task:
                print("Ошибка: не удалось обновить задачу")
                return
            print("Задача успешно обновлена")
        elif command == "delete":
            if len(args) < 1:
                print("Ошибка: Требуется ID задачи")
                print(help_msg())
                return
            success = delete_task(args)
            if not success:
                print("Ошибка: не удалось удалить задачу")
                return
            print("Задача успешно удалена")
        else:
            print(f"Неизвестная команда: {command}")
            print(help_msg())
            return
    except ValueError as e:
        print(f"Ошибка: id должно быть числом.\n\nПодробнее: {e}")
    except Exception as e:
        print(f"Ошибка {e}")
        return


if __name__ == "__main__":
    main()
