# GameDex API

API REST de videojuegos desarrollada con FastAPI. Incluye operaciones CRUD, búsqueda, filtros, paginación, documentación Swagger y persistencia con SQLite local o PostgreSQL/Supabase.

## 1. Instalar y ejecutar en local

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre `http://127.0.0.1:8000/docs` para probar la API. Sin configurar nada, se crea `gamedex.db` (SQLite) y se importan los datos de `juegos.json` si la tabla está vacía.

## 2. Usar Supabase (PostgreSQL)

1. En Supabase abre **Project Settings → Database** y copia el connection string PostgreSQL (URI).
2. Copia `.env.example` a `.env` y configura `DATABASE_URL` con tu URI real. No compartas ni subas `.env` a GitHub.
3. Instala dependencias y arranca la API. La tabla `videojuegos` se crea automáticamente al iniciar.

La contraseña y URL reales de Supabase no están incluidas en este ZIP: debes añadirlas tú en `.env` o como variables de entorno del hosting.

## 3. Endpoints

| Método | Ruta | Acción |
|---|---|---|
| GET | `/` | Estado e información de la API |
| GET | `/health` | Comprobación de salud |
| GET | `/videojuegos` | Listar videojuegos |
| GET | `/videojuegos/{id}` | Obtener uno por ID |
| POST | `/videojuegos` | Crear videojuego |
| PUT | `/videojuegos/{id}` | Reemplazar todos sus campos editables |
| PATCH | `/videojuegos/{id}` | Actualizar solo los campos enviados |
| DELETE | `/videojuegos/{id}` | Eliminar videojuego |

### Búsqueda y filtros

`GET /videojuegos?q=mario&plataforma=Switch&skip=0&limit=20`

### Ejemplo para crear un videojuego

```json
{
  "titulo": "The Legend of Zelda: Breath of the Wild",
  "plataforma": "Nintendo Switch",
  "horas_estimadas": 50,
  "puntuacion": 9.5,
  "portada_url": "https://ejemplo.com/portada.jpg"
}
```

`puntuacion` debe estar entre 0 y 10 y `horas_estimadas` no puede ser negativo. `portada_url` puede ser una URL o un valor de imagen compatible, como un data URL.

## 4. Despliegue en Render

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Añade `DATABASE_URL` en Environment si vas a usar Supabase.
- Configura `CORS_ORIGINS` con el dominio exacto del frontend cuando lo conectes. Mientras esté en `*`, cualquier origen podrá realizar peticiones sin credenciales.

## Nota

La API queda preparada para conectar con un frontend más adelante, pero no está conectada a Google Stitch ni desplegada en Render. Para usar Supabase hace falta introducir las credenciales de tu propio proyecto.
