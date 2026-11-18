# TodoTrabajo

Plataforma web para **ofrecer servicios** o **publicar encargos**, organizada por categorías y por región/comuna en todo Chile.

**Stack:** Django 5.1 · PostgreSQL 16 · HTMX · Tailwind · Docker Compose

## Levantar el proyecto

```bash
cp .env.example .env
docker compose up --build
# en otra terminal:
docker compose exec web python manage.py createsuperuser
```

- Sitio: http://localhost:8000
- Admin: http://localhost:8000/admin

Las migraciones cargan automáticamente las **16 regiones, 346 comunas** y las **categorías iniciales**.

### Sin Docker (rápido, con SQLite)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

(Si no hay `DATABASE_URL` definida, se usa SQLite.)

## Tests

```bash
docker compose exec web python manage.py test
```

## Estructura

```
config/            settings, urls, wsgi/asgi
apps/
  cuentas/         Usuario (login con email) + Perfil (se crea solo)
  ubicaciones/     Region, Comuna (+ datos.py con todo Chile)
  publicaciones/   Categoria (con subcategorías), Publicacion (oferta | encargo)
  chat/            Conversacion (publicación + interesado), Mensaje
templates/         base.html + plantillas por app
```

## Reglas de negocio ya implementadas

- El login es por **email** (no hay username).
- Una publicación con precio **fijo** o **por hora** debe tener monto (restricción en la BD). Si es **a convenir**, el monto es opcional.
- Hay **una sola conversación** por (publicación, interesado), y el autor no puede abrir chat sobre su propia publicación.
- Solo los dos participantes pueden escribir mensajes en una conversación.
- Cada mensaje nuevo sube su conversación al tope de la bandeja.

## Roadmap

| Sprint | Contenido | Estado |
|---|---|---|
| 1 | Setup, modelos, datos iniciales, admin | ✅ |
| 2 | Registro, login, logout y edición de perfil | ⏳ |
| 3 | CRUD de publicaciones + listado con filtros (tipo, categoría, región → comuna con HTMX) | |
| 4 | Chat: botón "Contactar", bandeja y conversación con polling HTMX | |
| 5 | Pulido, tests, assets locales y deploy | |
| v2 | Chat en tiempo real (Channels + Redis), reseñas, notificaciones | |
