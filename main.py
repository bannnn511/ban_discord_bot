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

client = commands.Bot(command_prefix=os.environ.get('PREFIX'))


@client.command()
async def join(ctx):
    isJoined = False
    voice = get(client.voice_clients, guild=ctx.guild)

    bot_voice = ctx.guild.voice_client
    author_voice = ctx.author.voice
    if bot_voice and bot_voice.is_connected():
        if bot_voice.channel != author_voice.channel:
            await voice.move_to(author_voice.channel)
        isJoined = True
    elif author_voice and not bot_voice:  # Author connected but bot not connected
        voice = await author_voice.channel.connect()
        isJoined = True
    elif not author_voice:  # Author not connected
        await ctx.send("Get in a voice channel")

    return isJoined


@client.command()
async def play(ctx, *url):
    if not await join(ctx):
        return

    YDL_OPTIONS = {'format': 'bestaudio',
                   'extractaudio': True,
                   'noplaylist': True,
                   }
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    searchKey = ' '.join(url)
    if not voice.is_playing():
        result = ytVideoSearchLink(searchKey)
        if result is None:
            await ctx.send('Bot cannot find ' + searchKey)
        link = result.get("link")
        title = result.get("title")
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(
                link, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing ' + title + '\n' + link)


# check if the bot is already playing
    else:
        await ctx.send("Bot is playing")
        return


@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()
        await ctx.send("resuming")


@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("paused")


@client.command()
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("skipping")


@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
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


def ytVideoSearchLink(search, limit=1):
    videoSearch = VideosSearch(search, limit=1)
    list = dict(enumerate(videoSearch.result().get("result"))).get(limit-1)
    print(list)
    return list


client.run(os.environ.get('TOKEN'))
