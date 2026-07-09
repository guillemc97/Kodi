import os
import shutil
import xbmcgui

# Carpeta donde está el addon
origen = os.path.dirname(os.path.abspath(__file__))

# Abrir selector de carpeta
dialog = xbmcgui.Dialog()
destino = dialog.browseSingle(
    type=0,
    heading="Selecciona la carpeta donde copiar las imágenes",
    shares="files"
)

# Si el usuario cancela
if not destino:
    raise SystemExit

# Copiar las imágenes
copiadas = 0

for archivo in os.listdir(origen):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        shutil.copy2(
            os.path.join(origen, archivo),
            os.path.join(destino, archivo)
        )
        copiadas += 1

dialog.ok(
    "Fotos",
    f"Se han copiado {copiadas} imágenes."
)