# AGENTS.md — Gym Tracker

## Qué es
Aplicación local de un solo usuario para registrar entrenamientos de pesas:
ejercicios, plantillas semanales, sesiones serie por serie, historial y análisis.

## Stack
Python 3.15, FastAPI, Uvicorn, Jinja2, SQLite (`sqlite3` estándar) y pytest.
CSS propio y JavaScript mínimo. Sin ORM y sin servicios externos.

## Comandos
```powershell
# Instalar (desde la raíz del repo)
py -3.15 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

# Ejecutar
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
# Abrir http://127.0.0.1:8000

# Probar
.venv\Scripts\python.exe -m pytest
```

## Convenciones
- Código (nombres, comentarios técnicos) en inglés.
- Textos de interfaz y documentación en español.
- Peso siempre en kilogramos; fechas en hora local (`AAAA-MM-DD`).

## Reglas
- Antes de tocar código, leer `docs/constitution.md`, la spec activa
  (`specs/001-gym-tracker/spec.md`), `plan.md` y `tasks.md`.
- Una tarea por vez: prueba que falla, código, `pytest` en verde, marcar y parar.
- La spec manda: si falta una decisión, frenar y preguntar.

## Límites
- No agregar dependencias sin preguntar.
- No implementar nada fuera de la tarea actual.
