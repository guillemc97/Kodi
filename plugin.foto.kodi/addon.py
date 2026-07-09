import os
import xbmcgui
import xbmcplugin
import sys

handle = int(sys.argv[1])

ruta = os.path.dirname(os.path.abspath(__file__))

for archivo in sorted(os.listdir(ruta)):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        imagen = os.path.join(ruta, archivo)

        li = xbmcgui.ListItem(label=archivo)
        li.setArt({
            "thumb": imagen,
            "icon": imagen,
            "fanart": imagen
        })

        xbmcplugin.addDirectoryItem(
            handle,
            imagen,
            li,
            isFolder=False
        )

xbmcplugin.endOfDirectory(handle)