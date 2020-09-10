import discord as original
from .sync import make_sync

from . import ext



Client = make_sync(original.Client)
Embed = make_sync(original.Embed)
Streaming = make_sync(original.Streaming)