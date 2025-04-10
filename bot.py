import os
import discord
from discord.ext import commands

# loads our token from our environment variable
TOKEN = os.getenv('DND_BOT_PUBLIC_KEY')


# ask ray later why we need this. from my understanding it grabs the intents we setup ealier in the discord developer portal
intents = discord.Intents.default()
intents.message_content = True

# creates the bot instance and sets the command prefix to /
bot = commands.Bot(command_prefix="\\", intents=intents, help_command=None)


# this is where we add our extensions (cogs) to the bot to be loaded in the setup_hook function
initial_extensions = ['cogs.fun', 'cogs.utility', 'cogs.ollama']

# this is the main function that runs when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

# this is where we load our cogs
@bot.event
async def setup_hook():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load {extension}: {e}")

# funny line that actually starts bot
bot.run(TOKEN)
