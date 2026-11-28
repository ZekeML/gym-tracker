# Tareas — Spec 001 Gym Tracker (fase 1)

Estado: aprobada

## Regla de pruebas
- **T1** prepara el entorno y deja funcionando el arnés de pruebas con una prueba mínima.
- **Desde T2**, cada comportamiento nuevo empieza con una prueba que falla (rojo). Después se escribe el código, se corre `pytest` hasta que pase (verde) y recién entonces se marca la tarea y se para.
- No se avanza a la tarea siguiente con pruebas en rojo.

## Tareas

- [x] **T1. Entorno y arnés del proyecto.** RNF-1, RNF-7
  - Se crea el entorno virtual (`.venv`), `requirements.txt`, la estructura de carpetas del plan, `.gitignore` (con `.venv/` y `data/`), `AGENTS.md` y `MEMORY.md`. Se agrega una prueba mínima: la aplicación de FastAPI se puede crear y su página inicial responde. Si las dependencias no se pueden instalar con Python 3.15, se usa Python 3.13 o 3.14 en el entorno virtual y la decisión se registra en `MEMORY.md`.
  - Hecho cuando: `pytest` encuentra y pasa al menos una prueba, la página mínima se ve en `localhost` desde el navegador y `AGENTS.md` referencia la constitución y la spec.
  - Entendé: qué es un entorno virtual y por qué `data/` no se sube a Git.

- [x] **T2. Base de datos y sus restricciones.** RF-1, RF-2, RF-4, RF-5b, RF-13, RF-16, RNF-3
  - Se escribe `schema.sql` y `db.py` con las 5 tablas, `PRAGMA user_version` y las claves foráneas activadas en cada conexión. Las pruebas cubren las restricciones del modelo:
    - Valores: peso mayor o igual a 0, repeticiones mayores a 0, números de serie y valores previstos mayores a 0, día de la semana entre 0 y 6.
    - Unicidad: nombre de ejercicio normalizado, versión por día de la semana y fecha de vigencia, ejercicio una sola vez por versión de plantilla, sesión por plantilla y fecha, serie por sesión, ejercicio y número.
    - Integridad: claves foráneas activas y no se puede eliminar un ejercicio usado en una plantilla ni en una sesión.
    - Persistencia: los datos siguen al reabrir el archivo.
  - Las reglas de aplicación (validaciones con mensajes, qué versión rige, formularios) se prueban en las tareas donde se implementan.
  - Hecho cuando: todas las pruebas de restricciones pasan.
  - Entendé: qué restricciones impone la base y cuáles quedan en el código.

- [ ] **T3. Lógica pura de la fase 1.** RF-5b, RF-6, RF-14, RF-15, RF-17, RNF-4
  - Se implementan `week_start`, `validate_set`, `validate_session_date`, `validate_template_items` y `resolve_version`, sin tocar la base ni la web. Las pruebas usan datos de ejemplo.
  - Hecho cuando: las pruebas unitarias pasan con los casos del plan: fecha futura, serie con un solo campo, serie vacía omitida, ejercicio repetido en una plantilla, versión vigente en una fecha, fecha anterior a la primera versión y dos versiones del mismo día.
  - Entendé: qué hace `resolve_version` y por qué recibe los datos como parámetro.

- [ ] **T4. Ejercicios.** RF-1, RF-2, RF-3, RF-4
  - Pantalla para crear, renombrar y eliminar ejercicios.
  - Hecho cuando: las pruebas de rutas pasan (duplicado rechazado sin distinguir mayúsculas, renombrar cambia el nombre en todos lados, eliminación bloqueada con mensaje si está en uso) y se verifica a mano en el navegador.

- [ ] **T5. Plantillas por día con versiones.** RF-5, RF-5b, RF-6
  - Pantalla con los 7 días, edición de cada uno y creación de versión nueva con fecha de vigencia.
  - Hecho cuando: las pruebas del comportamiento real pasan: el cambio rige desde hoy, modificar dos veces el mismo día reemplaza la versión de ese día, las sesiones anteriores no cambian y se rechaza un ejercicio repetido con mensaje.
  - Entendé: qué pasa con la rutina anterior cuando editás una plantilla.

- [ ] **T6. Registro de sesión.** RF-7, RF-8, RF-9, RF-10, RF-13, RF-14, RF-15, RF-16, RF-17
  - Pantalla para elegir plantilla y fecha, cargar series (con serie extra) y una nota final, y guardar.
  - Hecho cuando: las pruebas de rutas pasan y el flujo completo se verifica a mano: se cargan series, se omite una vacía, se rechaza una fecha futura y un duplicado.

- [ ] **T7. Referencia de la semana anterior.** RF-11, RF-12
  - Cada serie muestra lo que se hizo en la última sesión de esa plantilla anterior a la fecha, sin copiar valores en los campos.
  - Hecho cuando: las pruebas confirman la referencia correcta, el mensaje "sin registro previo" y que los campos quedan en blanco.
  - Entendé: cómo se busca la referencia (plantilla, ejercicio y número de serie).

- [ ] **T8. Historial.** RF-18, RF-19
  - Lista de sesiones ordenada por fecha de entrenamiento y filtro por ejercicio.
  - Hecho cuando: las pruebas confirman el orden (incluida la igualdad de fecha) y el filtro.

- [ ] **T9. Corrección de sesiones.** RF-20, RF-11
  - Pantalla para corregir una sesión pasada, con las mismas validaciones y la referencia anterior a su fecha.
  - Hecho cuando: las pruebas confirman que corregir respeta RF-14 a RF-17 y que no cambia otras sesiones.

- [ ] **T10. Cierre de la fase 1: interfaz móvil, datos de prueba y README.** RNF-2, RNF-5, RNF-6, RNF-7
  - Se ejecuta después de que todas las pantallas funcionales estén hechas. Ajusta y verifica en conjunto la interfaz para 360 px, agrega el script de datos de prueba y escribe el README.
  - Hecho cuando: la interfaz se ve sin desplazamiento horizontal en vista móvil de 360 px, la consulta del historial responde en menos de 1 segundo con un año de datos de prueba y alguien puede instalar y ejecutar el proyecto siguiendo solo el README.
  - Entendé: las limitaciones que quedan documentadas.