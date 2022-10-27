import random
import requests
import json

import os
import asyncio
import discord
from discord.ext import commands 
import youtube_dl

DISCORD_TOKEN = os.getenv("TOKEN")

#print(DISCORD_TOKEN)

intents = discord.Intents.all()
# intents.messages = True
# intents.guilds = True
bot = commands.Bot(('!','bot '), intents=intents, case_insensitive = True, strip_after_prefix=True)

#bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # test = ""
    # for command in bot.commands:
    #     test = test + " " + str(command)

@bot.command(
    help ="You need some help",
    brief ="It makes a crazy calculation to determing the answer"
)
async def ping(ctx):
    embed = discord.Embed(title="Function Ping", color=discord.Colour.gold())
    embed.add_field(name="pong", value="This is pong")
    await ctx.channel.send(embed=embed)

sadWords = ["sad","depressed","lonely"]

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        await message.channel.send('Hello my brother')

    for word in sadWords:
        if word in message.content:
            embed = discord.Embed(title="Don't be sad my dear friend!", color=discord.Colour.yellow())
            embed.add_field(name="Happy quote :) ", value=get_quote())
            await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    embed = discord.Embed(title="Welcome to the Server {0}!".format(member.name), color=discord.Colour.green())
    test = ""
    for command in bot.commands:
        test = test + "-" + str(command)

    embed.add_field(name="The available commands are: ",value=test) 
    await member.send(embed=embed)

def get_joke():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    json_data = json.loads(response.text)
    joke = json_data['value']
    return joke

def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    json_data = json.loads(response.text)
    rand = random.randint(0,1643)
    quote = json_data[rand]['text']
    return quote

@bot.command(
    name = "quote"
)
async def inspiration(ctx):
    embed = discord.Embed(title="Read this words of wisdom...", color=discord.Colour.red())
    response = get_quote()
    embed.add_field(name="Quote of Today: ", value=response)
    await ctx.channel.send(embed=embed)

@bot.command(
    #name = "chucknorris",
    help = "This gives a Chuck Norris joke",
    brief = "Calculation to determing the Chuck Norris joke."
)
async def joke(ctx):
    embed = discord.Embed(title="Believe it or not", color=discord.Colour.blue(), description="this is a description")
    response = get_joke()
    embed.add_field(name="Joke", value=response, inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(
    name="reminder"
)
async def remmin(ctx,time=None,*, amount: str):
    if time==None:
        await ctx.send("Please insert all the arguements.e.g kb$rem time(in minutes) text")
    else:
        await asyncio.sleep(int(time)*60)
        embed = discord.Embed(title = 'Reminder!', color = discord.Colour.magenta())
        embed.add_field(name = f"Requested by {ctx.author.name}", value = amount , inline=True)
        await ctx.send(embed = embed)
        asyncio.get_event_loop()

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester, volume=0.5):
        super().__init__(source,volume)
        self.requester = requester
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client


        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable='ffmpeg', source=filename))
            # ctx.voice_client.play(filename)
        await ctx.send('**Now playing:** %s' %filename)
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

bot.run(DISCORD_TOKEN)