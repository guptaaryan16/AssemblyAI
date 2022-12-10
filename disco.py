import discord
from discord.ext import commands,tasks
from discord.ext.audiorec import NativeVoiceClient
import random

client=commands.Bot(command_prefix='!',intents=discord.Intents.all())

status=['Jamming out to music!','Eating','Sleeping']

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def join(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect(cls=NativeVoiceClient)
    await ctx.invoke(client.get_command('rec'))

@client.command()
async def rec(ctx):
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)

@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    name = str(random.randint(000000, 999999))
    with open(f'{name}.wav', 'wb') as f:
        f.write(wav_bytes)
    await ctx.voice_client.disconnect()
        
@client.command()
async def leave(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The Bot is not connected to a Voice Channel")      

@client.command(name='input')
async def input(ctx, *args):
    for arg in args:
         await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
    print(ctx.author)
    print(ctx.message)
    print(ctx.guild)
    

@client.command()
#clears x amount of commands
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount)


TOKEN=""    
    
client.run(TOKEN)