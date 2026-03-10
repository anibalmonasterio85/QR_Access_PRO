
import re
path = "web_panel/app.py"

# Leemos el archivo ignorando errores de codificacion
with open(path, "r", encoding="latin-1") as f:
    lines = f.readlines()

new_content = []
# 1. Limpiamos lineas corruptas o duplicadas de intentos anteriores
for line in lines:
    # Si la linea tiene "@app.route" o "def " mal indentada al final del archivo, la saltamos
    if line.strip().startswith("@app.route(\"/panel\"") or line.strip().startswith("def panel()"):
        continue
    new_content.append(line)

# 2. Definimos la ruta /panel perfecta
panel_route = """
@app.route("/panel", methods=["GET", "POST"])
def panel():
    from flask import render_template, request, send_file
    import qrcode
    from io import BytesIO
    if request.method == "POST":
        qr = qrcode.make("USER:Anibal_Monasterio|ROLE:ADMIN")
        buf = BytesIO()
        qr.save(buf, "PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    return render_template("panel.html")
"""

# 3. Escribimos todo de nuevo, asegurando que no haya espacios fantasma
with open(path, "w", encoding="utf-8") as f:
    for line in new_content:
        # Esto quita espacios al inicio solo si la linea parece ser una funcion principal (def/route)
        if line.startswith(" ") and ("def " in line or "@app.route" in line):
            f.write(line.lstrip())
        else:
            f.write(line)
    f.write(panel_route)

print("--- ARCHIVO RESCATADO Y NORMALIZADO ---")

