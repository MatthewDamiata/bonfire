import discord
import asyncio
import random
from pymongo import MongoClient
from discord.ext import commands
from discord.utils import get
from prepCommands import * 
from tokens import *

##### BOT ASSETS #####

COLOR = 0xe73a4e

##### BOT CREATIONS & PERMISSIONS #####

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='#', intents=intents)

##### MONGODB CLIENT CONNECTION #####

client = MongoClient("mongodb+srv://bonfire_app:"+DB_PASS+"@cluster0.ctzl1.mongodb.net/?retryWrites=true&w=majority")
db = client.wyr
pos = db.positive
neg = db.negative
pos_ques = db.pos_questions
neg_ques = db.neg_questions
question_pipeline = [
        {"$project": {"option": 1, "_id": 1}},
        {"$sample": {"size": 2}},
    ]

##### COMMANDS #####

@bot.command()
async def dog(ctx):
    "Displays a random dog fact 🐶."
    embedVar = discord.Embed(title="Random Dog Fact", description="🔥 Bonfire", color=COLOR)
    ret = dogPrep()
    embedVar.add_field(name="Fact:", value="🐶 " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def cat(ctx):
    "Displays a random dog fact 🐱."
    embedVar = discord.Embed(title="Random Cat Fact", description="🔥 Bonfire", color=COLOR)
    ret = catPrep()
    embedVar.add_field(name="Fact:", value="🐱 " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def joke(ctx):
    "Displays a random joke 😆."
    embedVar = discord.Embed(title="Random Joke", description="🔥 Bonfire", color=COLOR)
    ret = jokePrep()
    embedVar.add_field(name="Fact:", value="😆 " + ret, inline=False)
    await ctx.send(embed = embedVar)

@bot.command()
async def trivia(ctx):
    "Displays a random trivia question, with the answer in a spoiler 💡."
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
    "Displays a would you rather question. React with 1️⃣ or 2️⃣ to see how many people chose that answer!"
    choice = random.randint(0,1)
    col = neg if choice == 0 else pos
    
    # Query for 2 random options
    randomOptions = list(col.aggregate(question_pipeline))
   
    # If there is no entry for either combination of these options, insert a new document
    if choice == 1:
        color = COLOR
        if pos_ques.find_one({'opt1': randomOptions[0]["option"], 'opt2': randomOptions[1]["option"]}) == None and pos_ques.find_one({'opt1': randomOptions[1]["option"], 'opt2': randomOptions[0]["option"]}) == None:
            pos_ques.insert_one({'opt1': randomOptions[0]["option"], 'opt2': randomOptions[1]["option"], 'votes1': 0, 'votes2': 0})
    else:
        # Embed whether the option is negative or positive into the color
        color = COLOR - 0x1
        if neg_ques.find_one({'opt1': randomOptions[0]["option"], 'opt2': randomOptions[1]["option"]}) == None and neg_ques.find_one({'opt1': randomOptions[1]["option"], 'opt2': randomOptions[0]["option"]}) == None:
            neg_ques.insert_one({'opt1': randomOptions[0]["option"], 'opt2': randomOptions[1]["option"], 'votes1': 0, 'votes2': 0})
    
    # Two options will be guaranteed by pipeline $match
    embedVar = discord.Embed(title="Would You Rather...", description="🔥 Bonfire", color=color)
    valueMessage = ":one: "+ randomOptions[0]["option"] + "\n:two: " + randomOptions[1]["option"]
    embedVar.add_field(name="Options:", value=valueMessage, inline=False)
    message = await ctx.send(embed = embedVar)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

@bot.command()
async def hedbanz(ctx):
    "Like the classic game Hedbanz, it displays an animal which one person has to interrogate others to find out which one they are."
    embedVar = discord.Embed(title="Hedbanz", description="🔥 Bonfire", color=COLOR)
    ret = '||' + hedbanzPrep() + '||'
    embedVar.add_field(name="The animal is (no peeking, guesser!):", value="❓ " + ret, inline=False)
    await ctx.send(embed = embedVar)

#### EVENTS ####

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('#help to start!'))

@bot.event
async def on_reaction_add(reaction, user):
    updateWYR(reaction, user, 1, pos_ques, neg_ques)

@bot.event
async def on_reaction_remove(reaction, user):
    updateWYR(reaction, user, -1, pos_ques, neg_ques)

##### RUN #####

def main():
    print("Bot ready")
    bot.run(AUTH_TOKEN)

if __name__ == '__main__':
    main()