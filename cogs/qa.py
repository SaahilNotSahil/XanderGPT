from discord.ext import commands
from utils import Cache
from qa_engine import QAEngine, add_website_data

cache = Cache()


class QA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, namespace, *, query):
        qae = QAEngine()

        status, response = qae.query_llm(
            query,
            namespace=namespace,
            response_type="trained",
            id="_".join([str(ctx.author.id), str(ctx.guild.id)])
        )

        if status:
            await ctx.send(response)
        else:
            await ctx.send(
                "There was an error running your query. Please try again later."
            )
    
    @commands.command(aliases=["ch"])
    async def clear_history(self, ctx):
        cache.delete(f"qa_history_{ctx.author.id}_{ctx.guild.id}")

        await ctx.send("Chat history cleared successfully!")


class Datastore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def train(self, ctx, namespace, *, url):
        urls = url.split(",")
        urls = [url.strip() for url in urls]

        status, error = await add_website_data(
            urls=urls,
            index_name="xandergpt",
            namespace=namespace
        )

        if status:
            await ctx.send("Website data added successfully!")
        else:
            await ctx.send(f"There was an error adding website data: {error}")


async def setup(bot):
    await bot.add_cog(QA(bot))
    await bot.add_cog(Datastore(bot))
