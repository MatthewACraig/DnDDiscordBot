from discord.ext import commands
import os
import sys

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")  # Command is named "restart"
    @commands.is_owner()  # Restrict this command to the bot owner
    async def restart(self, ctx):
        """Command to restart the bot."""
        await ctx.send("Restarting bot...")
        await self.bot.close()  # Gracefully close the bot
        # Restart the bot process with the correct file path
        python = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')
        if os.path.exists(python):
            os.execv(python, [python, os.path.abspath(sys.argv[0])])
        else:
            await ctx.send("Could not restart: .venv Python not found.")
        await ctx.send("Bot restarted.")

async def setup(bot):
    await bot.add_cog(Utility(bot))