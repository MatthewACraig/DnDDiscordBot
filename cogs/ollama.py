# this lets ollama use my GPU because good lord is it faster than my CPU
import os
os.environ["OLLAMA_NUM_THREADS"] = "0"

import asyncio
from discord.ext import commands
from ollama import generate
import time

def generateOllamaResponse(userPrompt):
    """Blocking function to generate a response using Ollama."""
    full_response = ''
    systemPrompt = 'You are a helpful assistant that is an expert in Dungeons and Dragons.' \
                   'You prioritize giving the user information from DnD 5e and the DnD 5e SRD, unless told to grab information from another system.' \
                   'If you do not know the answer, say you do not know.' \
                   'Limit your responses to 1000 characters for now please.' \
                   'Now respond to this message: '

    finalPrompt = f'{systemPrompt}\n\n{userPrompt}'
    for response in generate(model='wizardlm2:latest',  # Replace with your model name
                             prompt=finalPrompt,
                             stream=True):
        full_response += response['response']
    return full_response


class Ollama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return
        
        # Check if the bot is mentioned one of the trigger words
        triggerWords: list = ["dnd", "spell", "spells", "class"]
        if self.bot.user in message.mentions or any(word in message.content.lower() for word in triggerWords):
            # Remove the mention from the message content (if present)
            user_message = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            # If "dnd" is mentioned but no other content, set a default prompt
            if not user_message.strip():
                user_message = "Tell me something about Dungeons and Dragons."

            # Log that the bot is generating a response
            print(f"Generating a response for: {user_message}")
            startTime: time = time.time()
            
            # Run the blocking generate function in a separate thread
            try:
                response = await asyncio.to_thread(generateOllamaResponse, user_message)
                await message.channel.send(response)
                print('Response sent successfully.')
                print(f"Response time: {time.time() - startTime:.2f} seconds")
           
            except Exception as e:
                print(f"Error generating response: {e}")
                await message.channel.send("Sorry, I couldn't process your request.")

        # Allow the bot to process commands (so other cogs still work)
        await self.bot.process_commands(message)


# The setup command
async def setup(bot):
    await bot.add_cog(Ollama(bot))