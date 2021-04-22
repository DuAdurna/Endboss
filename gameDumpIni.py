import json

#ein Dict mit key value pairs, Key ist ein Game dahinter liegt ein neues Dict mit daten wie: Name, multiplayer, remote play together etc.
gameData = {}

gameData["4000"] = {
    "name": "Garry's Mod",
    "mPlayer": True,
    "remotePlay": False
}
gameData["105600"] ={
    "name": "Terraria",
    "mPlayer": True,
    "remotePlay": False
}

with open("gameData.json","w") as gamedump:
    json.dump(gameData,gamedump)