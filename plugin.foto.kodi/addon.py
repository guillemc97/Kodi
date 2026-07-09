import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

handle = int(sys.argv[1])

ruta = os.path.dirname(os.path.abspath(__file__))

xbmc.log("Ruta del addon: " + ruta, xbmc.LOGINFO)

xbmcplugin.setContent(handle, "images")

for archivo in sorted(os.listdir(ruta)):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        imagen = os.path.join(ruta, archivo)

        xbmc.log("Imagen encontrada: " + imagen, xbmc.LOGINFO)

        item = xbmcgui.ListItem(label=archivo)
        item.setArt({
            "thumb": imagen,
            "icon": imagen,
            "fanart": imagen
        })
        item.setProperty("IsPlayable", "true")

        xbmcplugin.addDirectoryItem(
            handle=handle,
            url=imagen,
            listitem=item,
            isFolder=False
        )

xbmcplugin.endOfDirectory(handle)