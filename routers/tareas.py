from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

router = APIRouter()

tareas = []

class Tarea(BaseModel):
    id: int
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None)
    prioridad: int = Field(ge=1, le=5)
    completada: bool = Field(default=False)

class Tarea_crear(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None)
    prioridad: int = Field(ge=1, le=5)
    completada: bool = Field(default=False)

class Tarea_actualizar(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None)
    prioridad: int = Field(ge=1, le=5)
    completada: bool = Field(default=False)

class Tarea_respuesta(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None)
    prioridad: int = Field(ge=1, le=5)
    completada: bool = Field(default=False)

class Respuesta_actualizacion(BaseModel):
    mensaje: str
    tarea_antigua: Tarea_respuesta
    tarea_actualizada: Tarea_respuesta


# GET
# Ver todas las tareas
@router.get("", response_model=list[Tarea_respuesta])
def mostrar_tareas():
    return tareas

# Mostrar solo tareas completadas
@router.get("/completadas", response_model=list[Tarea_respuesta])
def mostrar_completadas():
    return [tarea for tarea in tareas if tarea["completada"]]

# Mostrar solo tareas no completadas
@router.get("/no_completadas", response_model=list[Tarea_respuesta])
def mostrar_no_completadas():
    return [tarea for tarea in tareas if not tarea["completada"]]

# Buscar tarea por id
@router.get("/{tarea_id}", response_model=Tarea_respuesta)
def mostrar_tareaid(tarea_id: int):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            return tarea
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

# POST
# Crear tarea
@router.post("", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: Tarea_crear):
    nuevo_id = max([t["id"] for t in tareas], default=0) + 1
    tareas.append({**tarea.model_dump(), "id": nuevo_id})
    return {"mensaje": "se ha creado la tarea exitosamente"}

# PUT
# Actualizar tarea
@router.put("/{tarea_id}", response_model=Respuesta_actualizacion)
def actualizar_tarea(tarea_id: int, tarea_nueva: Tarea_actualizar):
    for indice, tarea in enumerate(tareas):
        if tarea["id"] == tarea_id:
            tarea_antigua = tareas[indice].copy()
            tareas[indice] = {**tarea_nueva.model_dump(), "id": tarea_id}
            return {"mensaje": "la tarea se ha modificado exitosamente", "tarea_antigua": tarea_antigua, "tarea_actualizada": tareas[indice]}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# DELETE
# Borrar una tarea
@router.delete("/{tarea_id}")
def borrar_tarea(tarea_id: int):
    for indice, tarea in enumerate(tareas):
        if tarea["id"] == tarea_id:
            tareas.pop(indice)
            return {"mensaje": "la tarea se ha eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")