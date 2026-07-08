# -*- coding: utf-8 -*-
"""
Añade automáticamente, sin preguntar nada, todas las fuentes listadas
en fuentes.json como fuente de archivos en Kodi (sources.xml).

Ajusta FUENTES_URL para que apunte a tu propio fuentes.json.
"""

import json
import urllib.request
import xml.etree.ElementTree as ET

import xbmcgui
import xbmcvfs

FUENTES_URL = "https://guillemc97.github.io/Kodi/plugin.program.repoinstaller/repos.json"


def obtener_fuentes():
    try:
        with urllib.request.urlopen(FUENTES_URL, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        xbmcgui.Dialog().notification(
            "Fuentes",
            "No se pudo descargar la lista de fuentes",
            xbmcgui.NOTIFICATION_ERROR,
        )
        return []


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
    fuentes = obtener_fuentes()
    if not fuentes:
        return

    anadidas = 0
    for fuente in fuentes:
        if anadir_fuente(fuente["nombre"], fuente["url"]):
            anadidas += 1

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