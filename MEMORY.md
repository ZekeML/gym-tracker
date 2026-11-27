# MEMORY — Gym Tracker

## Estado actual
- Spec 001 (fase 1) aprobada. T1 completada; T2 no iniciada.
- Python 3.15.0 funciona: todas las dependencias instalaron con wheels para 3.15.
  No se usó el respaldo de Python 3.13/3.14.
- `.venv` creado en la raíz; dependencias en `requirements.txt` (sin versiones fijas).
- `app/main.py` crea FastAPI y sirve `/` con `app/templates/index.html`.
- `pytest`: 1 prueba en verde (`tests/test_app.py`).

## Decisiones
- `pytest.ini` agrega la raíz al `pythonpath` para importar `app` al correr `pytest`.
- Starlette 1.10 avisa que `httpx` está deprecado para su TestClient
  (sugiere `httpx2`). Es solo una advertencia; no se cambió la dependencia
  porque el plan fija `httpx`.
- Las carpetas vacías del plan (`app/logic`, `app/static`, `scripts`) quedan
  sin archivos hasta que sus tareas las usen.

## Siguiente
- T2: base de datos y restricciones.
