# Plan 001 — Gym Tracker

Estado: aprobada
Spec: specs/001-gym-tracker/spec.md (aprobada)

## Fases
- **Fase 1:** ejercicios, plantillas, registro de sesiones, referencia, historial y correcciones (RF-1 a RF-20).
- **Fase 2:** análisis de progreso, volumen y constancia (RF-21 a RF-26). Se construye cuando la fase 1 esté terminada y haya datos cargados.

## Stack
- Python 3.11 o superior, FastAPI con Uvicorn, plantillas Jinja2 (el servidor genera el HTML), `sqlite3` de la biblioteca estándar y `pytest`.
- Dependencias externas: `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `httpx` (solo para pruebas) y `pytest`, listadas en `requirements.txt`.
- Se trabaja dentro de un entorno virtual (`.venv`, fuera de Git).
- CSS propio y JavaScript mínimo (solo para agregar una fila de serie extra).
- Cubre: RNF-1, RNF-2, RNF-7.

## Archivos y responsabilidades
| Archivo | Responsabilidad | Fase |
|---|---|---|
| `app/main.py` | Crea la aplicación y define las rutas. | 1 y 2 |
| `app/db.py` | Abre la conexión, activa claves foráneas, crea las tablas y aplica las migraciones. | 1 |
| `app/schema.sql` | Definición de tablas y restricciones. | 1 |
| `app/repository.py` | Todas las consultas SQL. No contiene reglas de negocio. | 1 y 2 |
| `app/logic/dates.py` | Fechas locales y semanas (funciones puras). | 1 |
| `app/logic/validation.py` | Validaciones de series, fechas y plantillas (funciones puras). | 1 |
| `app/logic/templates.py` | Resolver qué versión de plantilla rige en una fecha (funciones puras). | 1 |
| `app/logic/analysis.py` | Constancia, mejor serie y volumen (funciones puras). | 2 |
| `app/templates/` | Páginas HTML. | 1 y 2 |
| `app/static/` | CSS y JavaScript mínimo. | 1 y 2 |
| `scripts/seed_demo_data.py` | Carga datos de prueba conocidos. | 1 y 2 |
| `tests/` | Pruebas de lógica y de rutas. | 1 y 2 |
| `data/` | Archivo de la base de datos (fuera de Git). | 1 |

## Modelo de datos
- **exercise**: `id`, `name`, `name_key` (nombre normalizado en minúsculas, único).
- **template_version**: `id`, `weekday` (0 = lunes ... 6 = domingo), `valid_from` (fecha), `is_rest`. Único por `(weekday, valid_from)`.
- **template_item**: `id`, `template_version_id`, `exercise_id`, `position`, `planned_sets`, `planned_reps`. Único por `(template_version_id, exercise_id)`: un ejercicio aparece una sola vez por plantilla.
- **session**: `id`, `date`, `template_weekday`, `note`, `created_at`. Único por `(date, template_weekday)`.
- **session_set**: `id`, `session_id`, `exercise_id`, `set_number`, `weight_kg`, `reps`. Único por `(session_id, exercise_id, set_number)`.
- Restricciones: peso ≥ 0, repeticiones > 0, números de serie y valores previstos > 0, `weekday` entre 0 y 6.
- `exercise_id` se referencia con `ON DELETE RESTRICT`: la propia base impide borrar un ejercicio en uso (RF-4).
- Las fechas se guardan como texto `AAAA-MM-DD` en hora local.
- Cubre: RF-1 a RF-6, RF-13, RF-16.

## Reglas de las versiones de plantilla (RF-5, RF-5b, RF-6)
- Al guardar los cambios de la plantilla de un día de la semana se crea una versión nueva con `valid_from` igual a la fecha de hoy (hora local). La versión nueva contiene la lista completa resultante de ejercicios (es una copia editada de la anterior, no un parche).
- Si ya existe una versión de ese día con `valid_from` igual a hoy, se reemplaza su contenido y no se crea otra.
- Una versión rige desde su `valid_from` hasta el día anterior al `valid_from` de la siguiente versión del mismo día de la semana.
- Antes de la primera versión, el día se considera sin configurar (ni planificado ni de descanso) para la constancia.
- Al registrar o corregir una sesión se muestran las series previstas de la versión vigente en la fecha de esa sesión; si la fecha es anterior a la primera versión, se usa la primera versión de ese día.
- Se rechaza una plantilla que repita un ejercicio (RF-5b).

## Funciones puras (reciben "hoy" o los datos como parámetro)
- Fase 1: `week_start(day)`, `validate_set(weight, reps)`, `validate_session_date(day, today)`, `validate_template_items(items)` y `resolve_version(versions, weekday, day)`.
- Fase 2: `weekly_consistency(monday, versions, sessions, today)`, `best_set_per_week(sets)` y `weekly_volume(sets)`.

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
  si no hay previous: devolver "sin registro previo"
  set = serie de previous con ejercicio E y número N
  si no hay set: devolver "sin registro previo"
  devolver (peso, repeticiones) del set
```
- Al corregir una sesión antigua, D es la fecha de esa sesión: la referencia se busca solo entre sesiones anteriores a esa fecha.
- No hace falta desempate: por la restricción única `(date, template_weekday)`, dos sesiones de la misma plantilla nunca comparten fecha.

