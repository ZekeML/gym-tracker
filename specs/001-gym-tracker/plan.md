# Plan 001 — Gym Tracker

Estado: borrador
Spec: specs/001-gym-tracker/spec.md (aprobada)

## Stack
- Python 3.11 o superior, FastAPI con Uvicorn, plantillas Jinja2 (el servidor genera el HTML), `sqlite3` de la biblioteca estándar y `pytest`.
- Dependencias externas: `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `httpx` (solo para pruebas) y `pytest`, listadas en `requirements.txt`.
- CSS propio y JavaScript mínimo (solo para agregar una fila de serie extra).
- Cubre: RNF-1, RNF-2, RNF-7.

## Archivos y responsabilidades
| Archivo | Responsabilidad |
|---|---|
| `app/main.py` | Crea la aplicación y define las rutas (recibe pedidos y devuelve páginas). |
| `app/db.py` | Abre la conexión, activa claves foráneas y crea las tablas si no existen. |
| `app/schema.sql` | Definición de tablas y restricciones. |
| `app/repository.py` | Todas las consultas SQL (leer y guardar). No contiene reglas de negocio. |
| `app/logic/dates.py` | Fechas locales y semanas (funciones puras). |
| `app/logic/validation.py` | Validaciones de series y fechas (funciones puras). |
| `app/logic/templates.py` | Resolver qué versión de plantilla rige en una fecha (funciones puras). |
| `app/logic/analysis.py` | Constancia, mejor serie y volumen (funciones puras; fase 2). |
| `app/templates/` | Páginas HTML. |
| `app/static/` | CSS y el JavaScript mínimo. |
| `scripts/seed_demo_data.py` | Carga datos de prueba conocidos. |
| `tests/` | Pruebas de lógica y de rutas. |
| `data/` | Archivo de la base de datos (fuera de Git). |

## Modelo de datos
- **exercise**: `id`, `name`, `name_key` (nombre normalizado en minúsculas, único).
- **template_version**: `id`, `weekday` (0 = lunes ... 6 = domingo), `valid_from` (fecha), `is_rest`. Único por `(weekday, valid_from)`.
- **template_item**: `id`, `template_version_id`, `exercise_id`, `position`, `planned_sets`, `planned_reps`.
- **session**: `id`, `date`, `template_weekday`, `note`, `created_at`. Único por `(date, template_weekday)`.
- **session_set**: `id`, `session_id`, `exercise_id`, `set_number`, `weight_kg`, `reps`. Único por `(session_id, exercise_id, set_number)`.
- Restricciones: peso ≥ 0, repeticiones > 0, números de serie y valores previstos > 0, `weekday` entre 0 y 6.
- `exercise_id` se referencia con `ON DELETE RESTRICT`: la propia base impide borrar un ejercicio en uso (RF-4).
- Las fechas se guardan como texto `AAAA-MM-DD` en hora local.
- Cubre: RF-1 a RF-6, RF-13, RF-16.

## Funciones puras (reciben "hoy" o los datos como parámetro)
- `week_start(day)`: lunes de la semana de una fecha.
- `validate_set(weight, reps)`: aplica RF-14 y RF-15.
- `validate_session_date(day, today)`: aplica RF-17.
- `resolve_version(versions, weekday, day)`: versión vigente de un día de la semana en una fecha.
- `weekly_consistency(monday, versions, sessions, today)`: porcentaje de constancia.
- `best_set_per_week(sets)` y `weekly_volume(sets)`: análisis de progreso y volumen.

## Algoritmos

**Versión vigente (RF-6)**
```
resolve_version(versions, weekday, day):
  candidates = versions del weekday con valid_from <= day
  si no hay candidates: devolver None   (día sin configurar)
  devolver la de mayor valid_from
```

**Referencia de una serie (RF-11)**
```
reference(date D, template_weekday T, exercise E, set_number N):
  previous = última sesión con template_weekday = T y date < D
             (ante igualdad de fecha, la más reciente por created_at)
  si no hay previous: devolver "sin registro previo"
  set = serie de previous con ejercicio E y número N
  si no hay set: devolver "sin registro previo"
  devolver (peso, repeticiones) del set
```

**Constancia semanal (RF-23, RF-24)**
```
weekly_consistency(monday, versions, sessions, today):
  planned = 0
  para cada día de monday a monday + 6:
    v = resolve_version(versions, weekday del día, día)
    si v existe y no es descanso: planned += 1
  si planned = 0: devolver "sin plantillas planificadas"
  done = cantidad de template_weekday distintos en las sesiones de esa semana
  porcentaje = min(100, done / planned * 100)
  in_progress = (today <= monday + 6)
  devolver (porcentaje, in_progress)
