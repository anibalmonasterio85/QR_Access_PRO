
path = "web_panel/app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(path, "w", encoding="utf-8") as f:
    for line in lines:
        # Detectamos bloques comunes de Flask para asegurar indentacion de 4 espacios
        if line.strip().startswith("with app.app_context():"):
            f.write("    with app.app_context():\n")
        elif line.strip().startswith("app = create_app()"):
            f.write("app = create_app()\n")
        elif line.strip().startswith("if __name__ =="):
            f.write("if __name__ == \"__main__\":\n")
        elif line.strip().startswith("app.run"):
            f.write("    app.run(host=\"0.0.0.0\", port=5000)\n")
        else:
            f.write(line)

print("--- ESTRUCTURA DE BLOQUES NORMALIZADA ---")

