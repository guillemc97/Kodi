import sys
import xbmcplugin
import xbmcgui

HANDLE = int(sys.argv[1])

video_url = "https://storage.googleapis.com/coverr-main/mp4/Mt_Baker.mp4"

item = xbmcgui.ListItem(label="Video de prueba Kodi")
item.setInfo("video", {"title": "Video de prueba Kodi"})

xbmcplugin.addDirectoryItem(
    handle=HANDLE,
    url=video_url,
    listitem=item,
    isFolder=False
)

xbmcplugin.endOfDirectory(HANDLE)
