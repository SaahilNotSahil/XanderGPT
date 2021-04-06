import discord
from discord.ext import commands
import datetime
import random
import time
import aiohttp
from discord.ext.commands.core import command
from db import mongo_setup
from db.prefixes import Prefix
from db.links import Link
from googlesearch import search
import googletrans

mongo_setup.global_init()


def getprefix(msg) -> Prefix:
    for pref in Prefix.objects:
        if pref._guild_id == str(msg.guild.id):
            return pref._prefix


class Greetings(commands.Cog):
    '''
        Commands to greet you
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> Prefix:
        pref = Prefix()
        pref._guild_name = guild.name
        pref._guild_id = str(guild.id)
        pref._prefix = "$"
        pref.save()

        channel = guild.system_channel

        if channel is not None:
            await channel.send(f"Hola! I'm Xander! Thanks for inviting me to {guild.name}.")
            await channel.send("My default prefix is $.\nUse ```$setprefix <prefix>``` to change the prefix.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel

        await channel.send(f"Welcome {member.mention} to {member.guild.name}! We hope you enjoy your stay :slight_smile:")

    @commands.command()
    async def hello(self, ctx):
        '''
            Says hello

            Required arguments: None
        '''
        await ctx.send(f"Hello, {ctx.author.mention}! I'm Xander, nice to meet you :smile:")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel

        await channel.send(f"{member.display_name} has left {member.guild.name}. Hope they'll come back :slight_smile:")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild) -> Prefix:
        Prefix.objects(_guild_id=str(guild.id)).delete()


class Moderation(commands.Cog):
    '''
        Some moderation commands
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['c', 'clr'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        '''
            Clears the specified amount of messages

            Required arguments: <amount_of_messages_to_be_deleted>

            Note: Can be used only by the members having the permission to manage messages
        '''
        if amount == 0:
            await ctx.channel.purge()
        elif amount > 0:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send("Invalid amount specified.")

    @commands.command(aliases=['rmc'])
    @commands.has_permissions(manage_channels=True)
    async def rmchannel(self, ctx):
        '''
            Removes the current channel

            Required arguments: None

            Note: Can be used only by the moderators
        '''
        await ctx.channel.delete()

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason was provided."):
        '''
            Kicks the specified member from the server

            Required arguments: <mention_the_member_to_be_kicked>

            Note: Can be used only by the moderators
        '''
        await member.send(f"You've been kicked from {ctx.guild.name}. Reason - {reason}")

        channel = ctx.guild.system_channel
        await channel.send(f"{member.mention} has been kicked from this server. Reason - {reason}")

        await member.kick(reason=reason)

    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason was provided"):
        '''
            Bans the specified member from the server

            Required arguments: <mention_the_member_to_be_banned>

            Note: Can be used only by the moderators
        '''
        await member.send(f"You've been banned from {ctx.guild.name}. Reason - {reason}.")

        channel = ctx.guild.system_channel
        await channel.send(f"{member.mention} has been banned from this server. Reason - {reason}.")

        await member.ban(reason=reason)

    @commands.command(aliases=['bl'])
    async def banlist(self, ctx):
        '''
            Retrieves and sends the list of banned members of the server

            Required arguments: None
        '''
        banned_users = await ctx.guild.bans()

        Users = []
        for banned_entry in banned_users:
            User = str(banned_entry.user.name) + '#' + \
                str(banned_entry.user.discriminator)
            Users.append(User)

        await ctx.send('\n'.join(bannedUser for bannedUser in Users))

    @commands.command(aliases=['ub'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        '''
            Unbans the specified member from the server

            Required arguments: <username>#<discriminator>

            Note: Can be used only by the moderators
        '''
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split("#")

        channel = ctx.guild.system_channel
        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await channel.send(f"{member_name} has been unbanned!")
                return

        await ctx.send(f"{member} not found.")


class Settings(commands.Cog):
    '''
        Some bot settings
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.split()[0] == "prefix":
            if msg.mentions[0] == self.bot.user:
                await msg.channel.send(f"My prefix is {getprefix(msg)}")

    @commands.command()
    async def setprefix(self, ctx, *, prefix) -> Prefix:
        '''
            Sets the specified bot prefix for the server. 

            Optional parameters: <new_prefix>
        '''

        for pref in Prefix.objects:
            if pref._guild_id == str(ctx.guild.id):
                pref._prefix = prefix
                pref.save()

        await ctx.send("Prefix successfully changed to {}".format(prefix))

    @commands.command()
    async def ping(self, ctx):
        '''
            Tells the latency or ping of the bot

            Required arguments: None
        '''
        await ctx.send(f"My ping time is: {round(self.bot.latency * 1000)} ms")

    @commands.command()
    async def dob(self, ctx):
        '''
            Tells the date of birth of Xander

            Required arguments: None
        '''
        await ctx.send("I was born on Christmas' Day, 2020")

    @commands.command(aliases=['dt'])
    async def datetime(self, ctx):
        '''
            Tells the current date and time of the server where the bot is hosted

            Required arguments: None
        '''
        await ctx.send(datetime.datetime.now())

    @commands.command(aliases=['git'])
    async def github(self, ctx):
        '''
            Fetches the link to the bot's github repo

            Required arguments: None 
        '''
        await ctx.send("https://github.com/XanderWatson/xander-bot")


class Fun(commands.Cog):
    '''
        Just for fun commands
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dp(self, ctx, member: discord.Member):
        '''
            Displays the display picture of the tagged member

            Required arguments: <mention>
        '''
        if not member:
            member = ctx.author

        await ctx.send(member.avatar_url)

    @commands.command()
    async def meme(self, ctx, *, subreddit="memes"):
        '''
            Sends a random meme from the specified subreddit. Defaults to "memes"

            Optional parameters: <desired_subreddit>
        '''
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://www.reddit.com/r/{subreddit}.json") as r:
                memes = await r.json()
                embed = discord.Embed(
                    color=discord.Color.blue(),
                )
                embed.set_image(
                    url=memes["data"]["children"][random.randint(1, 25)]["data"]["url"])
                embed.set_footer(text=f"Meme requested by {ctx.author}")
                await ctx.send(embed=embed)

    @commands.command()
    async def spam(self, ctx, amount=100, *, msg="This is a spam"):
        '''
            Spams the given message specified number of times. Defaults to 100 times "This is a spam"

            Optional parameters: <amount> <message>
        '''
        for i in range(amount):
            await ctx.send(msg)
            time.sleep(0.2)

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        '''
            Flips a coin

            Required arguments: None
        '''
        choices = ['Heads', 'Tails']

        await ctx.send(f'{choices[random.randint(0, 1)]}')

    @commands.command(aliases=['die'])
    async def dieroll(self, ctx):
        '''
            Rolls a die

            Required arguments: None
        '''
        await ctx.send(f'{random.randint(1, 6)}')

    @commands.command(aliases=['google'])
    async def search(self, ctx, *, query):
        '''
            Makes a google search and returns the top 10 results

            Required arguments: <search_query>
        '''
        results = []
        for s in search(query, tld='co.in', lang='en', safe='off', num=10, start=0, stop=10, pause=2):
            results.append(s)

        result = '\n'.join(results)

        await ctx.send(f"```{result}```")

    @commands.command(aliases=['tr', 'trans', 'ts', 't'])
    async def translt(self, ctx, src, to, *, text):
        '''
            Translates the given text to the desired language

            Required arguments: <src_lang> <dest_lang> <text_to_translate>
        '''
        translator = googletrans.Translator()

        translated = translator.translate(text=text, dest=to, src=src)

        await ctx.send(translated.text)

    @commands.command(aliases=['tc'])
    async def lingua(self, ctx, lang1, lang2, member: discord.Member):
        translator = googletrans.Translator()

        while True:
            await ctx.send(f"{translator.translate('It is your turn', dest=lang1, src='en').text} {ctx.author.mention}")
            reply1 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            reply1 = reply1.content
            await ctx.send(translator.translate(text=reply1, dest=lang2, src=lang1).text)

            await ctx.send(f"{translator.translate('It is your turn', dest=lang2, src='en').text} {member.mention}")
            reply2 = await self.bot.wait_for('message', check=lambda message: message.author == member)
            reply2 = reply2.content
            await ctx.send(translator.translate(text=reply2, dest=lang1, src=lang2).text)

            if translator.translate(text=reply2, dest='en', src='en').text == "STOPPY" or translator.translate(text=reply1, dest='en', src='en').text == "STOPPY":
                break

    @commands.command(aliases=['ll'])
    async def langs(self, ctx):
        langlist = []
        for j in googletrans.LANGUAGES:
            langlist.append(f"{j}: {googletrans.LANGUAGES[j]}")

        lang = '\n'.join(l for l in langlist)
        await ctx.send(f"```{lang}```")


class College(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def rl(branch):
        l = Link()
        l._branch = branch
        l.save()

    @commands.command(aliases=['cl'])
    async def reglink(self, ctx, course, link="") -> Link:
        courses = ["ics", "em", "emtut", "maths",
                   "mathstut", "icslab1", "icslab2", "icslab3"]

        await ctx.send("Enter you branch code:")
        branch = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        branch = branch.content.upper()

        self.rl(branch)

        for l in Link.objects:
            if l._branch == branch:
                l.courses[courses.index(course.content)] = link
                l.save()

        await ctx.send(f"Link for {course} added/updated successfully")

    @commands.command()
    async def getlink(self, ctx, course):
        courses = ["ics", "em", "emtut", "maths",
                   "mathstut", "icslab1", "icslab2", "icslab3"]

        await ctx.send("Enter you branch code:")
        branch = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        branch = branch.content.upper()

        for l in Link.objects:
            if l._branch == branch:
                await ctx.send(f"{l.courses[courses.index(course.content)]}")


def setup(bot):
    bot.add_cog(Greetings(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Settings(bot))
    bot.add_cog(Fun(bot))
    bot.add_cog(College(bot))
