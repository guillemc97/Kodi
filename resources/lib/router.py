import sys, xbmcplugin, xbmcgui
def router():
    h=int(sys.argv[1])
    item=xbmcgui.ListItem("Hola Kodi")
    xbmcplugin.addDirectoryItem(h,"https://example.com/video.mp4",item,False)
    xbmcplugin.endOfDirectory(h)
