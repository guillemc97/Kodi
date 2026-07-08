"""
Genera addons.xml, addons.xml.md5, empaqueta cada addon en su .zip
e index.html (listados de directorio) para un repositorio de Kodi
alojado en GitHub Pages.

IMPORTANTE: Kodi exige que la PRIMERA entrada dentro del zip sea la
carpeta del addon (como entrada de directorio), antes que cualquier
archivo. Si no, falla la instalación con:
  "installing addon failed ... first item is folder: false"
Por eso este script escribe esa entrada de carpeta explícitamente
como primer elemento del zip.

Ejecutar desde la raíz del repositorio: python tools/generate.py
"""

import hashlib
import os
import re
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

EXCLUIR = {".git", ".github", ".vscode", "tools", "__pycache__"}

# ---------------------------------------------------------------
# 1. Detectar addons y empaquetar cada uno en su zip
# ---------------------------------------------------------------
addon_dirs = []

for carpeta in sorted(os.listdir(".")):
    if carpeta in EXCLUIR or not os.path.isdir(carpeta):
        continue
    if os.path.isfile(os.path.join(carpeta, "addon.xml")):
        addon_dirs.append(carpeta)


def version_de(carpeta):
    with open(os.path.join(carpeta, "addon.xml"), encoding="utf8") as f:
        contenido = f.read()
    # Ignoramos la cabecera <?xml version="1.0"?> y buscamos el
    # version="..." dentro de la propia etiqueta <addon ...>
    contenido = contenido.split("?>", 1)[-1]
    m = re.search(r'<addon\b[^>]*\bversion="([^"]+)"', contenido, re.DOTALL)
    return m.group(1) if m else "1.0.0"


def empaquetar(carpeta):
    version = version_de(carpeta)
    zip_name = f"{carpeta}-{version}.zip"
    zip_path = os.path.join(carpeta, zip_name)

    if os.path.isfile(zip_path):
        return  # ya está empaquetada esta versión

    # Elimina zips de versiones antiguas de este addon
    for f in os.listdir(carpeta):
        if f.endswith(".zip") and f != zip_name:
            os.remove(os.path.join(carpeta, f))

    # Reunimos los archivos a incluir, ignorando zips, index.html
    # y carpetas vacías (no aportan nada y pueden confundir a Kodi)
    archivos = []
    for raiz, _dirs, nombres in os.walk(carpeta):
        for nombre in nombres:
            if nombre.endswith(".zip") or nombre == "index.html":
                continue
            ruta_completa = os.path.join(raiz, nombre)
            arcname = os.path.join(carpeta, os.path.relpath(ruta_completa, carpeta))
            archivos.append((ruta_completa, arcname.replace(os.sep, "/")))

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 1) Entrada de carpeta explícita PRIMERO: Kodi la exige como
        #    primer elemento del zip para aceptar la instalación.
        carpeta_info = zipfile.ZipInfo(f"{carpeta}/")
        carpeta_info.external_attr = 0o40775 << 16
        z.writestr(carpeta_info, "")

        # 2) Después, el resto de archivos
        for ruta_completa, arcname in archivos:
            z.write(ruta_completa, arcname)

    print(f"Empaquetado {zip_name}")


for carpeta in addon_dirs:
    empaquetar(carpeta)

# ---------------------------------------------------------------
# 2. Generar addons.xml a partir de cada addon.xml existente
# ---------------------------------------------------------------
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'

for carpeta in addon_dirs:
    with open(os.path.join(carpeta, "addon.xml"), encoding="utf8") as f:
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
# 3. Generar index.html navegable en la raíz y en cada carpeta
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


raiz_entradas = ["addons.xml", "addons.xml.md5"] + [f"{d}/" for d in addon_dirs]
generar_listado("", raiz_entradas, "Mi Repositorio Kodi")

for carpeta in addon_dirs:
    archivos = sorted(
        f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))
    )
    generar_listado(carpeta, archivos, f"Index of /{carpeta}")

print("index.html generados en la raíz y en cada carpeta de addon.")