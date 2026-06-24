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
@router.get("")
def mostrar_tareas():
    return tareas

# BUSCAR TAREA POR ID
@router.get("/{tarea_id}")
def mostrar_tareaid(tarea_id: int):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            return {"mensaje": "tarea encontrada", "tarea": tarea}
    raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

# POST
# Crear tarea
@router.post("", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: Tarea):
    tareas.append(tarea.model_dump())
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