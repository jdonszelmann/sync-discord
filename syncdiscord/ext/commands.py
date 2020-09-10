from discord.ext import commands as originalcommands
from ..sync import make_sync

Bot = make_sync(originalcommands.Bot)