# Importing required modules
import os
import json
from dotenv import load_dotenv
from discord.ext import commands

# Setting the bot's prefix
def get_prefix(client, message):
    with open("prefix.json", "r") as p:
        prefixes = json.load(p)
    
    return prefixes[str(message.guild.id)]

prefix = get_prefix
client = commands.Bot(command_prefix = prefix)
client.remove_command("help")

@client.event
async def on_ready():
    print("Xander's Ready!")
    client.load_extension('cogs.commands')
    client.load_extension('cogs.help')

@client.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    '''
        Loads the specified extension or cog

        Required argument: <extension_name>

        Note: Can be used only by the administrators
    '''
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    '''
        Unloads the specified extension or cog

        Required argument: <extension_name>

        Note: Can be used only by the administrators
    '''
    client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    '''
        Reloads the specified extension or cog

        Required argument: <extension_name>

        Note: Can be used only by the administrators
    '''
    client.reload_extension(f'cogs.{extension}')

# Loads the discord token from enviroment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
