import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from models import Videojuego

app = FastAPI(
    title="API de Videojuegos",
    description="API CRUD para gestionar un catálogo de videojuegos",
    version="1.0.0",
)

ARCHIVO = Path(__file__).parent / "videojuegos.json"


def cargar_videojuegos():
    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_videojuegos(videojuegos):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(videojuegos, archivo, indent=4, ensure_ascii=False)


@app.get("/videojuegos", tags=["Videojuegos"])
def listar_videojuegos(genero: str | None = None, plataforma: str | None = None):
    videojuegos = cargar_videojuegos()
    if genero is not None:
        videojuegos = [v for v in videojuegos if v["genero"].lower() == genero.lower()]
    if plataforma is not None:
        videojuegos = [v for v in videojuegos if v["plataforma"].lower() == plataforma.lower()]
    return videojuegos


@app.get("/videojuegos/{id}", tags=["Videojuegos"])
def buscar_videojuego(id: int):
    for videojuego in cargar_videojuegos():
        if videojuego["id"] == id:
            return videojuego
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")


@app.post("/videojuegos", status_code=status.HTTP_201_CREATED, tags=["Videojuegos"])
def agregar_videojuego(videojuego: Videojuego):
    videojuegos = cargar_videojuegos()
    for existente in videojuegos:
        if (existente["titulo"].casefold() == videojuego.titulo.casefold()
                and existente["plataforma"].casefold() == videojuego.plataforma.casefold()):
            raise HTTPException(status_code=409, detail="Este videojuego ya existe en esa plataforma")
    nuevo_id = max((v["id"] for v in videojuegos), default=0) + 1
    nuevo = {"id": nuevo_id, **videojuego.model_dump()}
    videojuegos.append(nuevo)
    guardar_videojuegos(videojuegos)
    return nuevo


@app.put("/videojuegos/{id}", tags=["Videojuegos"])
def editar_videojuego(id: int, datos: Videojuego):
    videojuegos = cargar_videojuegos()
    for indice, videojuego in enumerate(videojuegos):
        if videojuego["id"] == id:
            for existente in videojuegos:
                if (existente["id"] != id
                        and existente["titulo"].casefold() == datos.titulo.casefold()
                        and existente["plataforma"].casefold() == datos.plataforma.casefold()):
                    raise HTTPException(status_code=409, detail="Este videojuego ya existe en esa plataforma")
            actualizado = {"id": id, **datos.model_dump()}
            videojuegos[indice] = actualizado
            guardar_videojuegos(videojuegos)
            return actualizado
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")


@app.delete("/videojuegos/{id}", tags=["Videojuegos"])
def borrar_videojuego(id: int):
    videojuegos = cargar_videojuegos()
    for indice, videojuego in enumerate(videojuegos):
        if videojuego["id"] == id:
            eliminado = videojuegos.pop(indice)
            guardar_videojuegos(videojuegos)
            return {"mensaje": "Videojuego eliminado correctamente", "videojuego": eliminado}
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")