**Constancia semanal (RF-23, RF-24; fase 2)**
```
weekly_consistency(monday, versions, sessions, today):
  planned = 0
  para cada día de monday a monday + 6:
    v = resolve_version(versions, weekday del día, día)
    si v existe y no es descanso: planned += 1
  si planned = 0: devolver "sin plantillas planificadas"
  done = cantidad de template_weekday distintos en las sesiones de esa semana
  porcentaje = min(100, done / planned * 100), redondeado al entero más cercano
  in_progress = (today <= monday + 6)
  devolver (porcentaje, in_progress)
```
- Una sesión cuenta para la semana de su fecha real, y para la plantilla que se usó, no para el día en que se hizo.
- Ejemplo (semana en curso): hay plantillas de entrenamiento planificadas para lunes, miércoles y viernes (3). Hoy es jueves. El lunes se entrenó la plantilla del lunes y el jueves la del miércoles. Realizadas: 2 (lunes y miércoles); constancia: 2 / 3 = 67 %, marcada como "en curso" porque el viernes todavía no terminó la semana.
- Entrenar la misma plantilla dos veces en la semana cuenta una sola vez.

## Interfaz
Una sola columna, pensada primero para celular (360 px), formularios que el servidor procesa y devuelve como página.
- **Inicio:** plantilla de hoy y botón para registrar. (Fase 1)
- **Ejercicios:** lista, crear, renombrar, eliminar (RF-1 a RF-4). (Fase 1)
- **Plantillas:** los 7 días de la semana y edición de cada uno (RF-5, RF-5b, RF-6). (Fase 1)
- **Registrar sesión:** selector de plantilla y fecha, una fila por serie con peso y repeticiones, referencia de la semana anterior en letra chica, botón "agregar serie" y nota final (RF-7 a RF-17). (Fase 1)
- **Historial:** lista por fecha con filtro por ejercicio y acceso a corregir (RF-18 a RF-20). (Fase 1)
- **Análisis:** progreso por ejercicio, volumen semanal y constancia (RF-21 a RF-26). (Fase 2)

