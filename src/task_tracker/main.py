from task_tracker.depends import (
    get_config,
    get_json_file_task_repository,
    get_task_router,
    get_task_service,
)


def main():
    cfg = get_config()
    repo = get_json_file_task_repository(cfg.path)
    service = get_task_service(repo)
    router = get_task_router(service)
    router.route()


if __name__ == "__main__":
    main()
