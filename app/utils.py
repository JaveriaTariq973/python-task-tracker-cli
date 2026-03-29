'''
Funciones auxiliares, como timestamps o validaciones pequeñas.
'''

from datetime import datetime


def get_current_timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")