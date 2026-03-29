# 🧩 Task Tracker CLI

## 🇪🇸 Español

Aplicación simple de **interfaz de línea de comandos (CLI)** desarrollada en Python para gestionar tareas.
Este proyecto demuestra conceptos clave de backend como manejo de archivos, persistencia en JSON y diseño de CLI.

---

### 🚀 Funcionalidades

* Agregar nuevas tareas
* Actualizar tareas existentes
* Eliminar tareas
* Marcar tareas como **en progreso** o **completadas**
* Listar todas las tareas
* Filtrar tareas por estado:

  * `todo`
  * `in-progress`
  * `done`

---

### 🛠️ Tecnologías utilizadas

* **Python 3**
* Librerías estándar:

  * `sys` (manejo de argumentos CLI)
  * `json` (almacenamiento de datos)
  * `pathlib` (manejo de archivos)
  * `datetime` (timestamps)

> ⚠️ No se utilizaron librerías externas.

---

### 📁 Estructura del proyecto

task-tracker/
│
├── app/
│   ├── cli.py              # Manejo de comandos CLI
│   ├── task_service.py     # Lógica de negocio
│   ├── storage.py          # Manejo del archivo JSON
│   └── utils.py            # Funciones auxiliares
│
├── tasks.json              # Almacenamiento de datos
├── main.py                 # Punto de entrada
├── README.md
└── .gitignore
```

---

### ⚙️ Instalación y ejecución

1. Clonar el repositorio:

```
git clone https://github.com/your-username/task-tracker-cli.git
cd task-tracker-cli
```

2. Verificar Python:

```
python --version
```

3. Ejecutar la aplicación:

```
python main.py <comando> [argumentos]
```

---

### 💻 Uso

#### ➕ Agregar tarea

```
python main.py add "Comprar despensa"
```

#### 📋 Listar tareas

```
python main.py list
```

#### 📌 Filtrar por estado

```
python main.py list done
python main.py list todo
python main.py list in-progress
```

#### ✏️ Actualizar tarea

```
python main.py update 1 "Comprar despensa y cocinar"
```

#### 🗑️ Eliminar tarea

```
python main.py delete 1
```

#### 🔄 Cambiar estado

```
python main.py mark-in-progress 1
python main.py mark-done 1
```

---

### 🧱 Modelo de datos

```
{
  "id": 1,
  "description": "Comprar despensa",
  "status": "todo",
  "createdAt": "2026-03-29T10:00:00",
  "updatedAt": "2026-03-29T10:00:00"
}
```

---

### ⚠️ Manejo de errores

La aplicación contempla:

* Comandos inválidos
* Argumentos faltantes
* IDs inexistentes
* Estados inválidos
* Archivo JSON corrupto

---

### 📌 Mejoras futuras

* Agregar pruebas con `pytest`
* Implementar `argparse`
* Soporte para prioridades
* Empaquetar como herramienta instalable
* Agregar logging

---

### 👨‍💻 Autor

Cristopher — QA Engineer 

---

---

## 🇺🇸 English

A simple **Command Line Interface (CLI)** application built with Python to manage tasks.
This project demonstrates key backend concepts such as file handling, JSON persistence, and CLI design.

---

### 🚀 Features

* Add new tasks
* Update existing tasks
* Delete tasks
* Mark tasks as **in-progress** or **done**
* List all tasks
* Filter tasks by status:

  * `todo`
  * `in-progress`
  * `done`

---

### 🛠️ Technologies Used

* **Python 3**
* Standard libraries:

  * `sys` (CLI argument handling)
  * `json` (data persistence)
  * `pathlib` (file handling)
  * `datetime` (timestamps)

> ⚠️ No external libraries were used.

---

### 📁 Project Structure

```
task-tracker/
│
├── app/
│   ├── cli.py
│   ├── task_service.py
│   ├── storage.py
│   └── utils.py
│
├── tasks.json
├── main.py
├── README.md
└── .gitignore
```

---

### ⚙️ Installation & Setup

1. Clone the repository:

```
git clone https://github.com/your-username/task-tracker-cli.git
cd task-tracker-cli
```

2. Check Python version:

```
python --version
```

3. Run the application:

```
python main.py <command> [arguments]
```

---

### 💻 Usage

#### ➕ Add a task

```
python main.py add "Buy groceries"
```

#### 📋 List tasks

```
python main.py list
```

#### 📌 Filter by status

```
python main.py list done
python main.py list todo
python main.py list in-progress
```

#### ✏️ Update a task

```
python main.py update 1 "Buy groceries and cook dinner"
```

#### 🗑️ Delete a task

```
python main.py delete 1
```

#### 🔄 Change status

```
python main.py mark-in-progress 1
python main.py mark-done 1
```

---

### 🧱 Data Model

```
{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "createdAt": "2026-03-29T10:00:00",
  "updatedAt": "2026-03-29T10:00:00"
}
```

---

### ⚠️ Error Handling

The application handles:

* Invalid commands
* Missing arguments
* Non-existent IDs
* Invalid status values
* Corrupted JSON file

---

### 📌 Future Improvements

* Add tests using `pytest`
* Implement `argparse`
* Add task priorities
* Package as an installable CLI tool
* Add logging system

---

### 👨‍💻 Author

Cristopher — QA Engineer 

---


