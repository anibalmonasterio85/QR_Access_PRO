
path = "web_panel/app.py"
# Abrimos con latin-1 para evitar el error del byte 0xed
with open(path, "r", encoding="latin-1") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "@app.route(\"/panel\"" in line or "@app.route(\"/generar_qr\"" in line:
        skip = True
    if skip and "def " in line and "panel" not in line and "@app" in line:
        skip = False
    if not skip:
        new_lines.append(line)

final_code = """
@app.route("/panel", methods=["GET", "POST"])
def panel():
    from flask import render_template, request, send_file
    import qrcode
    from io import BytesIO
    if request.method == "POST":
        # Generando QR para Anibal Monasterio
        qr = qrcode.make("USER:Anibal_Monasterio|ROLE:ADMIN")
        buf = BytesIO()
        qr.save(buf, "PNG")
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    return render_template("panel.html")
"""

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
    f.write(final_code)
print("--- ARCHIVO LIMPIADO CON EXITO ---")

