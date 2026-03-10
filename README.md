# QR Access PRO

Sistema profesional de control de acceso mediante códigos QR, diseñado para entorno empresarial. Escanea identificaciones de forma rápida, mantiene un registro del tráfico, y se administra todo desde un panel web amigable.

## 🌟 Características Principales
- **Sistema 100% Sin Contacto (Contactless)**
- **Respuestas Rápidas:** Identificación validada en milisegundos.
- **Gestión Centralizada:** Creación, edición y suspensión de credenciales desde panel de administrador.
- **Seguimiento Seguro:** Base de datos robusta de registros (MariaDB).
- **Escáner Portátil:** El escáner puede implementarse en Linux (Raspberry Pi), o Windows, solo necesita una cámara.
- **Despliegue Profesional:** Servidor web productivo configurado (Waitress para Windows / Gunicorn/Waitress para Linux).

---

## 🛠 Instalación y Configuración

### 1. Requisitos Previos
- **Python 3.9+**
- **Base de Datos MariaDB / MySQL** configurada
- Cámara conectada (para el módulo escáner)

### 2. Configurar Entorno
El sistema usa un solo entorno virtual para manejar sus dependencias y una configuración gestionada por un archivo `.env`.

1. Clona el repositorio/mueve la carpeta a tu sistema:
   ```bash
   cd QR_Access_PRO
   ```
2. Crea e inicia un entorno virtual:
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate
   # En Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instala los requerimientos:
   ```bash
   pip install -r requirements.txt
   ```
4. Configuración de Base de Datos:
   - Crea un archivo `.env` en la raíz copiando `.env.example`. (Ver `web_panel/.env` o usar el script base).
   - Coloca las credenciales de tu servidor de base de datos.
   
---

## 🚀 Uso del Sistema

La arquitectura consta de **dos partes independientes que se conectan entre sí**. Debes ejecutar el Servidor para que exista el Panel Web, y luego ejecutar el Escáner para realizar las lecturas reales.

### Parte 1: Iniciar el Panel Web (Servidor Central)
El panel web es el cerebro del sistema que controla la base de datos de usuarios y registros.

- **En Windows:**
  Cuentas con scripts de ayuda en la raíz del proyecto para encender el sistema usando el entorno de producción Waitress:
  ```powershell
  .\start.ps1
  ```
  Accede a `http://localhost:5000` con tu navegador. Para apagar el servidor de forma segura, ejecuta en otra ventana:
  ```powershell
  .\stop.ps1
  ```


- **En Linux (Ej: Raspberry Pi Principal):**
  Puedes iniciar la aplicación usando los scripts de control dentro de `scripts/`:
  ```bash
  ./scripts/start.sh
  ```
  *(Puedes detenerlo con `./scripts/stop.sh` o ver el estado con `./scripts/status.sh`)*

### Parte 2: Iniciar el Escáner (Terminal en Puerta)
El escáner es el programa que activa la cámara y espera que una credencial QR sea presentada en pantalla.

- **Escáner USB/Webcam (Windows/General):**
  ```bash
  cd scanner
  python scanner_windows.py
  ```

---

## 🔧 Herramientas de Mantenimiento (`/tools`)
El código basura ha sido centralizado mantener el entorno limpio. 
Si requieres reparar la base de datos o manipular contraseñas a nivel bruto, dirígete a la carpeta `tools/`.
Ejemplos:
- ¿Olvidaste la clave de administrador? Ejecuta `python tools/auth/reset_admin.py`
- ¿Necesitas limpiar la tabla de usuarios de pruebas basura? Ejecuta `python tools/cleanup/limpiar_usuarios.py`
- ¿Quieres ver los respaldos de BDD antiguos? Revisa `tools/database/`.

---

## 📚 Documentación Adicional
- Para conocer el propósito completo y fundamentos teóricos, lee: [ABOUT.md](docs/ABOUT.md)
- Para instrucciones de operación: [MANUAL_DE_USUARIO.md](docs/MANUAL_DE_USUARIO.md)
- Para escalar el proyecto y desarrollo a futuro: [proyecciones.md](docs/proyecciones.md)
