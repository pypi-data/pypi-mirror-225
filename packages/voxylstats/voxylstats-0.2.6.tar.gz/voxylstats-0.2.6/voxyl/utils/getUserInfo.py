import requests
from voxyl.constants import *

def getUUID(ign):
    mojdata = requests.get(f"{MOJBASE}{MOJUUID}{ign}")
    
    if mojdata.status_code != 200:
        raise UnknownPlayer(f"Player not found: '{ign}'")

    mojdata = mojdata.json()
    return mojdata["id"]

def getIGN(uuid):
    mojdata = requests.get(f"{MOJBASE}{MOJIGN}{uuid}")
    
    if mojdata.status_code != 200:
        raise UnknownPlayer(f"Player not found: '{uuid}'")

    mojdata = mojdata.json()
    return mojdata["name"]

def formatUUID(uuid):
    uuidFormated = uuid[0:8] + "-" + uuid[8:12] + "-" + uuid[12:16] + "-" + uuid[16:20] + "-" + uuid[20:]
    return uuidFormated

class UnknownPlayer(Exception):
    pass