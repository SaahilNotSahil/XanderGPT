# Importing required modules
import discord
import os
import json
from discord import message
from dotenv import load_dotenv
from discord.ext import commands
import datetime
import runCode

# Setting the bot's prefix
def get_prefix(client, message):
    with open("prefix.json", "r") as p:
        prefixes = json.load(p)
    
    return prefixes[str(message.guild.id)]

prefix = get_prefix
client = commands.Bot(command_prefix = prefix)
client.remove_command("help")

rules = ["Rule 0: No one will disrespect Xander. This includes banning/kicking/muting/using him aggressively. "]

coms = [
    "setprefix - Allows you to change the bot' prefix",
    "hello - Says hello and welcomes to the server", 
    "spam - Spams a message specified number of times",
    "dob - Displays the date of birth of the bot", 
    "date - Displays the current date and time", 
    "ping - Displays the ping time or latency of the bot", 
    "dp - Displays the Display Picture of the specified member",
    "rule - Displays the rule at the specified number",
    "kick or k - Kicks the specified member from the server", 
    "ban or b - Bans the specified member from the server", 
    "unban or ub - Unbans the specified member from the server", 
    "help or h - Displays this list of commands", 
    "clear or c - Clears the specified number of messages in the channel, default = 2, use 0 to clear all", 
    "rmchannel or rmc - Removes that channel where the command is run",
    "tweet_reg or tr - Registers the user's tweeter account using his api keys",
    "tweet - Tweets the specified number of previous messages to twitter. You need to have a twitter developer account and the same must be registered with the bot using the tweet_reg or tr command.",
    "ide - Lets you write your code directly on discord and returns the output and errors if any; Has two modes - channel and dm",
    "terminal - Runs your commands on a ubuntu terminal (experimental)"
    ]

@client.event
async def on_ready():
    print("Xander's Ready!")
    
@client.event
async def on_guild_join(guild):
    with open("prefix.json", "r") as p:
        prefixes = json.load(p)

    prefixes[str(guild.id)] = "$"

    with open("prefix.json", "w") as p:
        json.dump(prefixes, p, indent=4)
    
    for channel in guild.text_channels:
        await channel.send(f"Hola! I'm Xander! Thanks for inviting me to {guild.name}.")
        await channel.send(f"My default prefix is {prefixes[str(guild.id)]}.\nUse ```{prefixes[str(guild.id)]}setprefix <prefix>``` to change the prefix.")

@client.event
async def on_guild_remove(guild):
    with open("prefix.json", "r") as p:
        prefixes = json.load(p)

    prefixes.pop(str(guild.id))

    with open("prefix.json", "w") as p:
        json.dump(prefixes, p, indent=4)

@client.command()
async def setprefix(ctx, prefix=""):
    with open("prefix.json", "r") as p:
        prefixes = json.load(p)

    if prefix == "":
        await ctx.send(f"The current prefix is set to {prefixes[str(ctx.guild.id)]}.\nUse ```{prefixes[str(ctx.guild.id)]}setprefix <prefix>``` to change the prefix.")
    else:
        prefixes[str(ctx.guild.id)] = prefix
        with open("prefix.json", "w") as p:
            json.dump(prefixes, p, indent=4)
        await ctx.send(f"Prefix changed successfully to {prefix}")

# Welcomes you to the server
@client.command()
async def hello(ctx):
    for DGuild in client.guilds:
        if DGuild == ctx.guild:
            await ctx.send(f"Hye, Welcome to {DGuild.name}! I'm Xander. Pleasure meeting you!")

@client.command()
async def spam(ctx, *, message="This is a spam"):
    while True:
        await ctx.send(message)
        
# Tells the current date and time
@client.command()
async def date(ctx):
    await ctx.send(datetime.datetime.now())

# Tells the date of birth of Xander bot XD
@client.command()
async def dob(ctx):
    await ctx.send("I was born on Christmas' Day, 2020")

# Displays the rule at the specified index
@client.command(aliases = ['rules'])
async def rule(ctx, *, index=0):
    await ctx.send(rules[int(index)])

