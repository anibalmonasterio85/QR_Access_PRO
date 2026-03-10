# ABOUT QR_Access_PRO

## ¿Qué es QR_Access_PRO?
QR_Access_PRO es un sistema integral y profesional de control de acceso diseñado para gestionar la entrada y salida de personal mediante la validación de códigos QR seguros. Está compuesto por dos partes principales:
1. **Un Panel Web (Backend/Frontend):** Desarrollado en Python con Flask. Administra usuarios, genera y revoca códigos QR, registra el historial de accesos y proporciona métricas operativas.
2. **Un Sistema de Escaneo (Frontend de Hardware):** Un script adaptable (Raspberry Pi/Windows) diseñado para estar en la puerta de acceso, conectarse a una cámara o un escáner físico y validar los códigos QR contra el panel web en milisegundos.

## ¿Para qué sirve?
Sirve para reemplazar las tradicionales tarjetas magnéticas, llaves físicas o registros manuales de papel con una solución digital, segura y automatizada. 

Las principales funciones del sistema incluyen:
- **Autenticación rápida:** Lectura de códigos QR en la entrada de las instalaciones.
- **Gestión centralizada:** Creación, edición y suspensión de usuarios desde una interfaz web amigable.
- **Trazabilidad total:** Registro inmutable de la fecha, hora exacta y usuario que ingresa o sale de las instalaciones.
- **Seguridad perimetral:** Prevención de accesos no autorizados mediante escaneo en tiempo real de credenciales cifradas/únicas por usuario.

## ¿Por qué es la mejor opción en el entorno laboral?

### 1. Costo-Efectividad y Escalabilidad
A diferencia de los sistemas biométricos de huellas dactilares o tarjetas NFC que requieren hardware costoso para cada punto de acceso y consumibles (tarjetas físicas), QR_Access_PRO solo requiere un teléfono inteligente en el bolsillo del empleado y una cámara/escáner básica en la puerta. Agregar más empleados tiene un costo de cero.

### 2. Alta Disponibilidad y Tiempos de Respuesta
Concebido bajo una arquitectura robusta (Python + Flask + Waitress/Gunicorn + MariaDB), el sistema está optimizado para procesar múltiples peticiones por segundo sin latencia. Esto evita cuellos de botella ("filas o colas") en las entradas de fábricas, oficinas o eventos grandes durante horas pico.

### 3. Contactless (100% Sin Contacto)
Post-pandemia, los sistemas "contactless" han pasado de ser un lujo a un estándar de higiene laboral. Los empleados simplemente muestran su código desde la pantalla de sus teléfonos, reduciendo el riesgo de desgaste de hardware y transmisión de enfermedades.

### 4. Modularidad y Despliegue en Borde (Edge)
La división del proyecto en Web Panel y Scanner permite despliegues versátiles:
- El escáner puede correr en componentes pequeños y baratos como una *Raspberry Pi*.
- El Panel Web puede alojarse en un servidor local para máxima privacidad de datos, o en la nube (AWS/Azure) si se tienen múltiples sucursales a nivel mundial.

## Fines y Proyecciones Futuras

### Fines Actuales
El objetivo es otorgar control, orden y métricas exactas a las administraciones o departamentos de Recursos Humanos/Seguridad sobre el tráfico físico de la empresa, eliminando la suplantación de identidad o el préstamo del ingreso tradicional ("buddy punching").

### Proyecciones a Futuro
1. **Integración con Recursos Humanos:** Vincular las lecturas de los horarios de entrada automáticamente con sistemas de nómina (SAP, Workday, etc.) para cálculo de horas extras y puntualidad. 
2. **Códigos Dinámicos Temporales (TOTP):** Evolucionar de un QR estático a un QR dinámico que cambie cada 30 segundos usando un algoritmo tipo Google Authenticator en el teléfono de los empleados. Esto hará imposible que compartan capturas de pantalla de su QR.
3. **Control por Áreas e Inteligencia Artificial:** Expandir el sistema no solo para puertas principales, sino áreas restringidas (Ej: Nivel 1 = Oficinas, Nivel 5 = Servidores) e integrar IA de visión por computadora para además del QR, validar que la persona que escanea coincide con la foto en el registro (Anti-spoofing).
