# API CRUD de Videojuegos - gamesgg

## Descripción

Proyecto de una API para gestionar un catálogo de videojuegos. Está desarrollado
con Python, FastAPI y Pydantic. La versión CRUD de la actividad guarda los datos
en `videojuegos.json`, por lo que los cambios permanecen al reiniciar el servidor.

Además, el proyecto incluye `supabase.sql`, un ejercicio complementario basado
en el taller de introducción a SQL con Supabase. Este archivo permite crear una
tabla de videojuegos, insertar datos y practicar SELECT, INSERT, UPDATE y DELETE.

**Importante:** la API de FastAPI de este proyecto sigue usando el JSON. El archivo
SQL es para practicar en Supabase; no conecta automáticamente FastAPI con Supabase.

## Archivos

- `main.py`: aplicación FastAPI con las cinco rutas CRUD.
- `models.py`: modelo Pydantic y validaciones.
- `videojuegos.json`: datos iniciales y almacenamiento persistente de la API.
- `supabase.sql`: creación de tabla y ejemplos SQL para Supabase.
- `GamesGG.postman_collection.json`: colección de Postman lista para importar.
- `requirements.txt`: dependencias de Python.

## Instalación

Necesitas Python 3.10 o superior. Abre una terminal en esta carpeta y ejecuta:

```bash
pip install -r requirements.txt
```

## Arrancar la API

```bash
uvicorn main:app --reload
```

API: http://127.0.0.1:8000

Documentación interactiva: http://127.0.0.1:8000/docs

## Rutas de la API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/videojuegos` | Lista los videojuegos |
| GET | `/videojuegos/{id}` | Busca un videojuego por ID |
| POST | `/videojuegos` | Agrega un videojuego con ID automático |
| PUT | `/videojuegos/{id}` | Edita un videojuego |
| DELETE | `/videojuegos/{id}` | Elimina un videojuego |

## Filtros

- `/videojuegos?genero=Aventura`
- `/videojuegos?plataforma=PC`
- `/videojuegos?genero=Aventura&plataforma=PC`

## Validaciones y errores

- `404`: el videojuego solicitado no existe.
- `409`: ya existe un videojuego con el mismo título y plataforma.
- El año debe estar entre 1950 y 2100.
- La nota debe estar entre 1 y 10.
- El ID se calcula automáticamente.

## Guardado en JSON

Las operaciones de agregar, editar y borrar escriben los cambios en `videojuegos.json`.
Al reiniciar el servidor, los datos continúan guardados.

## Probar la API con Postman

1. Descarga e instala la **app de escritorio** de Postman desde https://www.postman.com/downloads/  
   (no uses la versión web: no puede llegar a tu `localhost`).

2. Arranca el servidor de la API (`uvicorn main:app --reload`).

3. En Postman ve a **Collections** → **Import** y selecciona el archivo  
   `GamesGG.postman_collection.json` de esta carpeta.

4. Se creará la colección **GamesGG - API de Videojuegos** con estas peticiones:

   | Petición | Método | Qué hace |
   |---|---|---|
   | Listar todos | GET | `/videojuegos` |
   | Filtrar por género | GET | `/videojuegos?genero=Aventura` |
   | Filtrar por plataforma | GET | `/videojuegos?plataforma=PC` |
   | Filtrar combinado | GET | género + plataforma |
   | Buscar por ID | GET | `/videojuegos/1` |
   | Agregar | POST | crea un videojuego nuevo |
   | Editar | PUT | modifica el ID 1 |
   | Borrar | DELETE | elimina el ID 5 |

5. Abre cualquier petición y pulsa **Send**.

**Compruebo:**
- La respuesta muestra el JSON esperado.
- Arriba aparece `200 OK`, `201 Created` o el código de error correspondiente.
- En la terminal del servidor aparece la línea de la petición (por ejemplo `GET /videojuegos`).

Si sale `Could not send request` o `ECONNREFUSED`, el servidor está apagado o la URL tiene un error. Revisa que el puerto sea **8000**.

## Práctica de SQL con Supabase

1. Entra en https://supabase.com e inicia sesión.
2. Crea una organización si Supabase te lo solicita y crea un proyecto.
3. Abre el **SQL Editor** de tu proyecto.
4. Abre el archivo `supabase.sql` de esta carpeta.
5. Copia su contenido en el editor SQL y pulsa **Run**.
6. En **Table Editor**, comprueba que aparece la tabla `videojuegos`.

El script crea la tabla, inserta cinco videojuegos de ejemplo y contiene consultas
para practicar las operaciones CRUD:

| Operación CRUD | Instrucción SQL | Para qué sirve |
|---|---|---|
| Crear | `INSERT` | Añadir una fila |
| Leer | `SELECT` | Consultar filas |
| Actualizar | `UPDATE` | Modificar una fila |
| Borrar | `DELETE` | Eliminar una fila |

También puedes probar los filtros con `WHERE`.

**Precaución:** las consultas `UPDATE` y `DELETE` modifican datos reales de la tabla.
Ejecuta solo las consultas que quieras probar y revisa siempre su condición `WHERE`.