## Decisiones técnicas
1. **`sqlite3` sin ORM.** Escribir SQL propio sirve para aprenderlo y practicar funciones de ventana. *Alternativa descartada:* SQLAlchemy (más abstracción, menos práctica de SQL y una dependencia más).
2. **Versiones de plantilla con fecha de vigencia.** Son necesarias para RF-6 y para calcular la constancia sobre la planificación de cada semana. *Alternativa descartada:* guardar una copia completa de la plantilla en cada sesión (más simple, pero no permite reconstruir qué estaba planificado cada semana).
3. **Páginas servidas por el backend (Jinja2).** Mantiene todo en Python. *Alternativa descartada:* aplicación de JavaScript separada (más herramientas y más código fuera de la zona de trabajo).
4. **Gráficos sin conexión (fase 2).** La app debe funcionar sin internet (RNF-1), así que la librería de gráficos se incluye como archivo local, o los gráficos se generan en el servidor. *Alternativa descartada:* cargarla desde una CDN. Se decide al llegar a la fase 2.
5. **Agregar serie con JavaScript propio.** *Alternativa descartada:* HTMX (una dependencia más para una sola función).
6. **Pandas no entra en la fase 1.** Se evalúa en la fase 2 si los análisis lo justifican; los cálculos de agregación se pueden resolver con SQL.
7. **Tope del 100 % en la constancia.** Defensa para casos raros. Es una precisión que agrega el plan y no contradice la spec.
8. **Un ejercicio aparece una sola vez por plantilla (RF-5b).** Más trabajo del mismo ejercicio se expresa con más series, cada una con su propio peso. *Alternativa descartada:* permitir apariciones repetidas con una posición (complica el modelo y la referencia por número de serie).
9. **Política de cambios en la base.** El esquema lleva un número de versión (`PRAGMA user_version`). Si una versión futura cambia las tablas, la actualización se hace con un paso numerado que conserva los datos existentes y hace una copia del archivo de la base antes de modificarlo. *Alternativa descartada:* recrear las tablas desde cero (perdería sesiones y viola el principio 5 de la constitución).

## Estrategia de pruebas (`pytest`)
**Fase 1**
- Lógica pura: fechas, validaciones, validación de plantillas y versión vigente, con casos límite (cambio de plantilla el mismo día, fecha anterior a la primera versión, igualdad de fecha entre plantillas distintas).
- Rutas y base de datos: cliente de pruebas de FastAPI con una base temporal; crear, renombrar y eliminar ejercicios, guardar y corregir sesiones, rechazar duplicados, ejercicios repetidos en una plantilla y fechas futuras.
- Interfaz: verificación manual en vista móvil de 360 px (RNF-2) y del flujo completo.

**Fase 2**
- Pruebas de constancia, mejor serie y volumen con datos conocidos del script de datos de prueba (semana sin plantillas, semana en curso, domingo registrado el lunes).
- Regla de la constitución: no se avanza con pruebas en rojo.

## Cobertura de requisitos
| Parte del plan | RF / RNF que cubre |
|---|---|
| Tablas, restricciones y claves foráneas | RF-1 a RF-6, RF-13, RF-16, RNF-3 |
| `validation.py` | RF-5b, RF-14, RF-15, RF-17 |
| `templates.py` y versiones | RF-5, RF-6 |
| Referencia de la semana anterior | RF-9, RF-11, RF-12 |
| Registro, historial y corrección | RF-7, RF-8, RF-10, RF-13, RF-18 a RF-20 |
| `analysis.py` (fase 2) | RF-21 a RF-26 |
| Diseño móvil, ejecución local, README | RNF-1, RNF-2, RNF-4 a RNF-7 |

## Riesgos y limitaciones
- Si se modifica una plantilla el mismo día en que ya se registró una sesión con ella, la pantalla de corrección de esa sesión mostrará las series previstas de la versión nueva. Los datos reales de la sesión no cambian. Limitación aceptada para la v1.
- Los análisis dependen de que se carguen datos reales durante varias semanas.
- La v1 se carga después de entrenar, desde la misma red local.
- Python 3.15.0 es una versión muy reciente: algunas dependencias podrían no estar listas. Si la instalación falla, se usa Python 3.13 o 3.14 en un entorno virtual.
