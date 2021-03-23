import discord
from discord.ext import commands
import json
import datetime
import random
import redditPosts

class Greetings(commands.Cog):
    '''
        Commands to greet you
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("prefix.json", "r") as p:
            prefixes = json.load(p)
        p.close()

        prefixes[str(guild.id)] = "$"

        with open("prefix.json", "w") as p:
            json.dump(prefixes, p, indent=4)
        p.close()

        channel = guild.system_channel
        
        if channel is not None:
                await channel.send(f"Hola! I'm Xander! Thanks for inviting me to {guild.name}.")
                await channel.send(f"My default prefix is {prefixes[str(guild.id)]}.\nUse ```{prefixes[str(guild.id)]}setprefix <prefix>``` to change the prefix.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"Welcome {member.mention} to {member.guild.name}!")

    @commands.command()
    async def hello(self, ctx):
        '''
            Says hello

            Required arguments: None
        '''
        await ctx.send(f"Hello, {ctx.author.mention}! I'm Xander, nice to meet you :smile:")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("prefix.json", "r") as p:
            prefixes = json.load(p)

        prefixes.pop(str(guild.id))

        with open("prefix.json", "w") as p:
            json.dump(prefixes, p, indent=4)

class Moderation(commands.Cog):
    '''
        Some moderation commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['c', 'clr'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 2):
        '''
            Clears the specified amount of messages

            Required arguments: <amount_of_messages_to_be_deleted>

            Note: Can be used only by the members having the permission to manage messages
        '''
        if amount == 0:
            await ctx.channel.purge()
        elif amount > 0:
            await ctx.channel.purge(limit = amount)
        else:
            await ctx.send("Invalid amount specified.")

    @commands.command(aliases = ['rmc'])
    @commands.has_permissions(manage_channels = True)
    async def rmchannel(self, ctx):
        '''
            Removes the current channel

            Required arguments: None

            Note: Can be used only by the moderators
        '''
        await ctx.channel.delete()

    @commands.command(aliases = ['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = "No reason was provided."):
        '''
            Kicks the specified member from the server

            Required arguments: <mention_the_member_to_be_kicked>

            Note: Can be used only by the moderators
        '''
        await member.send(f"You've been kicked from {ctx.guild.name}. Reason - {reason}")

        channel = ctx.guild.system_channel
        await channel.send(f"{member.mention} has been kicked from this server. Reason - {reason}")

        await member.kick(reason = reason)
        
    @commands.command(aliases = ['b'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = "No reason was provided"):
        '''
            Bans the specified member from the server

            Required arguments: <mention_the_member_to_be_banned>

            Note: Can be used only by the moderators
        '''
        await member.send(f"You've been banned from {ctx.guild.name}. Reason - {reason}.")

        channel = ctx.guild.system_channel
        await channel.send(f"{member.mention} has been banned from this server. Reason - {reason}.")

        await member.ban(reason = reason)
    
    @commands.command(aliases = ['bl'])
    async def banlist(self, ctx):
        '''
            Retrieves and sends the list of banned members of the server

            Required arguments: None
        '''
        banned_users = await ctx.guild.bans()

        Users = []
        for banned_entry in banned_users:
            User = str(banned_entry.user.name) + '#' + str(banned_entry.user.discriminator)
            Users.append(User)

        await ctx.send('\n'.join(bannedUser for bannedUser in Users))

    @commands.command(aliases = ['ub'])
    @commands.has_permissions(ban_members = True)
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

    @commands.command()
    async def setprefix(self, ctx, *, prefix = ""):
        '''
            Sets the specified bot prefix for the server. Prints the current prefix if no prefix is specified

            Optional parameters: <new_prefix>
        '''
        with open("prefix.json", "r") as p:
            prefixes = json.load(p)

        if prefix == "":
            await ctx.send(f"The current prefix is set to {prefixes[str(ctx.guild.id)]}\nUse ```{prefixes[str(ctx.guild.id)]}setprefix <prefix>``` to change the prefix.")
        else:
            prefixes[str(ctx.guild.id)] = prefix
            with open("prefix.json", "w") as p:
                json.dump(prefixes, p, indent=4)
            await ctx.send(f"Prefix changed successfully to {prefix}")

        p.close()
    
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

    @commands.command(aliases = ['dt'])
    async def datetime(self, ctx):
        '''
            Tells the current date and time of the server where the bot is hosted

            Required arguments: None
        '''
        await ctx.send(datetime.datetime.now())

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
    async def meme(self, ctx, *, subreddit = "memes"):
        '''
            Sends a random meme from the specified subreddit. Defaults to "memes"

            Optional parameters: <desired_subreddit>
        '''
        await redditPosts.reddit(subreddit, ctx.channel)

    @commands.command()
    async def spam(self, ctx, amount = 100, msg = "This is a spam"):
        '''
            Spams the given message specified number of times. Defaults to 100 times "This is a spam"

            Optional parameters: <amount> <message>
        '''
        for i in range(amount):
            await ctx.send(msg)

    @commands.command(aliases = ['flip', 'coin'])
    async def coinflip(self, ctx):
        '''
            Flips a coin

            Required arguments: None
        '''
        choices = ['Heads', 'Tails']

        await ctx.send(f'{choices[random.randint(0, 1)]}')

    @commands.command(aliases = ['die'])
    async def dieroll(self, ctx):
        '''
            Rolls a die

            Required arguments: None
        '''
        await ctx.send(f'{random.randint(1, 6)}')
        
def setup(bot):
    bot.add_cog(Greetings(bot))
    bot.add_cog(Moderation(bot))
    bot.add_cog(Settings(bot))
    bot.add_cog(Fun(bot))
