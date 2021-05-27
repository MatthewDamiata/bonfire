import discord
import asyncio
import random
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from prepCommands import * 
from tokens import *

COLOR = 0xe73a4e
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='#', intents=intents)
client = MongoClient("mongodb+srv://bonfire_app:"+DB_PASS+"@cluster0.ctzl1.mongodb.net/?retryWrites=true&w=majority")
db = client.wyr
pos = db.positive
neg = db.negative
question_pipeline = [
        {"$project": {"option": 1, "_id": 1}},
        {"$sample": {"size": 2}},
    ]

@bot.command()
async def dog(ctx):
    embedVar = discord.Embed(title="Random Dog Fact", description="🔥 Bonfire", color=COLOR)
    ret = dogPrep()
    embedVar.add_field(name="Fact:", value="🐶 " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def cat(ctx):
    embedVar = discord.Embed(title="Random Cat Fact", description="🔥 Bonfire", color=COLOR)
    ret = catPrep()
    embedVar.add_field(name="Fact:", value="🐱 " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def joke(ctx):
    embedVar = discord.Embed(title="Random Joke", description="🔥 Bonfire", color=COLOR)
    ret = jokePrep()
    embedVar.add_field(name="Fact:", value="😆 " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def trivia(ctx):
    embedVar = discord.Embed(title="Random Trivia Question", description="🔥 Bonfire", color=COLOR)
    ret = triviaPrep()
    embedVar.add_field(name="Question:", value="🤔 " + ret[0], inline=False)
    await ctx.send(embed = embedVar)
    embedVarA = discord.Embed(title="Random Trivia Question", description="🔥 Bonfire", color=COLOR)
    answer = '||' + ret[1] + '||'
    embedVarA.add_field(name='Answer', value="💡 " + answer, inline=False)
    await ctx.send(embed = embedVarA)

@bot.command()
async def wyr(ctx):
    choice = random.randint(0,1)
    col = neg if choice == 0 else pos
    embedVar = discord.Embed(title="Would You Rather...", description="🔥 Bonfire", color=COLOR)
    randomOptions = list(col.aggregate(question_pipeline))
    # Two options will be guaranteed by pipeline $match
    valueMessage = ":one: "+ randomOptions[0]["option"] + "\n:two: " + randomOptions[1]["option"]
    embedVar.add_field(name="Options:", value=valueMessage, inline=False)
    message = await ctx.send(embed = embedVar)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

@bot.command()
async def hedbanz(ctx):
    embedVar = discord.Embed(title="Hedbanz", description="🔥 Bonfire", color=COLOR)
    ret = '||' + hedbanzPrep() + '||'
    embedVar.add_field(name="Your object:", value="❓ " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    emoji = reaction.emoji
    # if message not embedded do nothing
    if len(message.embeds) == 0:
        return
    # if message not wyr or if reaction is bot do nothing
    if user.bot or message.embeds[0].title != "Would You Rather...":
        print("no action")
        return
    if emoji == "1️⃣":
        print("1 detected")
    if emoji == "2️⃣":
        print("2 detected")
    else:
        return

@bot.command()
async def commands(ctx):
    await ctx.send('Commands\n' + 'dog: random dog fact\n' + 'cat: random cat fact\n' + 'joke: random joke\n' + 'trivia: random question\n')

bot.run(AUTH_TOKEN)
bot.change_presence(status=discord.Status.idle, activity=discord.Game('#help to start!'))