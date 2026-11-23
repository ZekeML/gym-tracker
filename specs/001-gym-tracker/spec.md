# Spec 001 — Gym Tracker

Estado: borrador

## Contexto y objetivo
Quien entrena con pesas suele anotar rutinas y marcas en notas sueltas, sin estructura ni forma de ver su evolución. Esta aplicación permite definir una rutina semanal reutilizable, registrar cada sesión serie por serie y consultar el historial. En una segunda fase muestra la evolución del propio usuario respecto de sus semanas anteriores, para ajustar la sobrecarga progresiva.

## Usuarios
Una persona que entrena y quiere llevar su propio registro. La aplicación es local y de un solo usuario: cada persona que descargue el proyecto parte de un registro vacío.

## Historias de usuario
- HU-1. Como persona que entrena, quiero definir una plantilla para cada día de la semana para no repetir la rutina en cada sesión.
- HU-2. Como persona que entrena, quiero registrar peso y repeticiones de cada serie para conservar el detalle de mi entrenamiento.
- HU-3. Como persona que entrena, quiero ver lo que hice la última vez en cada serie mientras registro, para saber si supero, igualo o bajo mi marca.
- HU-4. Como persona que entrena, quiero consultar mi historial para revisar mi evolución.
- HU-5. Como persona que entrena, quiero ver mi progreso, mi volumen y mi constancia por semana para evaluar si mi plan funciona.

## Definiciones
- **Ejercicio:** movimiento con nombre propio, creado una vez por el usuario y reutilizable (por ejemplo, "Press de banca").
- **Plantilla:** rutina planificada para un día de la semana. Es de descanso o contiene ejercicios con series y repeticiones previstas.
- **Sesión:** un entrenamiento registrado, con fecha real y la plantilla utilizada.
- **Serie:** un conjunto de repeticiones de un ejercicio, con su peso y repeticiones reales.
- **Semana:** de lunes a domingo, en hora local.
- **Volumen:** suma de peso × repeticiones de todas las series.
- **Constancia semanal:** cantidad de plantillas de entrenamiento distintas realizadas en la semana, dividida por las plantillas de entrenamiento planificadas, expresada en porcentaje.

## Requisitos funcionales

### Plantillas y ejercicios
- RF-1: CUANDO el usuario crea un ejercicio con un nombre, EL SISTEMA lo guarda en su lista de ejercicios y lo deja disponible para las plantillas.
- RF-2: SI el nombre del ejercicio ya existe (sin distinguir mayúsculas), ENTONCES EL SISTEMA rechaza la creación e informa el motivo.
- RF-3: CUANDO el usuario configura un día de la semana, EL SISTEMA permite marcarlo como descanso o asignarle ejercicios, cada uno con cantidad de series y repeticiones previstas (números enteros mayores que 0).
- RF-4: CUANDO el usuario modifica una plantilla, EL SISTEMA aplica el cambio solo a las sesiones futuras y deja intactas las sesiones ya registradas, incluidos los ejercicios y series previstas con los que se registraron.

### Registro de sesiones
- RF-5: CUANDO el usuario inicia un registro, EL SISTEMA propone la plantilla del día de la semana actual (hora local) y permite elegir cualquier otra plantilla de entrenamiento.
- RF-6: CUANDO el usuario inicia un registro, EL SISTEMA propone como fecha el día de hoy (hora local) y permite cambiarla.
- RF-7: MIENTRAS hay un registro en curso, EL SISTEMA muestra, para cada ejercicio, una fila por cada serie prevista con los campos de peso y repeticiones en blanco.
- RF-8: CUANDO existe una sesión anterior de la misma plantilla, EL SISTEMA muestra junto a cada serie el peso y las repeticiones de la misma serie en la última sesión de esa plantilla; SI no existe, ENTONCES EL SISTEMA indica "sin registro previo".
- RF-9: EL SISTEMA no copia valores de sesiones anteriores en los campos de un registro nuevo: solo los muestra como referencia.
- RF-10: CUANDO el usuario guarda la sesión, EL SISTEMA almacena la fecha, la plantilla, el peso y las repeticiones de cada serie completada y una nota de texto opcional para toda la sesión.
- RF-11: SI una serie tiene solo uno de los dos valores, o el peso es menor que 0, o las repeticiones no son un entero mayor que 0, ENTONCES EL SISTEMA rechaza el guardado y señala el campo. El peso admite decimales y el valor 0.
- RF-12: SI una serie tiene ambos campos vacíos, ENTONCES EL SISTEMA la omite al guardar.
- RF-13: SI ya existe una sesión de la misma plantilla en la misma fecha, ENTONCES EL SISTEMA rechaza el guardado e informa el motivo.
- RF-14: SI la fecha es posterior a hoy (hora local), ENTONCES EL SISTEMA rechaza el guardado.

