# Prompt para Lovable - Frontend GameDex

Copia y pega TODO el contenido de abajo en Lovable:

---

Crea un frontend moderno y atractivo para una aplicación llamada **GameDex**, un catálogo de videojuegos.

IMPORTANTE:
- Solo frontend (React + Vite + TypeScript + Tailwind CSS).
- NO pidas backend, URL de Render, ni conexión real a API todavía.
- Usa datos mock (ficticios) por ahora.
- Diseño oscuro, estilo gaming, moderno y limpio.
- Responsive (móvil y escritorio).

Funcionalidades que debe tener:

1. **Página principal / Listado de videojuegos**
   - Grid de tarjetas de videojuegos
   - Cada tarjeta muestra: portada, título, plataforma, puntuación (estrellas o número), horas estimadas
   - Barra de búsqueda por título
   - Filtro por plataforma (Select)
   - Paginación simple

2. **Página de detalle de un videojuego**
   - Portada grande
   - Título, plataforma, puntuación, horas estimadas
   - Botones: Editar y Eliminar

3. **Formulario para Crear / Editar videojuego**
   - Campos:
     - Título (texto)
     - Plataforma (select o texto)
     - Horas estimadas (número)
     - Puntuación (0 a 10)
     - URL de portada (o placeholder de imagen)
   - Validación básica de campos

4. **Diseño general**
   - Navbar con logo "GameDex" y botón "Añadir juego"
   - Colores oscuros (fondo casi negro, acentos neón o morado/azul gaming)
   - Buenas animaciones suaves
   - Estados de carga y vacío ("No se encontraron juegos")

Usa datos mock de ejemplo (al menos 8-10 videojuegos ficticios).

Estructura clara de componentes y carpetas.

---

# Estructura del documento (Videojuego)

```json
{
  "id": "number (auto)",
  "titulo": "string (requerido)",
  "plataforma": "string (requerido)",
  "horas_estimadas": "number (mínimo 0)",
  "puntuacion": "number (0 a 10)",
  "portada_url": "string (URL de imagen o data URL)"
}
```

## Ejemplo de objeto

```json
{
  "id": 1,
  "titulo": "The Legend of Zelda: Breath of the Wild",
  "plataforma": "Nintendo Switch",
  "horas_estimadas": 50,
  "puntuacion": 9.5,
  "portada_url": "https://ejemplo.com/zelda.jpg"
}
```

## Datos mock de ejemplo

```json
[
  {
    "id": 1,
    "titulo": "The Legend of Zelda: Breath of the Wild",
    "plataforma": "Nintendo Switch",
    "horas_estimadas": 50,
    "puntuacion": 9.5,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co3p2d.jpg"
  },
  {
    "id": 2,
    "titulo": "Elden Ring",
    "plataforma": "PC",
    "horas_estimadas": 80,
    "puntuacion": 9.7,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co4jni.jpg"
  },
  {
    "id": 3,
    "titulo": "God of War Ragnarök",
    "plataforma": "PlayStation 5",
    "horas_estimadas": 30,
    "puntuacion": 9.4,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co5s5v.jpg"
  },
  {
    "id": 4,
    "titulo": "Hollow Knight",
    "plataforma": "PC",
    "horas_estimadas": 25,
    "puntuacion": 9.3,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1rgi.jpg"
  },
  {
    "id": 5,
    "titulo": "The Witcher 3: Wild Hunt",
    "plataforma": "PC",
    "horas_estimadas": 100,
    "puntuacion": 9.6,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1wyy.jpg"
  },
  {
    "id": 6,
    "titulo": "Red Dead Redemption 2",
    "plataforma": "PlayStation 4",
    "horas_estimadas": 60,
    "puntuacion": 9.5,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1q1f.jpg"
  },
  {
    "id": 7,
    "titulo": "Minecraft",
    "plataforma": "Multiplataforma",
    "horas_estimadas": 200,
    "puntuacion": 9.0,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co49x5.jpg"
  },
  {
    "id": 8,
    "titulo": "Among Us",
    "plataforma": "Mobile",
    "horas_estimadas": 10,
    "puntuacion": 8.0,
    "portada_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2tx4.jpg"
  }
]
```
