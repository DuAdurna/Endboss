import requests
import json
import time
import pyperclip


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
        self.key = "1EB3549A4CF22E85EF4D96DE8E8F565E"
        # Steamids der Freunde
        self.steamIds = {
            "Jan": 76561198055057775,
            "Felix": 76561198097530808,
            "Max": 76561198293306869,
            "Manu": 76561198117034035,
            "Maido": 76561198215794857,
            "Dome": 76561198036790611,
            "Simon": 76561199050767225,
            "Leon": 76561198052633626,
            "Kilian": 76561198059004685,
            "Moritz": 76561198097568563,
            "Paul": 76561198279221273,
        }

    def giveGames(self):
        return self.games

    def addGame(self, appId, spieler):
        try:
            faileintrag = {"ID": appId, "response": {str(appId): {"success": False}}}
            if faileintrag in self.faillist:
                return
            return (self.games[spieler][str(appId)])
        except KeyError:
            # schaue daten über app in steam api nach.
            parameter = {"appids": str(appId)}
            gameAPIRequest = requests.get("http://store.steampowered.com/api/appdetails/?", params=parameter)
            gameApiOut = json.loads(gameAPIRequest.content)
            if gameApiOut[str(appId)]["success"] == False:
                print(str(appId) + " hat gefailt, das kann erwartet sein!")
                time.sleep(1.2)
                self.faillist.append(
                    {
                        "ID": appId,
                        "response": json.loads(gameAPIRequest.content)
                    })
                return
            gameApiData = gameApiOut[str(appId)]["data"]
            del gameApiOut
            gameName = gameApiData["name"]
            time.sleep(1.2)
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
                "remotePlay": isRemoteplay,
                "spielerAnzahl": None
            }
            return self.games[spieler][str(appId)]

    def save(self, gameDataName="gameData.json", failDataName="requestFails.json"):
        with open(gameDataName, "w") as gameSaveDatei:
            json.dump(self.games, gameSaveDatei)
        with open(failDataName, "w") as failDataDatei:
            json.dump(self.faillist, failDataDatei)

    def addGameByHand(self, player,gameName=None, spielerAnzahl=None, gameID=None):
        """AddGameByHand soll der Liste ein spiel hinzufügen, obwohl dieses nicht bei Steam ist! wichtig ist hier,
        dass wir das ganze so gestalten dass wir Datenqualität haben und """
        if player is None:
            print("Please select a Player")
            return
        if gameName is None:
            print("Please select a Game")
            return
        if gameID is None:
            #Please select a game id, if none present, Endboss uses the name!
            gameID = gameName
        for spieler in player:
            try:
                self.games[spieler]
            except KeyError:
                self.games[spieler] = {}
            self.games[spieler][gameID] = {
                "name": gameName,
                "mPlayer": True,
                "remotePlay": False,
                "spielerAnzahl": spielerAnzahl
            }

    def generateParamsPerPerson(self):
        self.paramsPerPerson = {}
        for person in self.steamIds:
            self.paramsPerPerson[person] = {
                "key": self.key,
                "steamid": str(self.steamIds[person]),  # beachte steam ids werden als zahl gehandelt
                "include_played_free_games": True,
                "include_appinfo": True
            }

    def getCommonGames(self, ausgewaehlteSpieler=None):
        # Dies ist dafür da, die überschneidungen zwischen verschiedenen Leuten zu finden und auszugeben
        if ausgewaehlteSpieler is None:
            print("Geb halt spieler ein du Horst")
            return
        uberschneidungen = list(self.games[ausgewaehlteSpieler[0]].keys())
        for appid in uberschneidungen:
            if self.games[ausgewaehlteSpieler[0]][str(appid)]["mPlayer"] is False:
                uberschneidungen.remove(appid)
            elif self.games[ausgewaehlteSpieler[0]][str(appid)]["spielerAnzahl"] is not None:
                if self.games[ausgewaehlteSpieler[0]][str(appid)]["spielerAnzahl"] < len(ausgewaehlteSpieler):
                    uberschneidungen.remove(appid)
        remoteplayGames = []
        gemeinsamGames = []
        for spieler in ausgewaehlteSpieler:
            uberschneidungen = set(uberschneidungen) & set(self.games[spieler].keys())
            for game in self.games[spieler]:
                if self.games[spieler][str(game)]["remotePlay"]:
                    if self.games[spieler][str(game)]["spielerAnzahl"] is not None:
                        if self.games[spieler][str(game)]["spielerAnzahl"] >= len(ausgewaehlteSpieler) \
                            and self.games[spieler][str(game)]["name"] not in remoteplayGames:
                            remoteplayGames.append(self.games[spieler][str(game)]["name"])
                    elif self.games[spieler][str(game)]["name"] not in remoteplayGames:
                        remoteplayGames.append(self.games[spieler][str(game)]["name"])
                        #schon mal was von cases gehoert?:D hier müsste ich die aussagen mit AND verbinden aber fande das so übersichtlicher, cases bringen nix :P
        for appid in uberschneidungen:
            if self.games[ausgewaehlteSpieler[0]][str(appid)]["spielerAnzahl"] is not None:
                if self.games[ausgewaehlteSpieler[0]][str(appid)]["spielerAnzahl"] >= len(ausgewaehlteSpieler):
                    gemeinsamGames.append(self.games[ausgewaehlteSpieler[0]][str(appid)]["name"])
            else:
                gemeinsamGames.append(self.games[ausgewaehlteSpieler[0]][str(appid)]["name"])
        gemeinsamGames.sort()
        remoteplayGames.sort()
        return [gemeinsamGames, remoteplayGames]

    def updateGameData(self,ausgewaehlteSpieler=["Manu", "Jan", "Simon", "Max", "Maido", "Felix", "Dome", "Moritz", "Leon", "Kilian","Paul"]):
        """ Lädt die Spiele in die Daten rein, bzw updatet sie"""
        mnu = "Manu"
        jan = "Jan"
        smn = "Simon"
        max = "Max"
        mad = "Maido"
        flx = "Felix"
        dom = "Dome"
        mtz = "Moritz"
        all = [smn, flx, max, jan, mnu, mad, dom, "Leon", "Kilian", mtz, "Paul"]
        self.addGameByHand([mnu, dom, mad, flx], "Dying Light", 4)
        self.addGameByHand([mnu, mad, flx, smn, max, jan], "Overwatch", 6)
        self.addGameByHand([mnu, mad, mtz, jan, flx, smn, "Paul", "Leon", "Kilian"], "League of Legends", 5)
        self.addGameByHand(all, "Minecraft", 99)
        self.addGameByHand(all, "Geoguesser/Geotastic", 99)
        self.addGameByHand(all, "Gartic Phone", 15)
        persGameList = self.genPersGameList(ausgewaehlteSpieler)
        gcounter = 0
        glange = 0
        start = time.time()
        for person in ausgewaehlteSpieler:
            glange = glange + len(persGameList[person])
        for person in ausgewaehlteSpieler:
            counter = 1
            for game in persGameList[person]:
                self.addGame(game, person)
                print(list(self.games[person].values())[-1]["name"])
                print("index: " + str(counter) + " (" + str(gcounter + counter) + ")"
                      + " von " + str(len(persGameList[person])) + " (" + str(glange) + ") von " +
                      person + "\n" )
                counter = counter + 1
                if (gcounter + counter) % 53 == 0 or (time.time() - start) > 20:
                    self.save()
                    print("ich habe zwischengespeichert")
                    start = time.time()
            gcounter = gcounter + counter
        self.save()
        return

    def genPersGameList(self, ausgewaehlteSpieler=None):
        self.generateParamsPerPerson()
        persGameList = {}
        for person in ausgewaehlteSpieler:
            apiAusspuck = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?",
                                       params=self.paramsPerPerson[person])
            gamesImBesitz = json.loads(apiAusspuck.content)
            persGameList[person] = []
            for game in gamesImBesitz["response"]["games"]:
                # erstellt eine liste welche spiele Jeder hat
                persGameList[person].append(game["appid"])

        return persGameList

    def spielerAnzahlEintragen(self):
        for spieler in self.games:
            for game in self.games[spieler]:
                if (self.games[spieler][game]["mPlayer"] or self.games[spieler][game]["remotePlay"]) and \
                        self.games[spieler][game]["spielerAnzahl"] is None:
                    erfolg = self.getAnzahlSpieler(self.games[spieler][game]["name"])
                    if erfolg is None:
                        pyperclip.copy(self.games[spieler][game]["name"])
                        spielerAzahl = input(
                            "Spieleranzahl von " + self.games[spieler][game]["name"] + " eintragen (remoteplay: " + str(
                                self.games[spieler][game]["remotePlay"]) + "): ")
                        if spielerAzahl == "q":
                            self.save()
                            return
                        if spielerAzahl == "?":
                            pass
                        else:
                            self.games[spieler][game]["spielerAnzahl"] = int(spielerAzahl)
                            self.save()
                    else:
                        print("spieleranzahl gefunden für: " + self.games[spieler][game]["name"])
                        self.games[spieler][game]["spielerAnzahl"] = erfolg

    def editAnzahlSpieler(self, gameName, neueZahl):
        for spieler in self.games:
            for game in self.games[spieler]:
                if self.games[spieler][game]["name"] == gameName:
                    self.games[spieler][game]["spielerAnzahl"] = neueZahl
                    print("Spieleranzahl von Spiel " + str(gameName) +" auf " + str(neueZahl) + " geändert!" )
                    self.save
        return

    def getAnzahlSpieler(self, gameName):
        for spieler in self.games:
            for game in self.games[spieler]:
                if self.games[spieler][game]["name"] == gameName and \
                    self.games[spieler][game]["spielerAnzahl"] is not None:
                    return self.games[spieler][game]["spielerAnzahl"]

    def getRankedGames(self, ausgewaehlteSpieler=None, recent=True):
        commonGames = self.getCommonGames(ausgewaehlteSpieler)
        self.generateParamsPerPerson()
        rankingListRecent = {}
        rankingListEver = {}
        remoterankingListRecent = {}
        remoterankingListEver = {}
        for person in ausgewaehlteSpieler:
            apiAusspuck = requests.get(
                "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?",
                params=self.paramsPerPerson[person])
            gamesImBesitz = json.loads(apiAusspuck.content)
            for game in gamesImBesitz["response"]["games"]:
                if game["name"] in commonGames[0]:
                    # hier kumulativ die spielstunden errechen!
                    try:
                        rankingListRecent[game["name"]]
                    except KeyError:
                        rankingListRecent[game["name"]] = 0
                    try:
                        rankingListRecent[game["name"]] = rankingListRecent[game["name"]] + game["playtime_2weeks"]
                    except KeyError:
                        pass

                    try:
                        rankingListEver[game["name"]]
                    except KeyError:
                        rankingListEver[game["name"]] = 0
                    try:
                        rankingListEver[game["name"]] = rankingListEver[game["name"]] + game["playtime_forever"]
                    except KeyError:
                        pass
                if game["name"] in commonGames[1]:
                    # hier kumulativ die spielstunden errechen! (remoteplay games)
                    try:
                        remoterankingListRecent[game["name"]]
                    except KeyError:
                        remoterankingListRecent[game["name"]] = 0
                    try:
                        remoterankingListRecent[game["name"]] = remoterankingListRecent[game["name"]] + game["playtime_2weeks"]
                    except KeyError:
                        pass
                    try:
                        remoterankingListEver[game["name"]]
                    except KeyError:
                        remoterankingListEver[game["name"]] = 0
                    try:
                        remoterankingListEver[game["name"]] = remoterankingListEver[game["name"]] + game["playtime_forever"]
                    except KeyError:
                        pass
        #spiele die nicht in steam sind werden besser als 0 bewertet :D
        for game in commonGames[0]:
            try:
                rankingListEver[game]
            except KeyError:
                rankingListEver[game] = 120*len(ausgewaehlteSpieler)
            try:
                rankingListRecent[game]
            except KeyError:
                rankingListRecent[game] = 120*len(ausgewaehlteSpieler)

        #rankings sortieren
        rankingListRecent = dict(sorted(rankingListRecent.items(), key=lambda item: item[1], reverse=True))
        rankingListEver = dict(sorted(rankingListEver.items(), key=lambda item: item[1], reverse=True))
        remoterankingListRecent = dict(sorted(remoterankingListRecent.items(), key=lambda item: item[1], reverse=True))
        remoterankingListEver = dict(sorted(remoterankingListEver.items(), key=lambda item: item[1], reverse=True))
        #output entsprechend der wünsche anpassen (hatte keine lust alles in if zu packen deswegen wird immer beides berechnet
        if recent:
            return [rankingListRecent, remoterankingListRecent]
        else:
            return [rankingListEver, remoterankingListEver]

"""
------------------------Testcode Unter dieser Linie--------------------------------------------------------------------
"""

"""
spieleDaten = gameData(gameDataFile="gameData.json", failDataFile="requestFails.json")
spieleDaten.spielerAnzahlEintragen()
spieleDaten.save()
#"""