### Historial
- RF-15: CUANDO el usuario consulta el historial, EL SISTEMA lista las sesiones de la más reciente a la más antigua, con fecha, plantilla, series y nota.
- RF-16: CUANDO el usuario filtra el historial por ejercicio, EL SISTEMA muestra solo las series de ese ejercicio con su fecha.
- RF-17: CUANDO el usuario corrige una sesión ya registrada, EL SISTEMA aplica las mismas validaciones que al crearla.

### Análisis (fase 2)
- RF-18: CUANDO el usuario selecciona un ejercicio, EL SISTEMA muestra, por semana, la mejor serie (mayor peso; ante igualdad de peso, mayor cantidad de repeticiones).
- RF-19: CUANDO el usuario consulta el volumen, EL SISTEMA muestra el volumen semanal total y por ejercicio.
- RF-20: CUANDO el usuario consulta la constancia, EL SISTEMA muestra el porcentaje por semana y marca la semana en curso como incompleta.
- RF-21: SI un ejercicio tiene datos en menos de 2 semanas, ENTONCES EL SISTEMA indica que no hay datos suficientes para mostrar su evolución.
- RF-22: EL SISTEMA presenta los análisis como descripción de los datos del propio usuario y no afirma relaciones de causa y efecto.

## Requisitos no funcionales
- RNF-1: La aplicación funciona de forma local, sin conexión a internet, sin cuentas y sin costos.
- RNF-2: La interfaz está pensada primero para celular: se usa en una pantalla de 360 px de ancho sin desplazamiento horizontal.
- RNF-3: Los datos persisten al cerrar la aplicación.
- RNF-4: Las fechas se interpretan siempre en hora local.
- RNF-5: Las pantallas de registro e historial responden en menos de 1 segundo con un año de datos.
- RNF-6: Los textos de la interfaz y la documentación están en español.
- RNF-7: El proyecto se instala y ejecuta desde cero siguiendo únicamente las instrucciones del README.

## Casos límite
- Entrenar un día distinto del planificado: se elige otra plantilla; la sesión guarda la fecha real.
- Saltear un día: no se registra nada y la constancia lo refleja.
- Dato mal cargado: se corrige desde el historial (RF-17).
- Semana en curso: la constancia se muestra como incompleta.
- Cambio en la plantilla después de registrar sesiones: no altera las sesiones previas (RF-4).
- Primer uso sin datos: las pantallas de historial y análisis lo indican en lugar de mostrarse vacías.
- Primera sesión de una plantilla: sin referencia previa (RF-8).

## Fuera de alcance
- RIR, escala de fatiga y notas antes o después del entrenamiento.
- Comparación entre ejercicios para decidir cuáles funcionan mejor.
- Publicación en internet, uso desde el gimnasio en tiempo real y múltiples usuarios.
- Videos, rankings y comparación con otras personas.
- Importación desde Google Keep.
- Marcar explícitamente un día como descanso o pospuesto.

## Criterios de finalización
- Fase 1 (RF-1 a RF-17): cada RF con prueba automática en verde para la lógica y demostración manual del flujo completo (crear ejercicios, armar plantillas, registrar, consultar historial).
- Fase 2 (RF-18 a RF-22): análisis verificados con datos de prueba conocidos.
- README con instalación, uso y limitaciones.
- Datos de prueba incluidos en el repositorio.

## Dudas abiertas
- [NECESITA ACLARACIÓN] ¿Se permite agregar series extra a un ejercicio durante el registro, además de las previstas?
- [NECESITA ACLARACIÓN] ¿Se puede renombrar o eliminar un ejercicio que ya tiene historial?
- [NECESITA ACLARACIÓN] ¿Se maneja una sola unidad de peso (kg) o también libras?
- [NECESITA ACLARACIÓN] ¿La semana de lunes a domingo es adecuada para la constancia?