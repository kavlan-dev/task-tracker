from task_tracker.repositories.task import JsonFileTaskRepository
from task_tracker.routers.task import Router
from task_tracker.services.task import TaskService


def main():
    repo = JsonFileTaskRepository("tasks.json")
    service = TaskService(repo)
    router = Router(service)
    router.route()


if __name__ == "__main__":
    main()
