"""
Genera addons.xml, addons.xml.md5 e index.html (listados de directorio)
para un repositorio de Kodi alojado en GitHub Pages.

GitHub Pages no ofrece listado automático de directorios, y Kodi
necesita encontrar enlaces <a href="..."> para poder "navegar" la
fuente e instalar los addons. Este script genera esos listados.

Además, lee fuentes.json y añade en la página principal una lista
de otros repositorios recomendados (solo informativa: el usuario
tiene que copiar la URL y añadirla a mano como fuente en Kodi).

Ejecutar desde la raíz del repositorio: python tools/generate.py
"""

import hashlib
import json
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
# 2. Cargar fuentes.json (lista de repos recomendados, opcional)
# ---------------------------------------------------------------
fuentes = []
if os.path.isfile("fuentes.json"):
    with open("fuentes.json", encoding="utf8") as f:
        fuentes = json.load(f)

# ---------------------------------------------------------------
# 3. Generar index.html navegable en la raíz y en cada carpeta
#    de addon, para que Kodi pueda listar y descargar los zips.
# ---------------------------------------------------------------


def generar_listado(carpeta, entradas, titulo, seccion_fuentes_html=""):
    enlaces = "\n".join(f'<li><a href="{e}">{e}</a></li>' for e in entradas)
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{titulo}</title></head>
<body>
<h1>{titulo}</h1>
{seccion_fuentes_html}
<h2>Archivos</h2>
<ul>
{enlaces}
</ul>
</body>
</html>
"""
    ruta = os.path.join(carpeta, "index.html") if carpeta else "index.html"
    with open(ruta, "w", encoding="utf8") as f:
        f.write(html)


def generar_seccion_fuentes(fuentes):
    if not fuentes:
        return ""
    items = "\n".join(
        f'<li><strong>{f["nombre"]}</strong><br>'
        f'<code>{f["url"]}</code></li>'
        for f in fuentes
    )
    return f"""
<h2>Fuentes recomendadas para Kodi</h2>
<p>Copia la URL y añádela en Kodi: Ajustes &rarr; Sistema &rarr; Gestor de archivos &rarr; Añadir fuente.</p>
<ul>
{items}
</ul>
"""


seccion_fuentes = generar_seccion_fuentes(fuentes)

# Raíz: addons.xml, addons.xml.md5, cada carpeta de addon, y la lista de fuentes
raiz_entradas = ["addons.xml", "addons.xml.md5"] + [f"{d}/" for d in addon_dirs]
generar_listado("", raiz_entradas, "Mi Repositorio Kodi", seccion_fuentes)

# Cada carpeta de addon: listar sus propios archivos (icon.png, addon.xml, zip...)
for carpeta in addon_dirs:
    archivos = sorted(
        f
        for f in os.listdir(carpeta)
        if os.path.isfile(os.path.join(carpeta, f))
    )
    generar_listado(carpeta, archivos, f"Index of /{carpeta}")

print("index.html generados en la raíz y en cada carpeta de addon.")