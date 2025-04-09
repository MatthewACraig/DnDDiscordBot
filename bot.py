import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# loads our token from our environment variable
load_dotenv()
TOKEN = os.getenv('DND_BOT_PUBLIC_KEY')


# ask ray later why we need this. from my understand grabs the intents we setup ealier in the discord developer portal
intents = discord.Intents.default()
intents.message_content = True

# creates the bot instance and sets the command prefix to !
bot = commands.Bot(command_prefix="\\", intents=intents)

initial_extensions = ['cogs.fun', 'cogs.utility']

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.event
async def setup_hook():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load {extension}: {e}")

bot.run(TOKEN)
