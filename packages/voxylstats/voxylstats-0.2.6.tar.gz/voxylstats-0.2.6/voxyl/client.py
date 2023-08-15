import requests
from voxyl.guildstats import GuildLB, GuildStats
from voxyl.leaderboardstats import LevelWeightedLB, TechniqueLB

from voxyl.playerstats import PlayerStats
from voxyl.utils import *

from .constants import *

class Client():
    def __init__(self, key):
        r = requests.get(VOXYLBASE + VOXYLINFO.format("7dc5566d-4c2c-40dd-891c-4717d8f44713", VOXYLAPI.format(key)))

        if r.status_code != 200:
            raise InvalidAPIKey(f"Invalid API Key: " + key)
        
        self.key = key
    
    def set_key(self, key):        
        r = requests.get(VOXYLBASE + VOXYLINFO.format("7dc5566d-4c2c-40dd-891c-4717d8f44713", VOXYLAPI.format(key)))

        if r.status_code != 200:
            raise InvalidAPIKey(f"Invalid API Key: " + key)
        
        self.key = key
        return True

    def show_key(self):
        return self.key

    def remove_key(self):
        try:
            self.key = ""
            return True
        
        except Exception as e:
            raise e

    def get_player(self, uuid=None, ign=None):
        if uuid != None:
            if uuid.find("-") == -1:
                uuidFormated = getUserInfo.formatUUID(uuid)
            
            else:
                uuidFormated = uuid
        
        elif ign != None:
            uuidFormated = getUserInfo.formatUUID(getUserInfo.getUUID(ign))

        info = requests.get(f"{VOXYLBASE}{VOXYLINFO.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
        over = requests.get(f"{VOXYLBASE}{VOXYLOVERALL.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
        game = requests.get(f"{VOXYLBASE}{VOXYLGAME.format(uuidFormated, VOXYLAPI.format(self.key))}").json()
       
        if not info["success"] or not over["success"] or not game["success"]:
            return None
        
        return PlayerStats(uuid=uuidFormated, gen=info, over=over, game=game["stats"])
    
    def get_guild(self, tag):
        guildInfo = requests.get(f"{VOXYLBASE}{VOXYLGUILDINFO.format(tag, VOXYLAPI.format(self.key))}").json()
        guildMembers = requests.get(f"{VOXYLBASE}{VOXYLGUILDMEMBERS.format(tag, VOXYLAPI.format(self.key))}").json()

        if not guildInfo["success"] or not guildMembers["success"]:
            return None
        
        return GuildStats(infoData=guildInfo, membersData=guildMembers["members"], key=self.key)
    
    def get_guild_LB(self, num: int = 10):
        guildLB = requests.get(f"{VOXYLBASE}{VOXYLGUILDTOP.format(VOXYLAPI.format(self.key), num)}").json()

        if not guildLB["success"]:
            return None
        
        return GuildLB(guildLBInfo=guildLB["guilds"], num=num, key=self.key)
    
    def getLB(self, type: str = "level", num: int = 10, technique: str = ""):
        teststr = "7dc5566d-4c2c-40dd-891c-4717d8f44713"
        r = requests.get(f"{VOXYLBASE}{VOXYLINFO.format(teststr, VOXYLAPI.format(self.key))}").json()
        
        if not r["success"]:
            return None

        if type.lower() != "technique":
            lbInfo = requests.get(f"{VOXYLBASE}{VOXYLLB[type.lower()].format(VOXYLAPI.format(self.key), num)}").json()["players"]
            return LevelWeightedLB(lbInfo, key=self.key)

        elif type.lower() == "technique":
            lbInfo = requests.get(f"{VOXYLBASE}{VOXYLLB[type.lower()].format(VOXYLAPI.format(self.key), technique)}").json()["guilds"]
            return TechniqueLB(lbInfo, key=self.key)
        
        else:
            raise InvalidLeaderBoard(f"Leaderboard '{type}' does not exist")

class InvalidAPIKey(Exception):
    pass

class InvalidLeaderBoard(Exception):
    pass
    