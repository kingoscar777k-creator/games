from pydantic import BaseModel, Field


class Videojuego(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    genero: str = Field(min_length=2, max_length=50)
    plataforma: str = Field(min_length=2, max_length=50)
    anio: int = Field(ge=1950, le=2100)
    nota: float = Field(ge=1, le=10)
