import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = "!")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0x6535c4)
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    try:
        embed=discord.Embed(title="Bot Disconnected", description="Taskbot has been shut down by " + ctx.author.name, color=discord.Color.blue())
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
    await ctx.bot.logout()

@client.command()
@commands.is_owner()
async def reloadcogs(ctx):
    for f in os.listdir("./cogs"):
    	if f.endswith(".py"):
    		client.unload_extension("cogs." + f[:-3])
    for f in os.listdir("./cogs"):
    	if f.endswith(".py"):
    		client.load_extension("cogs." + f[:-3])

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension("cogs." + f[:-3])

client.run("TOKEN HERE")
