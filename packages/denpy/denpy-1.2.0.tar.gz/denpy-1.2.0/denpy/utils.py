import json
import discord

def get_config_path(__file__) -> str:
    path = __file__.split('\\')
    path.pop(-1)
    path.append('config.json')
    path = '/'.join(path)
    return path

def get_token(__file__) -> str:
    with open(get_config_path(__file__), 'r') as file:
        config = json.load(file)
    return config["token"]

def get_prefix(__file__) -> str:
    with open(get_config_path(__file__), 'r') as file:
        config = json.load(file)
    return config["prefix"]

def convert_ping_to_color(ping: float) -> str:
    ping = round(ping * 1000)
    if ping < 115:
        text = '\033[92m' + str(ping) + '\033[90m ms'
    elif ping < 120:
        text = '\033[90m' + str(ping) + '\033[90m ms'
    elif ping < 130:
        text = '\033[93m' + str(ping) + '\033[90m ms'
    else:
        text = '\033[91m' + str(ping) + '\033[90m ms'
    return text

async def status(bot: discord.Bot, name: str, status: discord.Status, type: discord.ActivityType):
    activity = discord.Activity(type=type, name=name)
    await bot.change_presence(activity=activity, status=status)
