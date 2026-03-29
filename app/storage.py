'''
Se encarga de leer y escribir el archivo JSON.
'''

import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def ensure_tasks_file_exists() -> None:
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def load_tasks() -> list:
    ensure_tasks_file_exists()

    try:
        content = TASKS_FILE.read_text(encoding="utf-8").strip()

        if not content:
            return []

        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("El archivo tasks.json está corrupto o no contiene JSON válido.")


def save_tasks(tasks: list) -> None:
    TASKS_FILE.write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    
