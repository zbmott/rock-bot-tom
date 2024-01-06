import os


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
GUILD_NAME = os.environ.get('GUILD_NAME')

BNET_CLIENT_ID = os.environ.get('BNET_CLIENT_ID')
BNET_SECRET = os.environ.get('BNET_SECRET')

try:
    from local_settings import *
except ImportError:
    pass
