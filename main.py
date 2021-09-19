from discord import channel, emoji, message
from discord.ext import commands
import discord
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os
from dotenv import load_dotenv
import emoji
from youtubesearchpython import VideosSearch

load_dotenv()

client = commands.Bot(command_prefix="$")


@client.command()
async def join(ctx, url):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    print(voice)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    if not voice:
        await ctx.send("Playing ")
        voice = await channel.connect()


@client.command()
async def play(ctx, *url):
    await join(ctx, url)
    YDL_OPTIONS = {'format': 'bestaudio',
                   'extractaudio': True,
                   'noplaylist': True, '--default-search': 'auto'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(ytVideoSearchLink(url), download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')

# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return


@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    print(voice)
    if not voice.is_playing():
        voice.resume()
        await ctx.send("resuming")


@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    print(voice)
    if voice.is_playing():
        voice.pause()
        await ctx.send("paused")


@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    print(voice)
    if voice.is_playing():
        voice.stop()
        await ctx.send("stopping")


@client.command()
async def leave(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnected()


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")


@client.command()
async def search(ctx, *search):
    print(search)
    print(ytVideoSearchLink(search))


@client.event
async def on_ready():
    print('We have looged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    await client.process_commands(message)
    # Ignore messages made by the bot
    if(message.author == client.user):
        return
    if message.content.startswith('hello'):
        await message.channel.send('hi!')
    if message.content.startswith("play"):
        await message.channel.send("What do you want to play?")


@client.event
async def on_reaction_add(reaction, user):
    channelId = reaction.message.channel.id
    Channel = client.get_channel(channelId)
    reaction_emoji = emoji.demojize(reaction.emoji)
    print(reaction_emoji)
    if reaction.message.channel != Channel:
        return
    if (user.id == client.user.id):
        return
    if reaction.emoji == '🏀':
        await Channel.send("sup bitch")


def ytVideoSearchLink(search):
    print(search)
    videoSearch = VideosSearch(''.join(search), limit=1)
    return videoSearch.result()["result"][0]["link"]


client.run(os.environ.get('TOKEN'))
