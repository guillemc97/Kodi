
"""
Genera addons.xml, addons.xml.md5 e index.html (listados de directorio)
para un repositorio de Kodi alojado en GitHub Pages.

GitHub Pages no ofrece listado automático de directorios, y Kodi
necesita encontrar enlaces <a href="..."> para poder "navegar" la
fuente e instalar los addons. Este script genera esos listados.

Ejecutar desde la raíz del repositorio: python tools/generate.py
"""

import hashlib
import os

# Nos aseguramos de trabajar desde la raíz del repo, sea cual sea
# el directorio desde el que se ejecute el script.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EXCLUIR = {".git", ".github", "tools", "__pycache__"}

# ---------------------------------------------------------------
# 1. Generar addons.xml a partir de cada addon.xml existente
# ---------------------------------------------------------------
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'
addon_dirs = []

for carpeta in sorted(os.listdir(".")):
    if carpeta in EXCLUIR or not os.path.isdir(carpeta):
        continue
    addon_xml_path = os.path.join(carpeta, "addon.xml")
    if os.path.isfile(addon_xml_path):
        addon_dirs.append(carpeta)
        with open(addon_xml_path, encoding="utf8") as f:
            contenido = f.read()
            contenido = contenido.split("?>", 1)[1]
            xml += contenido.strip() + "\n"

xml += "\n</addons>"

with open("addons.xml", "w", encoding="utf8") as f:
    f.write(xml)

md5 = hashlib.md5(xml.encode("utf-8")).hexdigest()
with open("addons.xml.md5", "w") as f:
    f.write(md5)

print(f"addons.xml generado con {len(addon_dirs)} addon(s): {', '.join(addon_dirs)}")

# ---------------------------------------------------------------
# 2. Generar index.html navegable en la raíz y en cada carpeta
#    de addon, para que Kodi pueda listar y descargar los zips.
# ---------------------------------------------------------------


OCULTAR = {"addons.xml", "addons.xml.md5", "index.html", "addon.xml"}
def generar_listado(carpeta, entradas, titulo):
    entradas = [e for e in entradas if e not in OCULTAR]
    enlaces = "\n".join(f'<li><a href="{e}">{e}</a></li>' for e in entradas)
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{titulo}</title></head>
<body>
<h1>{titulo}</h1>
<ul>
{enlaces}
</ul>
</body>
</html>
"""
    ruta = os.path.join(carpeta, "index.html") if carpeta else "index.html"
    with open(ruta, "w", encoding="utf8") as f:
        f.write(html)



# Raíz: addons.xml, addons.xml.md5 y cada carpeta de addon
raiz_entradas = ["addons.xml", "addons.xml.md5"] + [f"{d}/" for d in addon_dirs]
generar_listado("", raiz_entradas, "Mi Repositorio Kodi")

# Cada carpeta de addon: listar sus propios archivos (icon.png, addon.xml, zip...)
for carpeta in addon_dirs:
    archivos = sorted(
        f
        for f in os.listdir(carpeta)
        if os.path.isfile(os.path.join(carpeta, f))
    )
    generar_listado(carpeta, archivos, f"Index of /{carpeta}")

print("index.html generados en la raíz y en cada carpeta de addon.")