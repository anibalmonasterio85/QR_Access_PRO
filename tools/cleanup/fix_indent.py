
path = "web_panel/app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(path, "w", encoding="utf-8") as f:
    for line in lines:
        # Si la linea tiene un decorador o define una funcion, eliminamos espacios al inicio
        stripped = line.lstrip()
        if stripped.startswith("@app") or stripped.startswith("def "):
            f.write(stripped)
        else:
            f.write(line)

print("--- INDENTACION CORREGIDA EN DECORADORES Y FUNCIONES ---")

