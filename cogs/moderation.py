import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['c', 'clr'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: str | int=2):
        if amount == "all":
            await ctx.channel.purge()
        elif amount > 0:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send("Invalid amount specified.")

    @commands.command(aliases=['rmc'])
    @commands.has_permissions(manage_channels=True)
    async def rmchannel(self, ctx):
        await ctx.channel.delete()

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, ctx, member: discord.Member, *, reason="No reason was provided."
    ):
        await member.send(
            f"You've been kicked from {ctx.guild.name}. Reason - {reason}"
        )

        channel = ctx.guild.system_channel
        await channel.send(
            f"{member.mention} has been kicked from this server. Reason - {reason}"
        )

        await member.kick(reason=reason)

    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx, member: discord.Member, *, reason="No reason was provided"
    ):
        await member.send(
            f"You've been banned from {ctx.guild.name}. Reason - {reason}."
        )

        channel = ctx.guild.system_channel
        await channel.send(
            f"{member.mention} has been banned from this server. Reason - {reason}."
        )

        await member.ban(reason=reason)

    @commands.command(aliases=['bl'])
    async def banlist(self, ctx):
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


async def setup(bot):
    await bot.add_cog(Moderation(bot))
