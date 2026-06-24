# Gestor de Tareas (To-Do API)

API REST para la gestión de tareas (un *to-do*) construida con **FastAPI**. Permite crear, consultar, actualizar y eliminar tareas, además de filtrarlas por su estado (completadas / no completadas). Cada tarea incluye un título, una descripción opcional, un nivel de prioridad y un indicador de si está completada.

> **Nota:** los datos se almacenan en memoria (una lista de Python), por lo que se reinician cada vez que se detiene el servidor. El proyecto está pensado como base de aprendizaje y como punto de partida para integrar una base de datos real más adelante.

---

## Características

La API expone las siguientes operaciones:

- **Listar todas las tareas.**
- **Filtrar tareas por estado:** ver solo las completadas o solo las no completadas.
- **Buscar una tarea por su `id`.**
- **Crear tareas** con `id` autogenerado por el servidor (el cliente no envía el `id`).
- **Actualizar una tarea existente**, devolviendo una comparación entre el estado anterior y el nuevo.
- **Eliminar una tarea** por su `id`.
- **Validación automática de datos** mediante Pydantic (título de 1 a 100 caracteres, prioridad entre 1 y 5, etc.).
- **Filtrado de respuestas con `response_model`**, de modo que el `id` interno no se expone en las respuestas.
- **Manejo de errores** con códigos HTTP apropiados (`201 Created` al crear, `404 Not Found` cuando la tarea no existe).
- **Documentación interactiva automática** generada por FastAPI (Swagger UI y ReDoc).

### Modelo de una tarea

| Campo         | Tipo            | Reglas                          | Obligatorio |
|---------------|-----------------|---------------------------------|-------------|
| `id`          | `int`           | Generado por el servidor        | —           |
| `titulo`      | `str`           | Entre 1 y 100 caracteres        | Sí          |
| `descripcion` | `str` / `null`  | Opcional (por defecto `null`)   | No          |
| `prioridad`   | `int`           | Entre 1 y 5                     | Sí          |
| `completada`  | `bool`          | Por defecto `false`             | No          |

### Endpoints

Todos los endpoints de tareas comparten el prefijo `/tareas`.

| Método   | Ruta                        | Descripción                                   | Código éxito |
|----------|-----------------------------|-----------------------------------------------|--------------|
| `GET`    | `/tareas`                   | Lista todas las tareas                        | `200`        |
| `GET`    | `/tareas/completadas`       | Lista solo las tareas completadas             | `200`        |
| `GET`    | `/tareas/no_completadas`    | Lista solo las tareas no completadas          | `200`        |
| `GET`    | `/tareas/{tarea_id}`        | Busca una tarea por su `id`                   | `200`        |
| `POST`   | `/tareas`                   | Crea una tarea nueva                          | `201`        |
| `PUT`    | `/tareas/{tarea_id}`        | Actualiza una tarea existente                 | `200`        |
| `DELETE` | `/tareas/{tarea_id}`        | Elimina una tarea por su `id`                 | `200`        |
| `GET`    | `/`                         | Endpoint raíz de comprobación                 | `200`        |

---

## Tecnologías

- **Python 3.10+** — el código usa la sintaxis moderna de tipos (`str | None`, `list[...]`).
- **FastAPI** `0.138.0` — framework web para construir la API.
- **Pydantic** `2.x` — validación de datos y definición de modelos.
- **Uvicorn** `0.49.0` — servidor ASGI para ejecutar la aplicación.
- **Starlette** — base sobre la que se apoya FastAPI (incluida como dependencia).

El detalle completo de dependencias está en [`requirements.txt`](./requirements.txt).

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Zhoom0/Gestor-de-tareas-To-Do-API-
cd "GESTOR DE TAREAS (TO-DO API)"
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En **Windows**:

```bash
venv\Scripts\activate
```

En **Linux / macOS**:

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar el servidor

Con el CLI de FastAPI (incluido en las dependencias):

```bash
fastapi dev main.py
```

O directamente con Uvicorn:

```bash
uvicorn main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

### Documentación interactiva

Una vez en marcha, FastAPI genera documentación automática que puedes explorar y probar desde el navegador:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## Estructura del proyecto

```
GESTOR DE TAREAS (TO-DO API)/
├── routers/
│   ├── __init__.py
│   └── tareas.py        # Modelos y endpoints de las tareas
├── venv/                # Entorno virtual (no se versiona)
├── .gitignore
├── main.py              # Punto de entrada: crea la app e incluye el router
├── README.md
└── requirements.txt     # Dependencias del proyecto
```

El archivo `main.py` crea la aplicación e incluye el router de tareas bajo el prefijo `/tareas`. Toda la lógica de los modelos y los endpoints vive en `routers/tareas.py`.

---

## Ejemplos de uso

### Crear una tarea

**Petición:**

```http
POST /tareas
Content-Type: application/json

{
  "titulo": "Estudiar FastAPI",
  "descripcion": "Repasar response_model y validaciones",
  "prioridad": 2,
  "completada": false
}
```

**Respuesta** (`201 Created`):

```json
{
  "mensaje": "se ha creado la tarea exitosamente"
}
```

### Actualizar una tarea

**Petición:**

```http
PUT /tareas/1
Content-Type: application/json

{
  "titulo": "Estudiar FastAPI a fondo",
  "descripcion": "Incluir manejo de errores",
  "prioridad": 1,
  "completada": true
}
```

**Respuesta** (`200 OK`):

```json
{
  "mensaje": "la tarea se ha modificado exitosamente",
  "tarea_antigua": {
    "titulo": "Estudiar FastAPI",
    "descripcion": "Repasar response_model y validaciones",
    "prioridad": 2,
    "completada": false
  },
  "tarea_actualizada": {
    "titulo": "Estudiar FastAPI a fondo",
    "descripcion": "Incluir manejo de errores",
    "prioridad": 1,
    "completada": true
  }
}
```

### Buscar una tarea inexistente

**Petición:**

```http
GET /tareas/999
```

**Respuesta** (`404 Not Found`):

```json
{
  "detail": "Tarea no encontrada"
}
```

---

## Posibles mejoras futuras

- Persistir las tareas en una **base de datos** (SQLite, PostgreSQL) para que no se pierdan al reiniciar.
- Añadir **paginación** al listado de tareas.
- Incorporar **autenticación** para proteger los endpoints.
- Escribir **pruebas automatizadas** con `pytest`.