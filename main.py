from discord import channel, emoji, message
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
import emoji

load_dotenv()

client = commands.Bot(command_prefix='.')

TEXT_CHANNEL_ID = int(os.environ.get('TEXT_CHANNEL_ID'))


@client.event
async def on_ready():
    print('We have looged in as {0.user}'.format(client))
    Channel = client.get_channel(TEXT_CHANNEL_ID)
    text = "Welcome"
    Moji = await Channel.send(text)
    await Moji.add_reaction('🏀')


@client.event
async def on_message(message):
    # Ignore messages made by the bot
    if(message.author == client.user):
        return
    if message.content.startswith('hello'):
        await message.channel.send('hi!')
    if message.content.startswith("play"):
        await message.channel.send("What do you want to play?")


@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(TEXT_CHANNEL_ID)
    reaction_emoji = emoji.demojize(reaction.emoji)
    print(reaction_emoji)
    if reaction.message.channel != Channel:
        return
    if (user.id == client.user.id):
        return
    if reaction.emoji == '🏀':
        await Channel.send("sup bitch")

client.run(os.environ.get('TOKEN'))
