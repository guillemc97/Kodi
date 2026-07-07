import os
import urllib.request
import xbmc
import xbmcgui
import xbmcvfs

ZIP_URL = "https://bugatsinho.github.io/repo/repository.bugatsinho-2.8.zip"

dialog = xbmcgui.Dialog()

temp = xbmcvfs.translatePath("special://temp/")
zip_file = os.path.join(temp, "repository.bugatsinho.zip")

dialog.notification("Descargando", "Repositorio Bugatsinho")

urllib.request.urlretrieve(ZIP_URL, zip_file)

xbmc.executebuiltin(f'InstallAddon("{zip_file}")')

dialog.notification("Finalizado", "Repositorio instalado")