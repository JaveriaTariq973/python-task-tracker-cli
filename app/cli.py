'''
Se encarga de interpretar comandos y argumentos.
'''
import sys

from app.task_services import (
    add_task,
    list_tasks,
    update_task,
    delete_task,
    change_task_status,
)


def print_task(task: dict) -> None:
    print(
        f"[{task['id']}] {task['description']} | "
        f"status: {task['status']} | "
        f"createdAt: {task['createdAt']} | "
        f"updatedAt: {task['updatedAt']}"
    )


def print_task_list(tasks: list) -> None:
    if not tasks:
        print("No hay tareas para mostrar.")
        return

    for task in tasks:
        print_task(task)


def handle_command(args: list[str]) -> None:
    if not args:
        print("Debes proporcionar un comando.")
        return

    command = args[0]

    try:
        if command == "add":
            if len(args) < 2:
                print("Uso: python main.py add \"descripción\"")
                return

            description = args[1]
            task = add_task(description)
            print(f"Tarea agregada correctamente (ID: {task['id']})")

        elif command == "list":
            status = args[1] if len(args) > 1 else None
            tasks = list_tasks(status)
            print_task_list(tasks)

        elif command == "update":
            if len(args) < 3:
                print("Uso: python main.py update <id> \"nueva descripción\"")
                return

            task_id = int(args[1])
            new_description = args[2]
            updated_task = update_task(task_id, new_description)
            print(f"Tarea {updated_task['id']} actualizada correctamente.")

        elif command == "delete":
            if len(args) < 2:
                print("Uso: python main.py delete <id>")
                return

            task_id = int(args[1])
            delete_task(task_id)
            print(f"Tarea {task_id} eliminada correctamente.")

        elif command == "mark-in-progress":
            if len(args) < 2:
                print("Uso: python main.py mark-in-progress <id>")
                return

            task_id = int(args[1])
            task = change_task_status(task_id, "in-progress")
            print(f"Tarea {task['id']} marcada como in-progress.")

        elif command == "mark-done":
            if len(args) < 2:
                print("Uso: python main.py mark-done <id>")
                return

            task_id = int(args[1])
            task = change_task_status(task_id, "done")
            print(f"Tarea {task['id']} marcada como done.")

        else:
            print(f"Comando no reconocido: {command}")

    except ValueError as error:
        print(f"Error: {error}")