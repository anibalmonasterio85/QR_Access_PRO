# 📖 MANUAL DEL USUARIO - QR ACCESS PRO

Bienvenido a **QR Access Pro**, el sistema profesional de control de acceso mediante códigos QR y panel web administrativo. Este manual está diseñado para explicarte paso a paso cómo iniciar y detener el sistema en tu computadora usando Windows (PowerShell).

---

## 1. ¿Qué es QR Access Pro?
Es una plataforma completa que permite gestionar permisos de entrada a instalaciones o eventos. Consiste en varios componentes, destacando su **Panel Web** (donde administras los usuarios, ves los logs y creas códigos QR) y el sistema de **Escáner** (que lee los códigos físicamente).

---

## 2. Encendido y Apagado del Sistema

Actualmente, tienes instalado el sistema en tu computadora (entorno de pruebas o producción local). Para operarlo, usarás la terminal general de Windows (`PowerShell`).

### **Para Encender el Panel Web (Modo de Operación)**
1. Abre una ventana de **PowerShell**.
2. Navega a la carpeta principal de tu sistema usando el comando `cd`. (Copia y pega esto y presiona Enter):
   ```powershell
   cd "C:\Anti-Gravity Funcional\QR\QR_Access_PRO"
   ```
3. Ejecuta el script de arranque rápido. (Copia y pega esto y presiona Enter):
   ```powershell
   .\start.ps1
   ```

*Qué pasa después:* La consola te mostrará un mensaje indicando que el servidor está corriendo (usualmente en el puerto 5000). Deja esta pestaña negra abierta, ya que es el "motor" de la web.

### **Para Entrar al Panel de Administración**
1. Abre tu navegador web favorito (Chrome, Edge, Firefox).
2. Ve a la dirección: `http://localhost:5000`
3. Ingresa con tus credenciales de administrador configuradas en el sistema.

### **Para Apagar el Sistema**
Existen dos formas fáciles de apagarlo:

**Forma 1 (Rápida):** En la misma consola negra donde inició el servidor, presiona **`Ctrl + C`**.

**Forma 2 (Por Comando):** Abre una ventana de PowerShell nueva y ejecuta el script de apagado que buscará el servidor en memoria y lo cerrará:
   ```powershell
   cd "C:\Anti-Gravity Funcional\QR\QR_Access_PRO"
   .\stop.ps1
   ```

---

## 3. ¿Cómo funciona la Base de Datos?

QR Access Pro utiliza una base de datos **MySQL** en segundo plano (normalmente administrada a través de herramientas externas como XAMPP, WAMP o el servicio nativo de MySQL en Windows). 

> **⚠️ Importante:** Antes de iniciar el servidor de Python (Paso 2), debes asegurarte de que tu servidor MySQL esté encendido y corriendo en el puerto `3306`. Si usas XAMPP, simplemente abre el Panel de Control de XAMPP y dale a "Start" en el módulo de MySQL. Si la base de datos no está corriendo, el Panel Web arrojará un error al intentar conectarse.

---

## 4. Scripts de Mantenimiento y Recuperación

El sistema cuenta con varios scripts de Python (`.py`) dentro de la misma carpeta principal que te permiten solucionar problemas o hacer limpieza sin necesidad de entrar directo a la base de datos:

*   `test_login.py` o `test_system.py`: Útiles para verificar si la conexión a la base de datos y al sistema interno están funcionando correctamente sin necesidad de abrir la web.
*   `limpiar_usuarios.py` / `limpiar_duplicados.py`: Para hacer limpieza en lote de registros antiguos o con errores en la base de datos.
*   `cambiar_password.py` / `reset_admin.py`: Herramientas vitales si por algún motivo pierdes el acceso a la cuenta de Administrador. Ejecutar estos scripts restablecerá la clave a un valor conocido y seguro.

Para usar cualquiera de ellos, simplemente actíva el entorno virtual `(venv)` y ejecútalos como `python nombre_del_script.py`.
