import sys
import xbmcgui
import xbmcplugin

xbmcgui.Dialog().ok("Demo", "¡Hola desde el addon!")

xbmcplugin.endOfDirectory(int(sys.argv[1]))