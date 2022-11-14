import discord
from discord.ext import commands
import asyncio
import requests
import json
import os
import random
import youtube_dl

#The creation of a bot object, and the constructor of it
bot = commands.Bot(command_prefix=("!","bot "), intents=discord.Intents.all(), strip_after_prefix=True)

#describe the intents

for intent in bot.intents:
    print(intent)


token = "MTAyNzIwNzgzNzYwNjIyODA1OA.GJqsXz.27QF9L_liAZGddLbO_WG2GxHNC24CDs_reiQ9I"

#Explain what is an event and what does it do to the function preparation as a decorator
@bot.event
#Explain why async and 
async def on_ready():
    print(f"{bot.user.name} is ready to use !")

@bot.event
#here the message received as a parameter will be the message that created this event
async def on_message(message):
    if bot.user == message.author:
        return
    
    #Explain difference between == and in str 
    if message.content == "hello":
        await message.reply(f"hello how are you {message.author.name}")

    if "hello" in message.content:
        await message.reply(f"hello how are you {message.author.name}")

    #Declaration needed to specify the bot to await and process the commands
    await bot.process_commands(message)

rules = ["You will not bother anyone.","You will not share personal information.",
"You will help others.","You will follow the rules.",
"You will not write bad words.","You will not profit from this guild."]

@bot.event
#here the member that joined will be added as a parameter once the event is triggered
async def on_member_join(member):
    embed = discord.Embed(title=f"Welcome! Rules of {member.guild.name}", colour=discord.Colour.gold())
    for i, rule in enumerate(rules):
        embed.add_field(name=f"Rule No. {i+1}:", value=rule)
    await member.send(embed=embed)

# Represents the context in which a command is being invoked under.
#This class contains a lot of meta data to help you understand more about the invocation context. 
# This class is not created manually and is instead passed around to commands as the first parameter.

@bot.command(
    name = "ping",
    brief = "crazy calculation to determine an answer",
    help = "returns pong"
)
async def ping(ctx):
    await ctx.reply("pong")

@bot.command(
    name = "remind",
    brief = "crazy calculation to remind an something",
    help = "returns reminder"
)
async def remind(ctx, time, *, args):
    try:
        await asyncio.sleep(int(time))
        await ctx.message.author.send(args)
    except:
        await ctx.send("The time or args are not specified.")

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
    name='join', 
    help='Tells the bot to join the voice channel'
)
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(
    name="play"
)
async def play(ctx,*, url : str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait fot the current playing music to end or use the 'stop' command.")
        return

    voiceChannel = ctx.message.author.voice.channel

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file,"song.mp3")
    try:
        voice.play(discord.FFmpegPCMAudio("/Users/eskrg/Documents/git/discordbot/song.mp3"))
    except FileNotFoundError:
        print("Something weird is going on. ")

@bot.command(
    name="leave"
)
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(
    name= "pause"
)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.send("Currently no audio playing.")

@bot.command(
    name = "resume"
)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@bot.command(
    name = "stop"
)
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

bot.run(token)