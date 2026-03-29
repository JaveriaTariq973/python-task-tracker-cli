'''
Contiene la lógica principal de tareas:
agregar
listar
actualizar
eliminar
cambiar estado
'''

from app.storage import load_tasks, save_tasks
from app.utils import get_current_timestamp


VALID_STATUSES = {"todo", "in-progress", "done"}


def generate_next_id(tasks: list) -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(description: str) -> dict:
    tasks = load_tasks()
    timestamp = get_current_timestamp()

    new_task = {
        "id": generate_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp
    }

    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


def list_tasks(status: str | None = None) -> list:
    tasks = load_tasks()

    if status is None:
        return tasks

    if status not in VALID_STATUSES:
        raise ValueError(f"Estado inválido: {status}")

    return [task for task in tasks if task["status"] == status]


def find_task_by_id(tasks: list, task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(task_id: int, new_description: str) -> dict:
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        raise ValueError(f"No existe una tarea con ID {task_id}")

    task["description"] = new_description
    task["updatedAt"] = get_current_timestamp()

    save_tasks(tasks)
    return task


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        raise ValueError(f"No existe una tarea con ID {task_id}")

    tasks.remove(task)
    save_tasks(tasks)


def change_task_status(task_id: int, status: str) -> dict:
    if status not in VALID_STATUSES:
        raise ValueError(f"Estado inválido: {status}")

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        raise ValueError(f"No existe una tarea con ID {task_id}")

    task["status"] = status
    task["updatedAt"] = get_current_timestamp()

    save_tasks(tasks)
    return task
