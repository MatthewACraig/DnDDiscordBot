from discord.ext import commands
import asyncio

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_commands(self, ctx):
        """Get a list of all commands."""
        commands_list = [command.name for command in self.bot.commands]
        await ctx.send(f"Commands: {', '.join(commands_list)}")

    @commands.command()
    async def help(self, ctx): 
        await ctx.send("Best way to get help is to help yourself - Yoda")
        # wait like 2 seconds
        await asyncio.sleep(2)
        await ctx.send("Just kidding, I am working on a help command.")
        await asyncio.sleep(.5)
        await ctx.send("For now, use the `\\get_commands` command to get a list of all commands.")

async def setup(bot):
    await bot.add_cog(Utility(bot))