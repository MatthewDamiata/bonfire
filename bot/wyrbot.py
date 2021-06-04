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
bot.remove_command('help')

##### MONGODB CLIENT CONNECTION #####

client = MongoClient("mongodb+srv://bonfire_app:"+DB_PASS+"@cluster0.ctzl1.mongodb.net/?retryWrites=true&w=majority")

wyr = client.wyr
tod = client.truth_or_dare
nhieDB = client.nhie

pos = wyr.positive
neg = wyr.negative

pos_ques = wyr.pos_questions
neg_ques = wyr.neg_questions

truth_col = tod.truth
dare_col = tod.dare
nhie_col = nhieDB.opts

question_pipeline = [
    {"$project": {"option": 1, "_id": 1}},
    {"$sample": {"size": 2}},
]
dare_pipeline = [
    {"$project": {"dare_text": 1, "_id": 1}},
    {"$sample": {"size": 1}},
]
truth_pipeline = [
    {"$project": {"truth_text": 1, "_id": 1}},
    {"$sample": {"size": 1}},
]
nhie_pipeline = [
    {"$project": {"nhie_text": 1, "_id": 1}},
    {"$sample": {"size": 1}},
]
##### COMMANDS #####

@bot.command()
async def help(ctx):
    ret = helpPrep()
    embedVar = createEmbed("Help", "🔥 Bonfire", COLOR, "Commands", ret)
    await ctx.send(embed=embedVar)

@bot.command()
async def dog(ctx):
    ret = dogPrep()
    embedVar = createEmbed("Dog Fact", "🔥 Bonfire", COLOR, "Fact:", "🐶 " + ret)
    await ctx.send(embed = embedVar)

@bot.command()
async def cat(ctx):
    ret = catPrep()
    embedVar = createEmbed("Cat Fact", "🔥 Bonfire", COLOR, "Fact:", "🐱 " + ret)
    await ctx.send(embed = embedVar)

@bot.command()
async def joke(ctx):
    ret = jokePrep()
    embedVar = createEmbed("Absolutely Hilarious Joke", "🔥 Bonfire", COLOR, "Fact:", "😆 " + ret)
    await ctx.send(embed = embedVar)

@bot.command()
async def hedbanz(ctx):
    ret = '||' + hedbanzPrep() + '||'
    embedVar = createEmbed("Animal Hedbanz", "🔥 Bonfire", COLOR, "The animal is (no peeking, guesser!):", "❓ " + ret)
    await ctx.send(embed = embedVar)

@bot.command()
async def trivia(ctx):
    # Create and send question
    ret = triviaPrep()
    embedVarQuestion = createEmbed("Trivia Question", "🔥 Bonfire", COLOR, "Question:", "🤔 " + ret[0])
    await ctx.send(embed = embedVarQuestion)

    # Create and send answer
    answer = '||' + ret[1] + '||' # || is a spoiler
    embedVarQuestion = createEmbed("Trivia Question", "🔥 Bonfire", COLOR, "Answer:", "💡 " + answer)
    await ctx.send(embed = embedVarQuestion)

@bot.command()
async def truth(ctx):
    randomTruth = list(truth_col.aggregate(truth_pipeline))
    ret = randomTruth[0]["truth_text"]
    embedVar = createEmbed("Truth or Dare", "🔥 Bonfire", COLOR, "Truth 😲", ret)
    await ctx.send(embed = embedVar)

@bot.command()
async def dare(ctx):
    randomDare = list(dare_col.aggregate(dare_pipeline))
    ret = randomDare[0]["dare_text"]
    embedVar = createEmbed("Truth or Dare", "🔥 Bonfire", COLOR, "Dare 😈", ret)
    await ctx.send(embed = embedVar)

@bot.command()
async def nhie(ctx):
    randomNHIE = list(nhie_col.aggregate(nhie_pipeline))
    ret = randomNHIE[0]["nhie_text"]
    embedVar = createEmbed("Never Have I Ever...", "🔥 Bonfire", COLOR, "NHIE 🤫", "Never have I ever " + ret)
    
    message = await ctx.send(embed = embedVar)
   
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@bot.command()
async def wyr(ctx):
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
    valueMessage = ":one: "+ randomOptions[0]["option"] + "\n:two: " + randomOptions[1]["option"]
    
    embedVar = createEmbed("Would You Rather...", "🔥 Bonfire", color, "Options: (React to vote!)", valueMessage)
    message = await ctx.send(embed = embedVar)
   
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

#### EVENTS ####

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('would you rather | #help'))

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    
    # WYR
    chartWYR = updateWYR(reaction, user, 1, pos_ques, neg_ques)
    if chartWYR is not None:
        embedVar = discord.Embed(title="Voting Results", description="🔥 Bonfire", color=COLOR)
        embedVar.set_image(
            url="attachment://wyr.png"
        )
        opts = reaction.message.embeds[0].fields[0].value.splitlines()
        opt1 = opts[0][6:]
        opt2 = opts[1][6:]
        newEmbed = discord.Embed(title="Would You Rather...", description="🔥 Bonfire", color=COLOR + 0x1)
        valueMessage = ":one: "+ opt1 + "\n:two: " + opt2
        newEmbed.add_field(name="Options: (React to vote!)", value=valueMessage, inline=False)

        await reaction.message.edit(embed = newEmbed)
        await channel.send(embed = embedVar, file = chartWYR)
    
    # NHIE
    chartNHIE = updateNHIE(reaction, user, nhie_col)
    if chartNHIE is not None:
        embedVar = discord.Embed(title="NHIE Results", description="🔥 Bonfire", color=COLOR)
        embedVar.set_image(
            url="attachment://nhie.png"
        )
        newEmbed = discord.Embed(title="Never Have I Ever...", description="🔥 Bonfire", color=COLOR + 0x1)
        valueMessage = "Never have I ever " + reaction.message.embeds[0].fields[0].value[18:]
        newEmbed.add_field(name="NHIE 🤫", value=valueMessage, inline=False)

        await reaction.message.edit(embed = newEmbed)
        await channel.send(embed = embedVar, file = chartNHIE)

@bot.event
async def on_reaction_remove(reaction, user):
    updateWYR(reaction, user, -1, pos_ques, neg_ques)

##### RUN #####

def main():
    print("Bot ready")
    bot.run(AUTH_TOKEN)

if __name__ == '__main__':
    main()