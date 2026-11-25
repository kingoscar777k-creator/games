from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    if not DATABASE_URL:
        raise HTTPException(
            status_code=500,
            detail="Falta DATABASE_URL en las variables de entorno (.env)",
        )
    conn_url = DATABASE_URL
    if conn_url.startswith("postgres://"):
        conn_url = conn_url.replace("postgres://", "postgresql://", 1)
    return psycopg.connect(conn_url, row_factory=dict_row)


class VideojuegoEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    titulo: str = Field(min_length=1, max_length=160)
    plataforma: str = Field(default="Sin especificar", max_length=80)
    horas: int = Field(default=0, ge=0)
    puntuacion: float = Field(default=0, ge=0, le=10)
    imagen_url: Optional[str] = None
    precio: float = Field(default=0, ge=0)


class VideojuegoActualizacion(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=160)
    plataforma: Optional[str] = Field(default=None, max_length=80)
    horas: Optional[int] = Field(default=None, ge=0)
    puntuacion: Optional[float] = Field(default=None, ge=0, le=10)
    imagen_url: Optional[str] = None
    precio: Optional[float] = Field(default=None, ge=0)


app = FastAPI(
    title="GameDex API",
    description="API REST para gestionar el catálogo de videojuegos de GameDex.",
    version="1.0.0",
)

# CORS abierto para desarrollo. En producción, cambia '*' por el dominio del frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def iniciar_base_de_datos() -> None:
    if not DATABASE_URL:
        return
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS videojuegos (
                        id SERIAL PRIMARY KEY,
                        titulo TEXT NOT NULL,
                        plataforma TEXT NOT NULL DEFAULT 'Sin especificar',
                        horas INTEGER NOT NULL DEFAULT 0,
                        puntuacion REAL NOT NULL DEFAULT 0,
                        imagen_url TEXT,
                        precio REAL NOT NULL DEFAULT 0
                    )
                    """
                )
                cur.execute("SELECT id FROM videojuegos LIMIT 1")
                if cur.fetchone() is None:
                    json_path = BASE_DIR / "juegos.json"
                    if json_path.exists():
                        contenido = json.loads(json_path.read_text(encoding="utf-8-sig"))
                        juegos = contenido if isinstance(contenido, list) else [contenido]
                        for juego in juegos:
                            if isinstance(juego, dict) and juego.get("titulo"):
                                cur.execute(
                                    """
                                    INSERT INTO videojuegos
                                        (titulo, plataforma, horas, puntuacion, imagen_url, precio)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    """,
                                    (
                                        str(juego["titulo"]),
                                        str(juego.get("plataforma") or "Sin especificar"),
                                        max(0, int(juego.get("horas") or juego.get("horas_estimadas") or 0)),
                                        min(10.0, max(0.0, float(juego.get("puntuacion") or 0))),
                                        juego.get("imagen_url") or juego.get("portada_url"),
                                        max(0.0, float(juego.get("precio") or 0)),
                                    ),
                                )
            conn.commit()
    except Exception as exc:
        print(f"Aviso al iniciar BD: {exc}")


@app.get("/", tags=["Inicio"])
def inicio():
    return {
        "mensaje": "GameDex API funcionando",
        "documentacion": "/docs",
        "endpoints": "/videojuegos",
    }


@app.get("/health", tags=["Inicio"])
def health():
    return {"estado": "ok"}


@app.get("/videojuegos", tags=["Videojuegos"])
def listar_videojuegos(
    q: Optional[str] = Query(default=None, description="Buscar por título o plataforma"),
    plataforma: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    sql = """
        SELECT id, titulo, plataforma, horas, puntuacion, imagen_url, precio
        FROM videojuegos
        WHERE 1=1
    """
    params: list[object] = []

    if q:
        patron = f"%{q.strip()}%"
        sql += " AND (titulo ILIKE %s OR plataforma ILIKE %s)"
        params.extend([patron, patron])

    if plataforma:
        sql += " AND plataforma ILIKE %s"
        params.append(f"%{plataforma.strip()}%")

    sql += " ORDER BY id ASC LIMIT %s OFFSET %s"
    params.extend([limit, skip])

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


@app.get("/videojuegos/{videojuego_id}", tags=["Videojuegos"])
def obtener_videojuego(videojuego_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, titulo, plataforma, horas, puntuacion, imagen_url, precio
                FROM videojuegos
                WHERE id = %s
                """,
                (videojuego_id,),
            )
            juego = cur.fetchone()
            if juego is None:
                raise HTTPException(status_code=404, detail="Videojuego no encontrado")
            return juego


@app.post("/videojuegos", status_code=status.HTTP_201_CREATED, tags=["Videojuegos"])
def crear_videojuego(datos: VideojuegoEntrada):
    payload = datos.model_dump()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO videojuegos
                    (titulo, plataforma, horas, puntuacion, imagen_url, precio)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, titulo, plataforma, horas, puntuacion, imagen_url, precio
                """,
                (
                    payload["titulo"],
                    payload["plataforma"],
                    payload["horas"],
                    payload["puntuacion"],
                    payload["imagen_url"],
                    payload["precio"],
                ),
            )
            nuevo = cur.fetchone()
        conn.commit()
    return nuevo


@app.put("/videojuegos/{videojuego_id}", tags=["Videojuegos"])
def actualizar_videojuego(videojuego_id: int, datos: VideojuegoEntrada):
    payload = datos.model_dump()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE videojuegos
                SET titulo = %s,
                    plataforma = %s,
                    horas = %s,
                    puntuacion = %s,
                    imagen_url = %s,
                    precio = %s
                WHERE id = %s
                RETURNING id, titulo, plataforma, horas, puntuacion, imagen_url, precio
                """,
                (
                    payload["titulo"],
                    payload["plataforma"],
                    payload["horas"],
                    payload["puntuacion"],
                    payload["imagen_url"],
                    payload["precio"],
                    videojuego_id,
                ),
            )
            actualizado = cur.fetchone()
            if actualizado is None:
                raise HTTPException(status_code=404, detail="Videojuego no encontrado")
        conn.commit()
    return actualizado


@app.patch("/videojuegos/{videojuego_id}", tags=["Videojuegos"])
def editar_videojuego(videojuego_id: int, datos: VideojuegoActualizacion):
    cambios = datos.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(
            status_code=400, detail="Debes enviar al menos un campo para actualizar"
        )

    campos_permitidos = {
        "titulo": "titulo",
        "plataforma": "plataforma",
        "horas": "horas",
        "puntuacion": "puntuacion",
        "imagen_url": "imagen_url",
        "precio": "precio",
    }

    sets: list[str] = []
    params: list[object] = []
    for clave, valor in cambios.items():
        if clave in campos_permitidos:
            sets.append(f"{campos_permitidos[clave]} = %s")
            params.append(valor)

    params.append(videojuego_id)
    sql = f"""
        UPDATE videojuegos
        SET {", ".join(sets)}
        WHERE id = %s
        RETURNING id, titulo, plataforma, horas, puntuacion, imagen_url, precio
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            actualizado = cur.fetchone()
            if actualizado is None:
                raise HTTPException(status_code=404, detail="Videojuego no encontrado")
        conn.commit()
    return actualizado


@app.delete(
    "/videojuegos/{videojuego_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Videojuegos"],
)
def eliminar_videojuego(videojuego_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM videojuegos WHERE id = %s RETURNING id",
                (videojuego_id,),
            )
            eliminado = cur.fetchone()
            if eliminado is None:
                raise HTTPException(status_code=404, detail="Videojuego no encontrado")
        conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)