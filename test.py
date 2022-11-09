import discord
import os
import asyncio
from discord.ext import commands
import youtube_dl


# DISCORD_TOKEN = os.getenv("TOKEN")
DISCORD_TOKEN = "MTAyNzIwNzgzNzYwNjIyODA1OA.GHrIAk.Sw9RzWZPqznAJb-OfgOfd6S0e5H69HVTKyImCg"
intents = discord.Intents.all()
 
bot = commands.Bot(command_prefix=('!','?'), intents=intents, case_insensitive = True, strip_after_prefix=True)
# bot = commands.Bot(command_prefix=('!','?'), intents=intents)

@bot.event
async def on_ready():
    print(bot.case_insensitive, bot.strip_after_prefix)
    print(bot.command_prefix)
    print(f'{bot.user} has connected to Discord!')
    print(type(bot.commands))
    print(bot.commands)
    
    for command in bot.commands:
        print(command)
    print("Guilds:", bot.guilds[0])

    for i, intent in enumerate(bot.intents):
        print(i,intent)

    print(bot.user)

    for user in bot.users:
        print(user)

    for i, user in enumerate(bot.users):
        print("i ->" , i, "user ->" , user)

@bot.event
async def on_message(message):
    if bot.user == message.author:
        return

    if (bot.get_command(message.content[1:]) != None):
        print("This is a command")
    else:
        if (message.content == "hello"):
            # embed = discord.Embed(title="Hello {0}".format(message.author.name),color=discord.Colour.dark_green())
            # await message.channel.send(embed=embed)
            await message.channel.send("hello sister")
    await bot.process_commands(message)


@bot.command()
async def test(ctx, *args):
    arguments = ','.join(args)
    await ctx.send(f'{len(args)} You passed {arguments}')


@bot.event
async def on_member_join(member):
    embed = discord.Embed(title="Welcome to the server {0}".format(member.name))
    await member.send(embed=embed)

@bot.command(
    brief="Crazy calculation to return pong",
    help="you need some extra help"
)
async def ping(ctx):
    # print(ctx.author, ctx.message.content)
    await ctx.send("pong")

@bot.command(
    name="reminder",
    brief="remind something in certain seconds",
    help="give the command, seconds and the text to remind."
)
async def reminder(ctx,time=None,*,text: str):
    if time == None:
        await ctx.reply("Use the command well, reminder [time] [text]")
    else:
        #this is in seconds
        await asyncio.sleep(int(time))
        embed = discord.Embed(title = 'Reminder!', color = discord.Colour.magenta())
        embed.add_field(name = f"Requested by {ctx.author.name}", value = text)
        await ctx.send(embed = embed)
        asyncio.get_event_loop()


@bot.command(
    name="sh",
    brief="show help commands briefs",
    help="You seriously need some help?"
)
async def show_help(ctx):
    await ctx.send_help()

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

    await voiceChannel.connect()

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
@bot.command
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.send("Currently no audio playing.")

@bot.command
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


bot.run(DISCORD_TOKEN)