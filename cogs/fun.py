import random
import time

from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        choices = ['Heads', 'Tails']

        await ctx.send(f'{random.choice(choices)}')

    @commands.command(aliases=['die'])
    async def dieroll(self, ctx):
        await ctx.send(f'{random.randint(1, 6)}')

    @commands.command()
    async def timer(self, ctx, amount, *, message=""):
        Time = amount.split(':')
        hr = int(Time[0])
        min = int(Time[1])
        sec = int(Time[2])

        msg = await ctx.send(f"Time remaining: 0{hr}:{min}:{sec}")

        while True:
            time.sleep(0.7)
            sec -= 1

            if sec < 0:
                sec = 59
                min -= 1

            if min < 0:
                min = 59
                hr -= 1

            if sec < 10 and min < 10:
                await msg.edit(content=f"Time remaining: 0{hr}:0{min}:0{sec}")

            elif sec < 10 and min >= 10:
                await msg.edit(content=f"Time remaining: 0{hr}:{min}:0{sec}")

            elif sec >= 10 and min < 10:
                await msg.edit(content=f"Time remaining: 0{hr}:0{min}:{sec}")

            elif sec >= 10 and min >= 10:
                await msg.edit(content=f"Time remaining: 0{hr}:{min}:{sec}")

            if hr == 0 and min == 0 and sec == 0:
                time.sleep(0.5)
                await msg.delete()

                await ctx.send(f"{ctx.author.mention} Timer expired.")

                if message != "":
                    time.sleep(1)
                    await ctx.send(message)

                break


async def setup(bot):
    await bot.add_cog(Fun(bot))
