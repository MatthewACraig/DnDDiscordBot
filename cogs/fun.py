from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Responds with Pong!"""
        await ctx.send("Pong!")

    @commands.command(name="roll")
    async def roll(self, ctx):
        """Rolls a 6-sided die."""
        await ctx.send(f"You rolled a {random.randint(1, 6)}!")

    @commands.command(name="roll_d20")
    async def roll_d20(self, ctx):
        """Rolls a 20-sided die."""
        await ctx.send(f"You rolled a {random.randint(1, 20)}!")

    @commands.command(name="flip")
    async def flip(self, ctx):
        """Flips a coin."""
        await ctx.send(random.choices(['Heads', 'Tails', 'Landed on its side'], weights=[499, 499, 2], k=1)[0])

async def setup(bot):
    await bot.add_cog(Fun(bot))