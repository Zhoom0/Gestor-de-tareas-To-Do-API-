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
@router.get("")
def mostrar_tareas():
    return tareas

# POST
@router.post("", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: Tarea):
    tareas.append(tarea.model_dump())
    return {"mensaje": "se ha creado la tarea exitosamente"}