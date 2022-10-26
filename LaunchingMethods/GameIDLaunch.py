import requests
import datetime
import random
import urllib.parse
import webbrowser

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

presentDate = datetime.datetime.now()

LaunchTime = int(datetime.datetime.timestamp(presentDate)*1000)
#print(LaunchTime)

BrowserTrackerID = str(random.randint(100000, 120000)) + str(random.randint(100000, 900000))
#print(BrowserTrackerID)

Ticket=req.headers.get('rbx-authentication-ticket')
#print(Ticket)

PlaceID=189707 #currently launches into natural disaster survival; change this to launch into a diffrent game
#print(PlaceID)

GameID='id' #game id changes quite often based on if the server shuts down or not etc etc
#print(GameID)
#this isnt private servers; they have diffrent parameters; albeit the fix is easy

PlaceLauncherURL=urllib.parse.quote(f"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={BrowserTrackerID}&placeId={PlaceID}&gameId={GameID}&isPlayTogetherGame=false",safe='')#this could probably be merged into the webbrowser.open
#print(PlaceLauncherURL)

webbrowser.open(f"roblox-player:1+launchmode:play+gameinfo:{Ticket}+launchtime:{LaunchTime}+placelauncherurl:{PlaceLauncherURL}+browsertrackerid:{BrowserTrackerID}+robloxLocale:en_us+gameLocale:en_us+channel:") #execution
