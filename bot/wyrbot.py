import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from prepCommands import * 
from tokens import *

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def getonidiot(ctx, arg):
    jah = 0
    members = ctx.guild.members
    for member in members:
        if member.name == arg:
            jah = member
    while(True):
        await ctx.send(jah.mention)
        await asyncio.sleep(5)

@bot.command()
async def dog(ctx):
    embedVar = discord.Embed(title="Random Dog Fact", description="WYRBot", color=0x00ff00)
    ret = dogPrep()
    embedVar.add_field(name="Fact:", value=ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def cat(ctx):
    embedVar = discord.Embed(title="Random Cat Fact", description="WYRBot", color=0x00ff00)
    ret = catPrep()
    embedVar.add_field(name="Fact:", value=ret, inline=False)
    await ctx.send(ret)

@bot.command()
async def joke(ctx):
    embedVar = discord.Embed(title="Random Joke", description="WYRBot", color=0x00ff00)
    ret = jokePrep()
    embedVar.add_field(name="Fact:", value=ret, inline=False)
    await ctx.send(ret)

@bot.command()
async def trivia(ctx):
    ret = triviaPrep()
    await ctx.send(ret[0])
    await ctx.send('||' + ret[1] + '||')

@bot.command()
async def commands(ctx):
    await ctx.send('Commands\n' + 'dog: random dog fact\n' + 'cat: random cat fact\n' + 'joke: random joke\n' + 'trivia: random question\n')

bot.run(AUTH_TOKEN)