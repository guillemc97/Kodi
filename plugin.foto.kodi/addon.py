# -*- coding: utf-8 -*-
import os
import xbmcvfs
import xbmc

# Carpeta origen (cámbiala por la que quieras)
ORIGEN = os.path.dirname(os.path.abspath(__file__))

# Carpeta destino (el nuevo álbum)
DESTINO = "special://profile/Pictures/FodosKodi/"

# Crear el álbum si no existe
if not xbmcvfs.exists(DESTINO):
    xbmcvfs.mkdirs(DESTINO)

# Listar archivos
archivos, carpetas = xbmcvfs.listdir(ORIGEN)

copiadas = 0

for archivo in archivos:
    if archivo.lower().endswith((".jpg", ".jpeg")):
        origen = os.path.join(ORIGEN, archivo)
        destino = os.path.join(DESTINO, archivo)

        if xbmcvfs.copy(origen, destino):
            copiadas += 1

xbmc.log(f"Se copiaron {copiadas} imágenes al álbum.", xbmc.LOGINFO)

xbmc.executebuiltin(f'Notification(Álbum creado,{copiadas} imágenes copiadas,5000)')