# Kicks the mentioned user from the server
@client.command(aliases = ['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, * , reason = "Reason not provided"):
    await member.send(f"You've been kicked from the Bot Factory. Reason - {reason}")
    await member.kick(reasoni = reason)

# Bans the mentioned user from the server
@client.command(aliases = ['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, * , reason = "Reason not provided"):
    await member.send(f"{member.name} has been banned from the Bot Factory. Reason - {reason}")
    await member.ban(reason = reason)

# Unbans the banned user
@client.command(aliases = ['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f"{member_name} has been unbanned!")
            return

    await ctx.send(f"{member} not found")

# Displays help 
@client.command(aliases = ['h'])
async def help(ctx):
    with open("prefix.json", "r") as p:
        prefixes = json.load(p)

    comms = ""
    for com in coms:
        comms = comms + com + '\n'
    embed = discord.Embed(title = "Use the following commands with the prefix " + "'" + prefixes[str(ctx.guild.id)] + "'" + ": ", description = comms, colour = discord.Colour.magenta())
    await ctx.send(embed = embed)

# Tells the ping time or latency of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f"My ping time is: {round(client.latency * 1000)} ms")

# Clears the specified no. of recent messages from the channel 
@client.command(aliases = ['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 2):
    if amount == 0:
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit = amount)

@client.command(aliases = ['rmc'])
@commands.has_permissions(manage_channels = True)
async def rmchannel(ctx):
    await ctx.channel.delete()

# Displays the dp of the mentioned member
@client.command()
async def dp(ctx, member: discord.Member):
    if not member:
        member = ctx.author
    await ctx.send(member.avatar_url)

# Registers the user's twitter account to use with the tweet command 
@client.command(aliases = ['tr'])
async def tweet_reg(ctx):
    with open("twitter_reg.json", "r") as t:
        tweeters = json.load(t)
    t.close()

    regDiscordId = ctx.author.discriminator
    await ctx.author.send("Enter your twitter username: ")
    twitterUsername = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    await ctx.author.send("Enter your twitter consumer key (api key): ")
    consumerKey = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    await ctx.author.send("Enter your twitter consumer secret key (api secret key): ")
    consumerSecret = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    await ctx.author.send("Enter your twitter access key: ")
    accessKey = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    await ctx.author.send("Enter your twitter access secret key: ")
    accessSecret = await client.wait_for('message', check=lambda message: message.author == ctx.author)

    tweeters[str(ctx.guild.id)] = [
        str(regDiscordId),
        str(twitterUsername.content),
        str(consumerKey.content),
        str(consumerSecret.content),
        str(accessKey.content),
        str(accessSecret.content)
    ]

    with open("twitter_reg.json", "w") as t:
        json.dump(tweeters, t, indent=4)
    t.close()

    await ctx.author.send("Twitter credentials registered successfully.")

# Tweets the specified no. of recent messages as a single tweet
@client.command(aliases = ['tw'])
async def tweet(ctx, amount = 1, channelName = 'tweet'):
    await ctx.channel.purge(limit = 1)

    with open("twitterGuildID.txt", "a") as g:
        g.write(str(ctx.guild.id) + '\n')
    g.close()

    msgs = []
    async for msg in ctx.channel.history(limit = amount):
        msgs.append(msg.content)
    msgs.reverse()

    messages = ''
    for msg in msgs:
        messages = messages + msg + '\n'
    
    import tweeter
    tweeter.status_update(messages)
    tweets = tweeter.tweet_s()
    tweet_text = tweets.text
    
    with open("twitter_reg.json", "r") as t:
        tweeters = json.load(t)
    t.close()

    twitter_username = tweeters[str(ctx.guild.id)][1]
    response_channel = channelName
    tweet_url = f"https://twitter.com/{twitter_username}/status/" + str(tweets.id)

    for DChannel in ctx.guild.text_channels:
        if DChannel.name == f'{response_channel}':

            embed = discord.Embed(title = tweets.user.screen_name, description = tweet_text, colour = discord.Colour.blue())
            embed.add_field(name = "TWEET ID", value = tweets.id, inline = True)
            embed.add_field(name = "TWEET URL", value = tweet_url, inline = True)
            embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Posted by {ctx.author.name}")
            embed.set_author(name = f'@{twitter_username}', icon_url = client.user.default_avatar_url)
            await DChannel.send(embed = embed)

@client.command()
async def ide(ctx):
    with open("ideMode.json", "r") as i:
        modes = json.load(i)
    i.close()

    await ctx.send("Select ide mode (channel/dm):")
    ideMode = await client.wait_for('message', check=lambda message: message.author == ctx.author)
    ideMode = ideMode.content

    if ideMode == "channel":
        modes[str(ctx.author.discriminator)] = "channel"
        await ctx.send("Your ide mode is now set to channel.")

    if ideMode == "dm":
        modes[str(ctx.author.discriminator)] = "dm"
        await ctx.send("Your ide mode is now set to dm.")

    with open("ideMode.json", "w") as i:
        json.dump(modes, i, indent=4)
    i.close()

    with open("ideMode.json", "r") as i:
        modes = json.load(i)

    if modes[str(ctx.author.discriminator)] == "channel":
        await ctx.send("What should be the name of your code file (without extension)?")
        filename = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        filename = filename.content

        while True:
            langlist = ["c", "c++", "cpp", "py", "python"]
            await ctx.send("Select a programming language: c, cpp/c++, python/py")
            language = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            lang = language.content

            if lang in langlist:
                break
            else:
                await ctx.send("This programming language is either not recognized or not supported. Please try again.")

        ext = ""
        if lang == "python" or lang == "py":
            ext = "py"
        elif lang == "c":
            ext = "c"
        elif lang == "c++" or lang == "cpp":
            ext = "cpp"

        await ctx.send("Enter your code here (enclosed within three times '`'): ")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content[0:3] == '```' and msg.content[len(msg.content) - 3:] == '```':
            code = msg.content[3:len(msg.content) - 3]
        
        await ctx.send("Type 'run' to run this code.")
        toRun = await client.wait_for('message', check = lambda message: message.author == ctx.author)

        outputs = []
        if toRun.content == "run":
            outputs = runCode.execute(filename, ext, lang, code)
            await ctx.send(f"CompileError:\n{outputs[0]}")
            await ctx.send(f"Output:\n{outputs[1]}")
            await ctx.send(f"RuntimeError:\n{outputs[2]}")

    if modes[str(ctx.author.discriminator)] == "dm":
        await ctx.author.send("What should be the name of your code file (without extension)?")
        filename = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        filename = filename.content

        while True:
            langlist = ["c", "c++", "cpp", "py", "python"]
            await ctx.author.send("Select a programming language: c, cpp/c++, python/py")
            language = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            lang = language.content

            if lang in langlist:
                break
            else:
                await ctx.author.send("This programming language is either not recognized or not supported. Please try again.")

        ext = ""
        if lang == "python" or lang == "py":
            ext = "py"
        elif lang == "c":
            ext = "c"
        elif lang == "c++" or lang == "cpp":
            ext = "cpp"

        await ctx.author.send("Enter your code here (enclosed within three times '`'): ")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content[0:3] == '```' and msg.content[len(msg.content) - 3:] == '```':
            code = msg.content[3:len(msg.content) - 3]
        
        await ctx.author.send("Type 'run' to run this code.")
        toRun = await client.wait_for('message', check = lambda message: message.author == ctx.author)

        outputs = []
        if toRun.content == "run":
            outputs = runCode.execute(filename, ext, lang, code)
            await ctx.author.send(f"CompileError:\n{outputs[0]}")
            await ctx.author.send(f"Output:\n{outputs[1]}")
            await ctx.author.send(f"RuntimeError:\n{outputs[2]}")

    i.close()
    
@client.command(aliases=['term'])
async def terminal(ctx):
    while True:
        await ctx.send(f"{ctx.author}@Xander:~$")
        comm = await client.wait_for('message', check = lambda message: message.author == ctx.author)
        comm = comm.content

        if comm == "exit":
            break
        else:
            import terminal
            outputs = terminal.run(comm)

            if outputs[0] != '':
                await ctx.send(f"{outputs[0]}")

            if outputs[1] != '':
                await ctx.send(f"{outputs[1]}")
                
# Loads the discord token from enviroment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
