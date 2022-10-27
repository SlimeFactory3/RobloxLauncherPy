import re
import requests
import datetime
import random
import urllib.parse
import os

cookie = "cookie" #change with roblosecurity
refer = 'https://www.roblox.com'
session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie
session.headers["Referer"]=refer


def rbx_request(method, url, **kwargs):
    request = session.request(method, url, **kwargs)
    method = method.lower()
    if (method == "post") or (method == "put") or (method == "patch") or (method == "delete"):
        if "X-CSRF-TOKEN" in request.headers:
            session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
            if request.status_code == 403:
                request = session.request(method, url, **kwargs)
    return request


req = rbx_request("POST", "https://auth.roblox.com/v1/authentication-ticket/")
req2 =rbx_request("GET","https://clientsettings.roblox.com/v1/client-version/WindowsPlayer")

presentDate = datetime.datetime.now()
LaunchTime = int(datetime.datetime.timestamp(presentDate)*1000)
#print(LaunchTime)

BrowserTrackerID = str(random.randint(100000, 120000)) + str(random.randint(100000, 900000))
#print(BrowserTrackerID)

Ticket=req.headers.get("rbx-authentication-ticket")
#print(Ticket)

PlaceID=189707 #currently launches into natural disaster survival; change this to launch into a diffrent game
#print(PlaceID)

PlaceLauncherURL=urllib.parse.quote(f"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={BrowserTrackerID}&placeId={PlaceID}&isPlayTogetherGame=false",safe='')#this could probably be merged into the webbrowser.open
#print(PlaceLauncherURL)

RobloxVersion=req2.text
RobloxVersion=re.findall(r"([a-zA-Z]+(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?[a-zA-Z]+)+)",RobloxVersion)
RobloxVersion=RobloxVersion[0][0]
#print(RobloxVersion)

RobloxPath=f"C:\\Program Files (x86)\\Roblox\\Versions\\{RobloxVersion}\\RobloxPlayerBeta.exe"
if os.path.exists(RobloxPath) == True:
    pass
else:
    RobloxPath=os.getenv('LOCALAPPDATA')+f"\\Roblox\\Versions\\{RobloxVersion}\\RobloxPlayerBeta.exe"
#print(RobloxPath)


RobloxArgs=f"--play -a https://auth.roblox.com/v1/authentication-ticket/redeem -t {Ticket} -j \"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&placeId={PlaceID}&gameId=&isPlayTogetherGame=false\""
#print(RobloxArgs)

os.startfile(filepath=RobloxPath,arguments=RobloxArgs)
