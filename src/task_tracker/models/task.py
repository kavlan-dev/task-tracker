from dataclasses import dataclass
from typing import Optional


TASK_STATUS = {"todo": "todo", "in-progress": "in-progress", "done": "done"}


@dataclass
class TaskCreate:
    description: str


@dataclass
class TaskUpdate:
    description: Optional[str]
    status: Optional[str]


@dataclass
class TaskResponse:
    id: int
    description: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class Task:
    id: Optional[int]
    description: Optional[str]
    status: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
