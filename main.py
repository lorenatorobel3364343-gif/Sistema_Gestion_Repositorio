# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="API Biblioteca Pública - ADSO",
    description="API RESTful completa con operaciones CRUD para auditoría de servicios web",
    version="2.0.0"
)


# Modelo de Datos con Pydantic para validación automática
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    anio_publicacion: int
    disponible: bool = True


# Modelo auxiliar para la actualización parcial o total
class LibroUpdate(BaseModel):
    titulo: str
    autor: str
    anio_publicacion: int
    disponible: bool


# Base de datos simulada en memoria
db_libros: List[Libro] = [
    Libro(id=1, titulo="Cien Años de Soledad", autor="Gabriel García Márquez", anio_publicacion=1967, disponible=True),
    Libro(id=2, titulo="Don Quijote de la Mancha", autor="Miguel de Cervantes", anio_publicacion=1605, disponible=False)
]


# ---------------------------------------------------------------------
# ENDPOINTS / RUTAS DE LA API (CRUD COMPLETO)
# ---------------------------------------------------------------------

# 1. READ ALL (Obtener todos los libros)
@app.get("/api/v1/libros", response_model=List[Libro], status_code=status.HTTP_200_OK)
def obtener_todos_los_libros():
    return db_libros


# 2. READ ONE (Obtener un libro específico por ID)
@app.get("/api/v1/libros/{libro_id}", response_model=Libro, status_code=status.HTTP_200_OK)
def obtener_libro_por_id(libro_id: int):
    for libro in db_libros:
        if libro.id == libro_id:
            return libro
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El libro con ID {libro_id} no existe en el sistema de la biblioteca."
    )


# 3. CREATE (Registrar un nuevo libro)
@app.post("/api/v1/libros", response_model=Libro, status_code=status.HTTP_201_CREATED)
def crear_nuevo_libro(libro: Libro):
    # Validar si el ID ya existe
    for l in db_libros:
        if l.id == libro.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de registro: Ya existe un libro con el ID {libro.id}."
            )
    db_libros.append(libro)
    return libro


# 4. UPDATE (Actualizar un libro existente - Método PUT)
@app.put("/api/v1/libros/{libro_id}", response_model=Libro, status_code=status.HTTP_200_OK)
def actualizar_libro(libro_id: int, datos_actualizados: LibroUpdate):
    for index, libro in enumerate(db_libros):
        if libro.id == libro_id:
            libro_modificado = Libro(
                id=libro_id,
                titulo=datos_actualizados.titulo,
                autor=datos_actualizados.autor,
                anio_publicacion=datos_actualizados.anio_publicacion,
                disponible=datos_actualizados.disponible
            )
            db_libros[index] = libro_modificado
            return libro_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El libro con ID {libro_id} no fue encontrado."
    )


# 5. DELETE (Eliminar un libro de la biblioteca)
@app.delete("/api/v1/libros/{libro_id}", status_code=status.HTTP_200_OK)
def eliminar_libro(libro_id: int):
    for index, libro in enumerate(db_libros):
        if libro.id == libro_id:
            db_libros.pop(index)
            return {"mensaje": f"El libro con ID {libro_id} fue eliminado exitosamente."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El libro con ID {libro_id} no existe."
    )