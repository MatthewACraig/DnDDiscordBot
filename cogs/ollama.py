# this lets ollama use my GPU because good lord is it faster than my CPU
import os
import logging
import asyncio
from discord.ext import commands
from ollama import generate
import time

# Configure logging
logging.basicConfig(
    filename="ollama_logs.log",  # log file name
    level=logging.INFO,          # log level
    format="%(asctime)s - %(message)s"  # log format
)

# Global variable to track total response time and number of responses
total_response_time = 0
response_count = 0


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
        global total_response_time, response_count

        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Check if the bot is mentioned or "dnd" is in the message content
        if self.bot.user in message.mentions or "dnd" or "class" or "spell" or "attack" in message.content.lower():
            # Remove the mention from the message content (if present)
            user_message = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            # If "dnd" is mentioned but no other content, set a default prompt
            if not user_message.strip():
                user_message = "Tell me something about Dungeons and Dragons."

            # Log that the bot is generating a response
            print(f"Generating a response for: {user_message}")
            start_time = time.time()

            # Run the blocking generate function in a separate thread
            try:
                response = await asyncio.to_thread(generateOllamaResponse, user_message)
                await message.channel.send(response)
                print('Response sent successfully.')

                # Calculate response time
                response_time = time.time() - start_time
                total_response_time += response_time
                response_count += 1
                average_response_time = total_response_time / response_count

                # Log the details
                logging.info(
                    f"Model: wizardlm2:latest | Prompt: {user_message} | Response: {response} | "
                    f"Response Time: {response_time:.2f}s | Average Response Time: {average_response_time:.2f}s"
                )

                # Print the average response time to the console
                print(f"Average Response Time: {average_response_time:.2f}s")

            except Exception as e:
                print(f"Error generating response: {e}")
                await message.channel.send("Sorry, I couldn't process your request.")

        # Allow the bot to process commands (so other cogs still work)
        await self.bot.process_commands(message)


# The setup command
async def setup(bot):
    await bot.add_cog(Ollama(bot))