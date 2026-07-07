import hashlib
import os

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'

for carpeta in os.listdir("."):

    addon = os.path.join(carpeta, "addon.xml")

    if os.path.exists(addon):

        with open(addon, encoding="utf8") as f:

            contenido = f.read()

            contenido = contenido.split("?>")[1]

            xml += contenido

xml += "\n</addons>"

with open("addons.xml", "w", encoding="utf8") as f:
    f.write(xml)

md5 = hashlib.md5(xml.encode()).hexdigest()

with open("addons.xml.md5", "w") as f:
    f.write(md5)