import discord
from discord.ext import commands,tasks
import random
import os
import youtube_dl
import time
import asyncio
import pickle
from itertools import cycle
import pandas as pd

client=commands.Bot(command_prefix='!',intents=discord.Intents.all())

status=['Jamming out to music!','Eating','Sleeping']

movie=pickle.load(open('movie.pkl', 'rb'))
movies = pd.DataFrame(movie)
cosim = pickle.load(open('cosine.pkl', 'rb'))

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready")

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(cycle(status))))
    
@client.command()
async def play(ctx,url: str):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice_client:
        await ctx.send('Already connected to voice channel')
        return

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    voice_client.play(discord.FFmpegPCMAudio(source='song1.mp3',executable="ffmpeg.exe"))
    # # song_there=os.path.isfile(("song.mp3"))
    # # try:
    # #     if song_there:
    # #         os.remove("song.mp3")
    # # except PermissionError:
    # #     await ctx.send("Press stop to stop current song")
    # #     return
    # channel=ctx.author.voice.channel
    # # vc=discord.utils.get(ctx.guild.voice_channels,name='General')
    # print(discord.utils.get(client.voice_clients,guild=ctx.guild))
    # # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # #     ydl.download([url])
    # # for file in os.listdir("./"):
    # #     if file.endswith(".mp3"):
    # #         os.rename(file, "song.mp3")
    
    # # vc.connect()
    #     # voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    
    # await channel.connect()
    # # voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    # # print((discord.FFmpegPCMAudio(executable="ffmpeg.exe",source="song.mp3")))
    
        
@client.command()
async def leave(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The Bot is not connected to a Voice Channel")
    
@client.command()
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("The audio is not playing")
        
@client.command()
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is playing")
@client.command()
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
@client.command()
# name of func is name of commands
async def ping(ctx):
    await ctx.send(f'Pong!{round(1000*client.latency)}')

@client.command(name='hello',help="gives random msg")
async def hello(ctx):
    responses=["Hi, how are you?","hoping to have a good time with u","you are welcome"]
    await ctx.send(random.choice(responses))    

@client.command(name='input')
async def input(ctx, *args):
    for arg in args:
         await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)

@client.command(name='recommend')
async def recommend(ctx, arg1):
    movie_user_likes = str(arg1)
    movie_index = movies[movies['title'] == movie_user_likes].index[0]
    distances = cosim[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:12]
    for i in movies_list:
        await ctx.send(str(movies.iloc[i[0]].title))
@client.command()
async def server(ctx):
    name=str(ctx.guild.name)
    description=str(ctx.guild.description)
    author=str(ctx.guild.owner)
    icon=str(ctx.guild.icon_url)
    count=str(ctx.guild.member_count)
    id=str(ctx.guild.id)
    region=str(ctx.guild.region)
    
    embed=discord.Embed(
        title=name,
        description=description,
        color=discord.Color.blue()
        
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner",value=author,inline=True)
    embed.add_field(name="Server ID",value=id,inline=True)
    embed.add_field(name="Region",value=region,inline=True)
    
    await ctx.send(embed=embed)
    


@client.command()
#clears x amount of commands
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount)


    
    
client.run('TOKEN')