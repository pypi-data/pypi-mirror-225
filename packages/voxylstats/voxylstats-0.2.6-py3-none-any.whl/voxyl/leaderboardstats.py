import requests
import json
from voxyl.playerstats import WeightedLevelLBPlayer, TechniqueLBPlayer

from voxyl.utils import getUserInfo
from .constants import *

class LevelWeightedLB:
    def __init__(self, lbInfo, key=""):
        self.lbInfo = lbInfo
        self.key = key
    
    def get_player(self, ign):
        member = getUserInfo.formatUUID(getUserInfo.getUUID(ign))

        for i in self.lbInfo:
            if i["uuid"] == member:
                uuidFormated = i["uuid"]
                info = requests.get(f"{VOXYLBASE}{VOXYLINFO.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
                over = requests.get(f"{VOXYLBASE}{VOXYLOVERALL.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
                game = requests.get(f"{VOXYLBASE}{VOXYLGAME.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
            
                if not info["success"] or not over["success"] or not game["success"]:
                    return None

                return WeightedLevelLBPlayer(uuid=member, gen=info, over=over, game=game["stats"], placing=i["position"])

        raise LeaderboardPlayerNotFound(f"{ign} not found in leaderboards")

class TechniqueLB:
    def __init__(self, lbInfo, key=""):
        self.lbInfo = lbInfo
        self.key = key
    
    def get_player(self, ign):
        member = getUserInfo.formatUUID(getUserInfo.getUUID(ign))

        for i in self.lbInfo:
            if i["uuid"] == member:
                uuidFormated = i["uuid"]
                info = requests.get(f"{VOXYLBASE}{VOXYLINFO.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
                over = requests.get(f"{VOXYLBASE}{VOXYLOVERALL.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
                game = requests.get(f"{VOXYLBASE}{VOXYLGAME.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
            
                if not info["success"] or not over["success"] or not game["success"]:
                    return None

                return TechniqueLBPlayer(uuid=member, gen=info, over=over, game=game["stats"], placing=i["position"], time=i["time"], subtime=i["submittime"])

        raise LeaderboardPlayerNotFound(f"{ign} not found in leaderboards")

class LeaderboardPlayerNotFound(Exception):
    pass