from datetime import datetime
import requests
import json
from voxyl.playerstats import PlayerStats
from voxyl.utils import *
from .constants import *

class GuildLB:
    def __init__(self, guildLBInfo, num, key=""):
        self.guildLB = guildLBInfo
        self.num = num
        self.key = key

    def get_guild(self, tag):
        for i in self.guildLB:
            if i["tag"].lower() == tag:
                guildInfo = requests.get(f"{VOXYLBASE}{VOXYLGUILDINFO.format(tag, VOXYLAPI.format(self.key))}").json()
                guildMembers = requests.get(f"{VOXYLBASE}{VOXYLGUILDMEMBERS.format(tag, VOXYLAPI.format(self.key))}").json()

                if not guildInfo["success"] or not guildMembers["success"]:
                    return None

                return GuildLBGuild(infoData=guildInfo, membersData=guildMembers["members"], placing=i["placing"], key=self.key)
        
        raise GuildNotFound(f"'{tag}' not found in top {self.num} requested guilds")
    

class GuildStats:
    def __init__(self, infoData, membersData, key=""):
        self.id = infoData["id"]
        self.name = infoData["name"]
        self.desc = infoData["desc"]
        self.xp = infoData["xp"]
        self.num = infoData["num"]
        self.owner = infoData["ownerUUID"]
        self.creationTimeRaw = infoData["time"]
        self.creationTime = datetime.fromtimestamp(self.creationTimeRaw).strftime("%I:%M %p on %B %d, %Y")
        self.allMembers = get_members(membersData)
        self.memberUUIDs = self.allMembers["owner"] + self.allMembers["admin"] + self.allMembers["moderator"] + self.allMembers["member"]
        self.rawData = membersData
        self.key = key

    def getGuildMember(self, ign):
        member = getUserInfo.formatUUID(getUserInfo.getUUID(ign))

        for i in self.rawData:
            if i["uuid"] == member:
                return GuildMember(i["uuid"], i["role"], i["time"], self.key)

        raise GuildMemberNotFound(f"{ign} not found in guild '{self.name}'")

    def getGuildMembers(self):
        self.membersList = []
        for i in self.rawData:
            self.membersList.append(GuildMember(i["uuid"], i["role"], i["time"], self.key))
        
        return self.membersList

class GuildLBGuild(GuildStats):
    def __init__(self, infoData, membersData, placing, key=""):
        self.placing = placing
        GuildStats.__init__(self, infoData, membersData, key)

class GuildMember:
    def __init__(self, uuid, role, joinTime, key):
        self.uuid = uuid
        self.ign = getUserInfo.getIGN(uuid)
        self.role = role
        self.joinTimeRaw = joinTime
        self.joinTIme = datetime.fromtimestamp(self.joinTimeRaw).strftime("%I:%M %p on %B %d, %Y")
        self.key = key
    
    def get_stats(self):
        info = requests.get(f"{VOXYLBASE}{VOXYLINFO.format(self.uuid, VOXYLAPI.format(self.key))}").json()
        over = requests.get(f"{VOXYLBASE}{VOXYLOVERALL.format(self.uuid, VOXYLAPI.format(self.key))}").json()
        game = requests.get(f"{VOXYLBASE}{VOXYLGAME.format(self.uuid, VOXYLAPI.format(self.key))}").json()

        if not info["success"] or not over["success"] or not game["success"]:
            return None
        
        return PlayerStats(gen=info, over=over, game=game["stats"])

def get_members(memberList):
    members = {"owner": [], "admin": [], "moderator": [], "member": []}

    for i in memberList:
        members[i["role"].lower()].append(i["uuid"])
    
    return members

class GuildNotFound(Exception):
    pass

class GuildMemberNotFound(Exception):
    pass