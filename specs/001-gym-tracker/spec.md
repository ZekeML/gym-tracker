# Spec 001 — Gym Tracker

Estado: aprobada

## Contexto y objetivo
Quien entrena con pesas suele anotar rutinas y marcas en notas sueltas, sin estructura ni forma de ver su evolución. Esta aplicación permite definir una rutina semanal reutilizable, registrar cada sesión serie por serie y consultar el historial. En una segunda fase muestra la evolución del propio usuario respecto de sus semanas anteriores, para ajustar la sobrecarga progresiva.

## Usuarios
Una persona que entrena y quiere llevar su propio registro. La aplicación es local y de un solo usuario: cada persona que descargue el proyecto parte de un registro vacío.

## Historias de usuario
- HU-1. Como persona que entrena, quiero definir una plantilla para cada día de la semana para no repetir la rutina en cada sesión.
- HU-2. Como persona que entrena, quiero registrar peso y repeticiones de cada serie para conservar el detalle de mi entrenamiento.
- HU-3. Como persona que entrena, quiero ver lo que hice la última vez en cada serie mientras registro, para saber si supero, igualo o bajo mi marca.
- HU-4. Como persona que entrena, quiero consultar y corregir mi historial para mantenerlo fiel a lo que hice.
- HU-5. Como persona que entrena, quiero ver mi progreso, mi volumen y mi constancia por semana para evaluar si mi plan funciona.

## Definiciones
- **Ejercicio:** movimiento con nombre propio, creado una vez por el usuario y reutilizable (por ejemplo, "Press de banca"). Conserva su identidad aunque se renombre.
- **Plantilla:** rutina planificada para un día de la semana. Es de descanso o de entrenamiento; en este último caso contiene ejercicios con series y repeticiones previstas.
- **Versión de plantilla:** estado de una plantilla desde la fecha en que se modificó hasta la siguiente modificación.
- **Sesión:** un entrenamiento registrado, con fecha real y la plantilla utilizada.
- **Serie:** un conjunto de repeticiones de un ejercicio, con su peso (en kg) y repeticiones reales.
- **Semana:** de lunes a domingo, en hora local. Una sesión pertenece a la semana de su fecha real.
- **Volumen:** suma de peso × repeticiones de todas las series.
- **Constancia semanal:** cantidad de plantillas de entrenamiento distintas realizadas en la semana, dividida por la cantidad de plantillas de entrenamiento planificadas para esa semana, expresada en porcentaje. La planificación de cada día es la versión de plantilla vigente en esa fecha.

## Requisitos funcionales

### Ejercicios y plantillas
- RF-1: CUANDO el usuario crea un ejercicio con un nombre, EL SISTEMA lo guarda en su lista de ejercicios y lo deja disponible para las plantillas.
- RF-2: SI el nombre de un ejercicio ya existe (sin distinguir mayúsculas), ENTONCES EL SISTEMA rechaza la creación o el cambio de nombre e informa el motivo.
- RF-3: CUANDO el usuario renombra un ejercicio, EL SISTEMA muestra el nuevo nombre en todas las plantillas y sesiones donde aparece.
- RF-4: CUANDO el usuario elimina un ejercicio que no está en ninguna plantilla ni en ninguna sesión, EL SISTEMA lo elimina; SI está en alguna plantilla o sesión, ENTONCES EL SISTEMA rechaza la eliminación e informa el motivo.
- RF-5: CUANDO el usuario configura un día de la semana, EL SISTEMA permite marcarlo como descanso o asignarle ejercicios, cada uno con cantidad de series y repeticiones previstas (números enteros mayores que 0).
- RF-5b: SI el usuario asigna dos veces el mismo ejercicio a una plantilla, ENTONCES EL SISTEMA rechaza el cambio e informa el motivo; para más trabajo del mismo ejercicio se aumentan sus series previstas.
- RF-6: CUANDO el usuario modifica una plantilla, EL SISTEMA aplica el cambio desde la fecha de la modificación, conserva las versiones anteriores con su fecha de vigencia y deja intactas las sesiones ya registradas.

### Registro de sesiones
- RF-7: CUANDO el usuario inicia un registro, EL SISTEMA propone la plantilla del día de la semana actual (hora local) y permite elegir cualquier otra plantilla de entrenamiento.
- RF-8: CUANDO el usuario inicia un registro, EL SISTEMA propone como fecha el día de hoy (hora local) y permite cambiarla.
- RF-9: MIENTRAS hay un registro en curso, EL SISTEMA muestra, para cada ejercicio, una fila por cada serie prevista con los campos de peso y repeticiones en blanco.
- RF-10: CUANDO el usuario agrega una serie extra a un ejercicio durante el registro, EL SISTEMA la trata como cualquier otra serie, con las mismas validaciones y sin referencia previa.
- RF-11: CUANDO el usuario registra o corrige una sesión, EL SISTEMA muestra junto a cada serie el peso y las repeticiones de la misma serie (mismo ejercicio y mismo número de serie) en la última sesión de esa plantilla con fecha anterior a la de la sesión en curso; SI no existe, ENTONCES EL SISTEMA indica "sin registro previo".
- RF-12: EL SISTEMA no copia valores de sesiones anteriores en los campos de un registro: solo los muestra como referencia.
- RF-13: CUANDO el usuario guarda la sesión, EL SISTEMA almacena la fecha, la plantilla, el peso y las repeticiones de cada serie completada y una nota de texto opcional para toda la sesión.
- RF-14: SI una serie tiene solo uno de los dos valores, o el peso es menor que 0, o las repeticiones no son un entero mayor que 0, ENTONCES EL SISTEMA rechaza el guardado y señala el campo. El peso admite decimales y el valor 0.
- RF-15: SI una serie tiene ambos campos vacíos, ENTONCES EL SISTEMA la omite al guardar.
- RF-16: SI ya existe otra sesión de la misma plantilla en la misma fecha, ENTONCES EL SISTEMA rechaza el guardado e informa el motivo.
- RF-17: SI la fecha es posterior a hoy (hora local), ENTONCES EL SISTEMA rechaza el guardado.

