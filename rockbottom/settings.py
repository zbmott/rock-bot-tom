import os


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
GUILD_NAME = os.environ.get('GUILD_NAME')

try:
    from local_settings import *
except ImportError:
    pass
