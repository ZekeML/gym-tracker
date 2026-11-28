# MEMORY — Gym Tracker

## Estado actual
- Spec 001 (fase 1) aprobada. T1 y T2 completadas; T3 no iniciada.
- Python 3.15.0 funciona: todas las dependencias instalaron con wheels para 3.15.
  No se usó el respaldo de Python 3.13/3.14.
- `.venv` creado en la raíz; dependencias en `requirements.txt` (sin versiones fijas).
- `app/main.py` crea FastAPI y sirve `/` con `app/templates/index.html`.
- `app/schema.sql` define las 5 tablas y sus restricciones.
- `app/db.py`: `connect(path)` activa `PRAGMA foreign_keys = ON` en cada conexión;
  `init_db(path)` crea las tablas si faltan y fija `PRAGMA user_version = 1`.
- `pytest`: 29 pruebas en verde (`tests/test_app.py` y `tests/test_db.py`).

## Decisiones
- `pytest.ini` agrega la raíz al `pythonpath` para importar `app` al correr `pytest`.
- Starlette 1.10 avisa que `httpx` está deprecado para su TestClient
  (sugiere `httpx2`). Es solo una advertencia; no se cambió la dependencia
  porque el plan fija `httpx`.
- Las carpetas vacías del plan (`app/logic`, `app/static`, `scripts`) quedan
  sin archivos hasta que sus tareas las usen.
- `exercise.name_key` es una columna normal: la normalización (minúsculas) la
  hará la capa de aplicación en T4; la base solo garantiza su unicidad.
- Las claves foráneas de `template_item.template_version_id` y
  `session_set.session_id` usan el comportamiento por defecto (NO ACTION),
  porque el plan solo pide `ON DELETE RESTRICT` para `exercise_id`.
- `init_db` es idempotente (`CREATE TABLE IF NOT EXISTS`) y se puede llamar
  sobre una base existente sin perder datos.
- Las pruebas de base usan `tmp_path` de pytest; nunca tocan `data/`.

## Siguiente
- T3: lógica pura de la fase 1.
