import enum


class TaskStatus(str, enum.Enum):
    todo = "todo"
    done = "done"
