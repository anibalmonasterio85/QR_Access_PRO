
path = "web_panel/app.py"
with open(path, "r", encoding="latin-1") as f:
    contenido = f.read()

# Buscamos donde terminan los imports (usualmente antes del primer @app.route)
# Y reconstruimos el archivo garantizando que nuestra ruta este al principio
import re
partes = re.split(r"@app\.route", contenido, maxsplit=1)
cabecera = partes[0]
resto = "@app.route" + partes[1] if len(partes) > 1 else ""

# Quitamos CUALQUIER otra definicion de /panel que exista en el resto del archivo
resto_limpio = re.sub(r"@app\.route\(\"/panel\".*?def panel\(.*?\):.*?return.*?\n", "", resto, flags=re.DOTALL)

nueva_ruta = """
@app.route("/panel", methods=["GET", "POST"])
def panel():
    from flask import render_template, request, send_file
    import qrcode
    from io import BytesIO
    if request.method == "POST":
        # Datos para Anibal Monasterio
        qr = qrcode.make("USER:Anibal_Monasterio|ROLE:ADMIN")
        buf = BytesIO()
        qr.save(buf, "PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    return render_template("panel.html")

"""

with open(path, "w", encoding="utf-8") as f:
    f.write(cabecera + nueva_ruta + resto_limpio)
print("--- SISTEMA REESTRUCTURADO ---")