```

## Interfaz
Una sola columna, pensada primero para celular (360 px), formularios que el servidor procesa y devuelve como página.
- **Inicio:** plantilla de hoy y botón para registrar.
- **Ejercicios:** lista, crear, renombrar, eliminar (RF-1 a RF-4).
- **Plantillas:** los 7 días de la semana y edición de cada uno (RF-5, RF-6).
- **Registrar sesión:** selector de plantilla y fecha, una fila por serie con peso y repeticiones, referencia de la semana anterior en letra chica, botón "agregar serie" y nota final (RF-7 a RF-17).
- **Historial:** lista por fecha con filtro por ejercicio y acceso a corregir (RF-18 a RF-20).
- **Análisis (fase 2):** progreso por ejercicio, volumen semanal y constancia (RF-21 a RF-26).

## Decisiones técnicas
1. **`sqlite3` sin ORM.** Escribir SQL propio sirve para aprenderlo y practicar funciones de ventana. *Alternativa descartada:* SQLAlchemy (más abstracción, menos práctica de SQL y una dependencia más).
2. **Versiones de plantilla con fecha de vigencia.** Son necesarias para RF-6 y para calcular la constancia sobre la planificación de cada semana. *Alternativa descartada:* guardar una copia completa de la plantilla en cada sesión (más simple, pero no permite reconstruir qué estaba planificado cada semana).
3. **Páginas servidas por el backend (Jinja2).** Mantiene todo en Python, que es lo que ya manejás. *Alternativa descartada:* aplicación de JavaScript separada (más herramientas y más código fuera de tu zona de trabajo).
4. **Gráficos sin conexión (fase 2).** La app debe funcionar sin internet (RNF-1), así que la librería de gráficos se incluye como archivo local, o los gráficos se generan en el servidor. *Alternativa descartada:* cargarla desde una CDN. Se decide al llegar a la fase 2.
5. **Agregar serie con un poco de JavaScript propio.** *Alternativa descartada:* HTMX (una dependencia más para una sola función).
6. **Pandas no entra en la fase 1.** Se evalúa en la fase 2 si los análisis lo justifican; los cálculos de agregación se pueden resolver con SQL.
7. **Tope del 100 % en la constancia.** Defensa para casos raros donde las realizadas superen a las planificadas. Es una precisión que agrega el plan: no contradice la spec.

## Estrategia de pruebas (`pytest`)
- **Lógica pura:** pruebas unitarias para fechas, validaciones, versión vigente y análisis, con casos límite (semana sin plantillas, cambio de plantilla a mitad de semana, domingo registrado el lunes, igualdad de fecha).
- **Rutas y base de datos:** pruebas con el cliente de pruebas de FastAPI y una base temporal, para crear, renombrar y eliminar ejercicios, guardar y corregir sesiones, y rechazar duplicados y fechas futuras.
- **Datos de prueba conocidos:** el script de datos de prueba genera resultados que se pueden verificar a mano.
- **Interfaz:** verificación manual en vista móvil de 360 px (RNF-2) y del flujo completo.
- Regla de la constitución: no se avanza con pruebas en rojo.

## Cobertura de requisitos
| Parte del plan | RF / RNF que cubre |
|---|---|
| Tablas, restricciones y claves foráneas | RF-1 a RF-6, RF-13, RF-16, RNF-3 |
| `validation.py` | RF-14, RF-15, RF-17 |
| `templates.py` y versiones | RF-5, RF-6 |
| Referencia de la semana anterior | RF-9, RF-11, RF-12 |
| Registro, historial y corrección | RF-7, RF-8, RF-10, RF-13, RF-18 a RF-20 |
| `analysis.py` | RF-21 a RF-26 |
| Diseño móvil, ejecución local, README | RNF-1, RNF-2, RNF-4 a RNF-7 |

## Riesgos y limitaciones
- Si se modifica una plantilla el mismo día en que ya se registró una sesión con ella, la pantalla de corrección de esa sesión mostrará las series previstas de la versión nueva. Los datos reales de la sesión no cambian. Limitación aceptada para la v1.
- Los análisis dependen de que se carguen datos reales durante varias semanas.
- La v1 se carga después de entrenar, desde la misma red local.
- La versión de Python instalada está por confirmar con `python --version`.