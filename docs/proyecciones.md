# Proyecciones y Escalabilidad de QR_Access_PRO

Este documento detalla los 4 grandes hitos o propuestas de evolución para llevar el sistema QR_Access_PRO al siguiente nivel de seguridad, funcionalidad empresarial y automatización de procesos.

---

### 1. 🔄 QRs Dinámicos (Protección Anti-Spoofing y Capturas)
**El Problema:** Actualmente, los códigos QR son estáticos. Un empleado podría tomar una captura de pantalla de su QR y enviársela a un compañero para que registre su entrada fraudulentamente (conocido como *buddy punching*).
**La Solución:** 
- Desarrollar un "Portal del Empleado" (WebApp optimizada para móviles).
- En lugar de un QR fijo impreso, la app mostrará un QR que cambia cada 30 segundos usando el algoritmo TOTP (Time-Based One-Time Password), al igual que Google Authenticator.
- El servidor validará matemáticamente que el QR escaneado corresponda al segundo exacto en que fue generado, haciendo inútiles las fotos o capturas de pantalla viejas.

---

### 2. 📊 Módulo de RRHH y Exportación de Nóminas
**El Problema:** El sistema actual registra entradas y salidas brutas, pero los departamentos de Recursos Humanos necesitan cálculos de horas exactas para procesar pagos y amonestaciones.
**La Solución:**
- Crear un panel de reportería avanzada que procese los _logs_ en crudo y empareje automáticamente los eventos de "Entrada" con los de "Salida".
- Calcular automáticamente horas regulares trabajadas, horas extras acumuladas, ausencias, y minutos de atraso según el turno asignado a cada empleado.
- Agregar funcionalidad de exportación en un solo clic a formatos estándar empresariales (Excel, CSV) que sean directamente compatibles para importación en sistemas ERP o de planillas (como SAP, Workday, Meta4 o Buk).

---

### 3. 🚪 Control de Acceso Multi-Zona (RBAC Físico)
**El Problema:** Actualmente el sistema valida si la persona tiene acceso general al edificio. En instalaciones grandes, diferentes empleados tienen permisos para diferentes áreas.
**La Solución:**
- Expandir el modelo de base de datos para soportar "Zonas" o "Puertas" múltiples.
- Configurar múltiples instancias de escáneres físicos (`scanner_windows.py` o Linux en Raspberry Pi) mapeados a puertas específicas (Ej: Entrada, Laboratorio, Sala de Servidores).
- Implementar Control de Acceso Basado en Roles (RBAC). Por ejemplo: el QR de un empleado regular abrirá la puerta del comedor, pero será "Denegado" al intentar leerse en la puerta de bóveda de seguridad.

---

### 4. 👁️ Inteligencia Artificial Anti-Spoofing y Reconocimiento Facial
**El Problema:** Incluso con QRs dinámicos, un empleado podría entregarle físicamente su teléfono desbloqueado a otra persona.
**La Solución:**
- Integrar tecnología de Visión por Computadora (Computer Vision) directamente en el script del escáner en puerta.
- Durante el milisegundo en que se lee el código QR, la cámara también tomará una captura del rostro de la persona frente a la puerta.
- El sistema comparará mediante modelos de IA ligeros (ej. OpenCV o Dlib) la foto tomada en tiempo real con la fotografía de perfil almacenada en la base de datos del empleado.
- El acceso solo se marca como "PERMITIDO" si tanto el QR es válido como la identidad del rostro coincide (*Match biométrico*).

---

### 5. 🔒 Certificados de Seguridad Automáticos (HTTPS / SSL)
**El Problema:** El tráfico local o a través de internet expone contraseñas corporativas si no está encriptado bajo HTTPS.
**La Solución:**
- Integrar un proxy inverso (como Nginx o Traefik) dentro del entorno Docker.
- Configurar la emisión y renovación automática de certificados SSL gratuitos de *Let's Encrypt*.
- Asegurar que todas las comunicaciones cliente-servidor y escáner-servidor viajen bajo un túnel encriptado.

---

### 6. ⚡ Base de Datos en Caché Ultrarrápida (Redis)
**El Problema:** En entornos ultra-masivos (ej: validar entradas en un concierto o turno rotativo de fábrica de 5,000 personas al mismo tiempo), golpear el disco duro de la base de datos MySQL por cada lectura genera cuellos de botella.
**La Solución:**
- Instalar e integrar un servidor Redis.
- Configurar el sistema para que cuando un usuario inicie sesión o sea validado, su estado y permisos se guarden en la memoria RAM de Redis.
- Conseguir tiempos de lectura casi instantáneos (sub-milisegundo) e independencia parcial de caídas del motor relacional.
