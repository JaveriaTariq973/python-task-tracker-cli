'''
Punto de entrada del programa. Desde aquí arrancas la CLI.
'''
import sys
from app.cli import handle_command


if __name__ == "__main__":
    handle_command(sys.argv[1:])