# -*- coding: utf-8 -*-
"""
Añade automáticamente, sin preguntar nada, todas las fuentes listadas
en repos.json como fuente de archivos en Kodi (sources.xml).

Ajusta FUENTES_URL para que apunte a tu propio repos.json.
"""

import json
import traceback
import urllib.request
import xml.etree.ElementTree as ET

import xbmcgui
import xbmcvfs

FUENTES_URL = "https://guillemc97.github.io/Kodi/plugin.program.repoinstaller/repos.json"


def obtener_fuentes():
    with urllib.request.urlopen(FUENTES_URL, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def anadir_fuente(nombre, url):
    sources_path = xbmcvfs.translatePath("special://profile/sources.xml")

    if xbmcvfs.exists(sources_path):
        tree = ET.parse(sources_path)
        root = tree.getroot()
    else:
        root = ET.Element("sources")
        tree = ET.ElementTree(root)

    files_node = root.find("files")
    if files_node is None:
        files_node = ET.SubElement(root, "files")

    # Si ya existe esa URL como fuente, no la duplicamos
    for bookmark in files_node.findall("bookmark"):
        path_node = bookmark.find("path")
        if path_node is not None and path_node.text == url:
            return False  # ya existía

    bookmark = ET.SubElement(files_node, "bookmark")
    ET.SubElement(bookmark, "name").text = nombre
    ET.SubElement(bookmark, "path").text = url
    ET.SubElement(bookmark, "allowsharing").text = "true"

    tree.write(sources_path, encoding="UTF-8", xml_declaration=True)
    return True


def main():
    try:
        fuentes = obtener_fuentes()
    except Exception as e:
        xbmcgui.Dialog().notification(
            "Fuentes",
            f"No se pudo descargar repos.json: {e}",
            xbmcgui.NOTIFICATION_ERROR,
            8000,
        )
        return

    if not isinstance(fuentes, list) or not fuentes:
        xbmcgui.Dialog().notification(
            "Fuentes", "repos.json está vacío o mal formado", xbmcgui.NOTIFICATION_ERROR
        )
        return

    anadidas = 0
    for fuente in fuentes:
        try:
            nombre = fuente["name"]
            url = fuente["repo"]
        except (KeyError, TypeError) as e:
            xbmcgui.Dialog().notification(
                "Fuentes",
                f"Entrada inválida en repos.json (falta {e}). Debe tener 'name' y 'repo'.",
                xbmcgui.NOTIFICATION_ERROR,
                8000,
            )
            continue

        try:
            if anadir_fuente(nombre, url):
                anadidas += 1
        except Exception:
            xbmcgui.Dialog().notification(
                "Fuentes",
                f"Error añadiendo '{nombre}', revisa el log",
                xbmcgui.NOTIFICATION_ERROR,
            )
            # Vuelca el error completo al log de Kodi para poder depurarlo
            import xbmc

            xbmc.log(traceback.format_exc(), xbmc.LOGERROR)

    if anadidas:
        xbmcgui.Dialog().notification(
            "Fuentes",
            f"{anadidas} fuente(s) añadida(s). Reinicia Kodi para verlas.",
            xbmcgui.NOTIFICATION_INFO,
        )
    else:
        xbmcgui.Dialog().notification(
            "Fuentes", "Todas las fuentes ya estaban añadidas", xbmcgui.NOTIFICATION_INFO
        )


if __name__ == "__main__":
    main()