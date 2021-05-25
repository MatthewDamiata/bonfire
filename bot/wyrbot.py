import discord
import asyncio
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from prepCommands import * 
from tokens import *

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)

client = MongoClient("mongodb+srv://bonfire_app:"+DB_PASS+"@cluster0.ctzl1.mongodb.net/wyr?retryWrites=true&w=majority")
col = client.positive

@bot.command()
async def dog(ctx):
    embedVar = discord.Embed(title="Random Dog Fact", description="Bonfire", color=0x00ff00)
    ret = dogPrep()
    embedVar.add_field(name="Fact:", value=ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def cat(ctx):
    embedVar = discord.Embed(title="Random Cat Fact", description="Bonfire", color=0x00ff00)
    ret = catPrep()
    embedVar.add_field(name="Fact:", value=ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def joke(ctx):
    embedVar = discord.Embed(title="Random Joke", description="Bonfire", color=0x00ff00)
    ret = jokePrep()
    embedVar.add_field(name="Fact:", value=ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def trivia(ctx):
    embedVar = discord.Embed(title="Random Trivia Question", description="Bonfire", color=0x00ff00)
    ret = triviaPrep()
    embedVar.add_field(name="Question:", value=ret[0], inline=False)
    await ctx.send(embed = embedVar)
    embedVarA = discord.Embed(title="Random Trivia Question", description="Bonfire", color=0x00ff00)
    answer = '||' + ret[1] + '||'
    embedVarA.add_field(name='Answer', value=answer, inline=False)
    await ctx.send(embed = embedVarA)

@bot.command()
async def dbtest(ctx):
    temp = col.collection.find({})
    print(temp)
    for x in temp:
        await ctx.send(x)

@bot.command()
async def commands(ctx):
    await ctx.send('Commands\n' + 'dog: random dog fact\n' + 'cat: random cat fact\n' + 'joke: random joke\n' + 'trivia: random question\n')

bot.run(AUTH_TOKEN)