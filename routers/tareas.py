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

# GET
# TODAS LAS TAREAS
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
@router.post("", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: Tarea):
    tareas.append(tarea.model_dump())
    return {"mensaje": "se ha creado la tarea exitosamente"}