import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import datetime
import tweeter

client = commands.Bot(command_prefix = "zord ")

rules = ["Rule 0: No one will disrespect Xander. This includes banning/kicking/muting/using him aggressively. "]

zds = ["hello", "dob", "date", "ping", "(k)ick", "(b)an", "unban", "h or zords", "(c)lear", "tweet"]

@client.event
async def on_ready():
    print("Xander's Ready!")

@client.command()
async def hello(ctx):
    await ctx.send("S.P.D. Emergency!")
    await ctx.send("Hye, Welcome to Bot Factory! I'm Xander. Pleasure meeting you!")

@client.command()
async def date(ctx):
    await ctx.send("S.P.D. Emergency!")
    await ctx.send(datetime.datetime.now())

@client.command()
async def dob(ctx):
    await ctx.send("S.P.D. Emergency!")
    await ctx.send("I was born on Christmas' Day, 2020")

@client.command(aliases = ['rules'])
async def rule(ctx, *, number):
    await ctx.send("S.P.D. Emergency!")
    await ctx.send(rules[int(number)])

@client.command(aliases = ['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, * , reason = "Reason not provided"):
    await ctx.send("S.P.D. Emergency!")
    await member.send(f"You've been kicked from the Bot Factory. Reason - {reason}")
    await member.kick(reason=reason)

@client.command(aliases = ['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, * , reason = "Reason not provided"):
    await ctx.send("S.P.D. Emergency!")
    await member.send(f"{member.name} has been banned from the Bot Factory. Reason - {reason}")
    await member.ban(reason = reason)

@client.command(aliases = ['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    await ctx.send("S.P.D. Emergency!")
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f"{member_name} has been unbanned!")
            return

    await ctx.send(f"{member} not found")

@client.command(aliases = ['h'])
async def zords(ctx):
    await ctx.send("S.P.D. Emergency!")
    await ctx.send("Call the following zords starting with 'zord ':")
    await ctx.send(zds)

@client.command()
async def ping(ctx):
    await ctx.send("S.P.D. Emergency!")
    await ctx.send(f"My ping time is: {round(client.latency * 1000)} ms")

@client.command(aliases = ['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 2):
       await ctx.channel.purge(limit = amount)
    
# tweet command
@client.command()
async def tweet(ctx, amount = 1):
    await ctx.channel.purge(limit = 1)

    msgs = []
    async for msg in ctx.channel.history(limit = amount):
        msgs.append(msg.content)
    msgs.reverse()

    messages = ''
    for msg in msgs:
        messages = messages + msg + '\n'
    
    tweeter.status_update(messages)
    tweets = tweeter.tweet_s()
    tweet_text = tweeter.tweetText()
    tweet_url = tweeter.tweetURL()
    twitter_username = os.getenv('TWITTER_USERNAME')
    response_channel = os.getenv('RESPONSE_CHANNEL_NAME')

    for DGuild in client.guilds:
        for DChannel in DGuild.text_channels:
            if DChannel.name == f'{response_channel}':

                embed = discord.Embed(title = tweets.user.screen_name, description = tweet_text, colour  = discord.Colour.blue())
                embed.add_field(name = "TWEET ID", value = tweets.id, inline = True)
                embed.add_field(name = "TWEET URL", value = tweet_url, inline = True)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Posted by {ctx.author.name}")
                embed.set_author(name = f'@{twitter_username}', icon_url = client.user.default_avatar_url)
                await DChannel.send(embed = embed)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