### Historial
- RF-18: CUANDO el usuario consulta el historial, EL SISTEMA lista las sesiones ordenadas por fecha de entrenamiento, de la más reciente a la más antigua (ante igualdad de fecha, por orden de creación, la más reciente primero), con fecha, plantilla, series y nota.
- RF-19: CUANDO el usuario filtra el historial por ejercicio, EL SISTEMA muestra solo las series de ese ejercicio con su fecha.
- RF-20: CUANDO el usuario corrige una sesión ya registrada, EL SISTEMA aplica las mismas validaciones que al crearla (RF-14 a RF-17).

### Análisis (fase 2)
- RF-21: CUANDO el usuario selecciona un ejercicio, EL SISTEMA muestra, por semana, la mejor serie (mayor peso; ante igualdad de peso, mayor cantidad de repeticiones).
- RF-22: CUANDO el usuario consulta el volumen, EL SISTEMA muestra el volumen semanal total y por ejercicio.
- RF-23: CUANDO el usuario consulta la constancia, EL SISTEMA muestra el porcentaje por semana; la semana en curso se calcula contra todas las plantillas de entrenamiento de esa semana y se marca como incompleta.
- RF-24: SI una semana no tiene plantillas de entrenamiento planificadas, ENTONCES EL SISTEMA muestra "sin plantillas planificadas" en lugar de un porcentaje.
- RF-25: SI un ejercicio tiene datos en menos de 2 semanas, ENTONCES EL SISTEMA indica que no hay datos suficientes para mostrar su evolución.
- RF-26: EL SISTEMA presenta los análisis como descripción de los datos del propio usuario y no afirma relaciones de causa y efecto.

## Requisitos no funcionales
- RNF-1: La aplicación funciona de forma local, sin conexión a internet, sin cuentas y sin costos.
- RNF-2: La interfaz está pensada primero para celular: se usa en una pantalla de 360 px de ancho sin desplazamiento horizontal.
- RNF-3: Los datos persisten al cerrar la aplicación.
- RNF-4: Las fechas se interpretan siempre en hora local.
- RNF-5: Las pantallas de registro e historial responden en menos de 1 segundo con un año de datos.
- RNF-6: Los textos de la interfaz y la documentación están en español; el peso se expresa solo en kilogramos.
- RNF-7: El proyecto se instala y ejecuta desde cero siguiendo únicamente las instrucciones del README.

## Casos límite
- Entrenar un día distinto del planificado: se elige otra plantilla; la sesión guarda la fecha real y la constancia lo cuenta como realizado en la semana de esa fecha.
- Sesión de un domingo registrada el lunes siguiente con la fecha del domingo: pertenece a la semana del domingo.
- Saltear un día: no se registra nada y la constancia lo refleja.
- Dato mal cargado: se corrige desde el historial (RF-20).
- Cambio en una plantilla después de registrar sesiones o en mitad de una semana: las sesiones previas no cambian y cada día de la semana usa la versión vigente en su fecha (RF-6).
- Semana sin plantillas de entrenamiento: sin porcentaje de constancia (RF-24).
- Eliminar un ejercicio en uso: bloqueado con mensaje (RF-4).
- Corregir una sesión antigua: la referencia es la última sesión de esa plantilla anterior a su fecha (RF-11).
- Primer uso sin datos: las pantallas de historial y análisis lo indican en lugar de mostrarse vacías.
- Mismo ejercicio dos veces en una plantilla: rechazado (RF-5b).

## Fuera de alcance
- RIR, escala de fatiga y notas antes o después del entrenamiento.
- Comparación entre ejercicios para decidir cuáles funcionan mejor.
- Publicación en internet, uso desde el gimnasio en tiempo real y múltiples usuarios.
- Videos, rankings y comparación con otras personas.
- Importación desde Google Keep.
- Registrar que un día planificado se descansó o se pospuso (distinto de configurar un día de descanso en la plantilla).
- Archivar ejercicios y unidades distintas del kilogramo.

## Criterios de finalización
- Fase 1 (RF-1 a RF-20): cada RF con prueba automática en verde para la lógica y demostración manual del flujo completo (crear ejercicios, armar plantillas, registrar, consultar y corregir el historial).
- Fase 2 (RF-21 a RF-26): análisis verificados con datos de prueba conocidos.
- README con instalación, uso y limitaciones.
- Datos de prueba incluidos en el repositorio.

## Dudas abiertas
- Ninguna.