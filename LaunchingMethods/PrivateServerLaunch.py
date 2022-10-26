import requests
import datetime
import random
import urllib.parse
import webbrowser
import re

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


PrivateServerLink="link"

req = rbx_request("POST", "https://auth.roblox.com/v1/authentication-ticket/")
req2 = rbx_request("GET",PrivateServerLink)


AccessCode=re.findall("Roblox.GameLauncher.joinPrivateGame\\(\\d+\\,\\s*'(\\w+\\-\\w+\\-\\w+\\-\\w+\\-\\w+)'",req2.text)
#print(AccessCode[0])

LinkCode=re.findall("privateServerLinkCode=(.+)",PrivateServerLink)
#print(LinkCode[0])

presentDate = datetime.datetime.now()

LaunchTime = int(datetime.datetime.timestamp(presentDate)*1000)
#print(LaunchTime)

BrowserTrackerID = str(random.randint(100000, 120000)) + str(random.randint(100000, 900000))
#print(BrowserTrackerID)

Ticket=req.headers.get('rbx-authentication-ticket')
#print(Ticket)

PlaceID=123123123 #have this be the same as the placeid on PrivateServerLink; i will most likely implement a fix to this in a day or so to be automatic
#print(PlaceID)

PlaceLauncherURL=urllib.parse.quote(f"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={BrowserTrackerID}&placeId={PlaceID}&accessCode={AccessCode[0]}&linkCode={LinkCode[0]}",safe='')#this could probably be merged into the webbrowser.open
print(PlaceLauncherURL)

webbrowser.open(f"roblox-player:1+launchmode:play+gameinfo:{Ticket}+launchtime:{LaunchTime}+placelauncherurl:{PlaceLauncherURL}+browsertrackerid:{BrowserTrackerID}+robloxLocale:en_us+gameLocale:en_us+channel:") #execution
