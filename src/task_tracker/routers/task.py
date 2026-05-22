from typing import List
import sys
from task_tracker.models.task import TASK_STATUS, TaskCreate, TaskUpdate
from task_tracker.services.task import TaskService


class Router:
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
            return
        new_task = TaskCreate(desc)
        task = self.service.create_task(new_task)
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
            print(f"Создано: {t.created_at}")
            print(f"Обновлено: {t.updated_at}")
            print("-" * 50)

    def cmd_update(self, args: List[str]) -> None:
        if len(args) < 2:
            print("Ошибка: укажите id и новое описание задачи")
            return
        tid = int(args[0])
        desc = " ".join(args[1:])
        task_update = TaskUpdate(desc, None)
        task = self.service.update_task(tid, task_update)
        if task:
            print("Задача обновлена успешно")
            return
        print("Не удалось обновить задачу")

    def cmd_in_progress(self, args: List[str]) -> None:
        if len(args) < 1:
            print("Ошибка: укажите id")
            return
        tid = int(args[0])
        task_update = TaskUpdate(None, TASK_STATUS["in-progress"])
        task = self.service.update_task(tid, task_update)
        if task:
            print("Задача успешно отмечена как в процессе")
            return
        print("Задача не отмечена как в процессе")

    def cmd_done(self, args: List[str]) -> None:
        if len(args) < 1:
            print("Ошибка: укажите id")
            return
        tid = int(args[0])
        task_update = TaskUpdate(None, TASK_STATUS["done"])
        task = self.service.update_task(tid, task_update)
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
