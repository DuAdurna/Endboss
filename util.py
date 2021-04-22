import requests
import json
import time
from colorama import Fore, Back, Style


# print(list(spieleDaten.games.values()))
# print(Fore.BLUE + str(str((list(spiele.games.values())[-1])).rsplit(',1)[0]).split(':',1)[1])
#  print(Fore.RED + ("Game " + str(counter) + " von " + str(len(masterGameList)) + " wurde hinzugefuegt&quot)
# print(Style.RESET_ALL)
class gameData:
    """gmae Data ist eine Liste der SPiele für die Daten gesammelt werden. Diese werden aus einem File geladen und da
    wieder rein gepackt. zusätzlich kann für eine gegebene AppId der steam API ein Game Nachgeschaut werden und falls
    keine Daten vorliegen so wird das Spiel nachgeschaut """

    def __init__(self, gameDataFile=None, failDataFile=None):
        if gameDataFile is not None:
            try:
                with open(gameDataFile) as gameInfoDatei:
                    self.games = json.load(gameInfoDatei)
            except FileNotFoundError:
                self.games = {}
        else:
            self.games = {}
        if failDataFile is not None:
            try:
                with open(failDataFile) as failInfoDatei:
                    self.faillist = json.load(failInfoDatei)
            except FileNotFoundError:
                self.faillist = []
        else:
            self.faillist = []

        # Api Key der Person, von der der Zugriff ausgeht
        self.key = "01B5B710F0BE9A09BF1E010E5EA38374"
        # Steamids der Freunde
        self.steamIds = {
            "Jan": 76561198055057775,
            "Felix": 76561198097530808,
            "Max": 76561198293306869,
            "Manu": 76561198117034035,
            "Maido": 76561198215794857,
            "Maido²": 76561198040993319,
            "Dome": 76561198036790611,
            "Simon": 76561199050767225,
            "Leon": 76561198052633626,
            "Kilian": 76561198059004685,
        }

    def addGame(self, appId, spieler):
        try:
            faileintrag = {"ID": appId, "response": {str(appId): {"success": False}}}
            if faileintrag in self.faillist:
                print("game in Faillist vorhanden")
                return
            return (self.games[spieler][str(appId)])
        except KeyError:
            # schaue daten über app in steam api nach.
            parameter = {"appids": str(appId)}
            print("ich requeste grade: " + str(appId))
            gameAPIRequest = requests.get("https://store.steampowered.com/api/appdetails/?", params=parameter)
            gameApiOut = json.loads(gameAPIRequest.content)
            if gameApiOut[str(appId)]["success"] == False:
                print(str(appId) + " hat gefailt")
                time.sleep(2)
                self.faillist.append(
                    {
                        "ID": appId,
                        "response": json.loads(gameAPIRequest.content)
                    })
                return
            gameApiData = gameApiOut[str(appId)]["data"]
            del gameApiOut
            gameName = gameApiData["name"]
            print("ich warte jetzt, nachdem ich: " + gameName + " angefragt hab")
            time.sleep(2)
            isMultiplayer = False
            isRemoteplay = False
            try:
                for category in gameApiData['categories']:
                    if category["id"] == 1:
                        isMultiplayer = True
                    if category["id"] == 44:
                        isRemoteplay = True
            except KeyError:
                pass
            try:
                self.games[spieler]
            except KeyError:
                self.games[spieler] = {}

            self.games[spieler][str(appId)] = {
                "name": gameName,
                "mPlayer": isMultiplayer,
                "remotePlay": isRemoteplay
            }
            return self.games[spieler][str(appId)]

    def save(self, gameDataName="gameData.json", failDataName="requestFails.json"):
        with open(gameDataName, "w") as gameSaveDatei:
            json.dump(self.games, gameSaveDatei)
        with open(failDataName, "w") as failDataDatei:
            json.dump(self.faillist, failDataDatei)

    def addGameByHand(self, player, gameName=None, mPlayer=None, remotePlay=None):
        """AddGameByHand soll der Liste ein spiel hinzufügen, obwohl dieses nicht bei Steam ist! wichtig ist hier,
        dass wir das ganze so gestalten dass wir Datenqualität haben und """
        if player is None:
            print("Please select a Player")
            return
        if gameName is None:
            print("Please select a Game")
            return
        for spieler in player:
            self.games[spieler][gameName] = {
                "name": gameName,
                "mPlayer": True,
                "remotePlay": False
                }

    def generateParamsPerPerson(self):
        self.paramsPerPerson = {}
        for person in self.steamIds:
            self.paramsPerPerson[person] = {
                "key": self.key,
                "steamid": str(self.steamIds[person]),  # beachte steam ids werden als zahl gehandelt
                "include_played_free_games": True
            }


"""
------------------------Testcode Unter dieser Linie--------------------------------------------------------------------
"""

spieleDaten = gameData(gameDataFile="gameData.json", failDataFile="requestFails.json")
paramsPerPerson = spieleDaten.generateParamsPerPerson()

ausgewaehlteSpieler = ["Simon", "Felix", "Max", "Jan", "Manu", "Maido", "Maido²", "Dome", "Leon", "Kilian"]


persGameList = {}
# Erstellen einer Liste welche Person Welche Spiele hat.
for person in ausgewaehlteSpieler:
    apiAusspuck = requests.get(
        "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?",
        params=spieleDaten.paramsPerPerson[person])
    gamesImBesitz = json.loads(apiAusspuck.content)
    persGameList[person] = []
    for game in gamesImBesitz["response"]["games"]:
        # erstellt eine liste welche spiele Jeder hat
        persGameList[person].append(game["appid"])

# sortieren in Remote play games und nicht remoteplay
masterGameList = persGameList[ausgewaehlteSpieler[0]]
for listePerson in persGameList:
    masterGameList = list(set(masterGameList) & set(persGameList[listePerson]))

counter = 0
for person in ausgewaehlteSpieler:
    for game in persGameList[person]:
        spieleDaten.addGame(game,person)

        print(Fore.BLUE + str(str(list(spieleDaten.games.values())[-1]).rsplit(',')[0]).split(':',1)[1])

        print(Fore.RED + "index: " + str(counter) + " von " + str(len(persGameList[person])) + " von " + person)
        counter = counter + 1
        if counter == len(persGameList[person]):
            counter = 0
        print(Style.RESET_ALL)
        if counter % 31 == 0:
            spieleDaten.save()
            print("ich habe zwischengespeichert")


spieleDaten.save()
print(masterGameList)
print(persGameList)
print('penis')
""" Spiele die per ahnd hinzugefügt werden müssen:
Dying light, Overwatch, Lol, Scribble Io, Gartic Phone, Factorio (maid), minecraft


"""