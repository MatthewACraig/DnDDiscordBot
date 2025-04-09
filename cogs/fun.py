from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def roll(self, ctx):
        await ctx.send(f"You rolled a {random.randint(1, 6)}!")

    @commands.command()
    async def roll_d20(self, ctx):
        await ctx.send(f"You rolled a {random.randint(1, 20)}!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
