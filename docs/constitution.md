# Constitución — Gym Tracker

Principios innegociables. Toda spec, plan y tarea debe cumplirlos.

1. **Simplicidad primero**: aplicación local de un solo usuario, sin cuentas, sin servicios externos y sin costos.
2. **La spec manda**: nada se implementa si no está en la spec activa. Si falta una decisión, se frena y se pregunta.
3. **Lógica separada de interfaz**: los cálculos (volumen, carga, tendencias) son funciones puras, sin acceso a la base de datos ni a la web.
4. **Tests como puerta**: la lógica se prueba con `pytest`. No se avanza con tests en rojo.
5. **Los datos del usuario son sagrados**: los cambios en la base de datos mantienen compatibilidad y nunca se pierde una sesión registrada.
6. **Entender lo que se integra**: todo código generado por IA se revisa, se puede explicar y las decisiones relevantes quedan registradas.