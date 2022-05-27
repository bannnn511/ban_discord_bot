from time import sleep
from discord import channel, emoji, message
from discord.ext import commands
import discord
from discord.utils import get
from discord import FFmpegPCMAudio
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix=os.environ.get('PREFIX'))


@client.event
async def on_message(message):
    await client.process_commands(message)
    # Ignore messages made by the bot
    if(message.author == client.user):
        return
    if (message.channel.id==975710033692209243):
       await client.get_channel(865902462430871553).send(message.content)


client.run(os.environ.get('TOKEN'))
