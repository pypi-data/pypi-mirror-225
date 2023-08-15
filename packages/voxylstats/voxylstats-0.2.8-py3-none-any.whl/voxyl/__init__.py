"""Voxyl API Wrapper

A  simple python wrapper for the Voxyl API

"""


__title__ = 'voxapiwrapper'
__author__ = '_lightninq'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 BWP-Stats'
__version__ = '1.0.0'


from .guildstats import GuildStats
from .leaderboardstats import LevelWeightedLB, TechniqueLB
from .playerstats import PlayerStats
from .utils import *
from .client import Client
