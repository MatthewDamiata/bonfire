import requests
import os
import random
import discord
import asyncio
import io
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import pandas as pd
from discord.ext import commands
from discord.utils import get
from pymongo import MongoClient
from pymongo import ReturnDocument

dogURL = 'https://dog-api.kinduff.com/api/facts'
catURL = 'https://catfact.ninja/fact'
jokeURL = 'https://official-joke-api.appspot.com/random_joke'
triviaURL = 'https://opentdb.com/api.php?amount=1'
hedbanzURL = 'https://random-word-form.herokuapp.com/random/'

COLOR = 0xe73a4e

def createEmbed(title, description, color, name, value):
    embedVar = discord.Embed(title=title, description=description, color=color)
    embedVar.add_field(name=name, value=value, inline=False)
    return embedVar


def helpPrep():
    ret = '''
            \n
            **#dog** → Sends a dog fact.\n
            **#cat** → Sends a cat fact.\n
            **#joke** → Sends an absolutely hilarious joke.\n
            **#dare** → Sends a dare (truth or dare).\n
            **#truth** → Sends a truth question (truth or dare).\n
            **#trivia** → Sends a trivia question, then another message with the answer in a spoiler.\n
            **#hedbanz** → Sends an animal which everyone can see except one person. That person has to interrogate others to find out what animal they are.\n
            **#wyr** → Sends a Would You Rather question. React to vote on which you would choose. Then Bonfire sends a graph showing what percentage of people chose each option.\n
            **#nhie** → Sends a Never Have I Ever question. React to indicate whether or not you have done the action. Then Bonfire sends a graph showing what percentage of people have done the action.
            '''
    return ret

def triviaPrep():
    req = requests.get(triviaURL)
    q = req.json()['results'][0]['question'].replace('&quot;', '\"').replace('&#039;', '\'').replace('&rsquo;', '\'')
    ans = req.json()['results'][0]['correct_answer'].replace('&quot;', '\"').replace('&#039;', '\'').replace('&rsquo;', '\'')
    return [q, ans]

def dogPrep():
    req = requests.get(dogURL)
    req = req.json()['facts'][0]
    return req

def catPrep():
    req = requests.get(catURL)
    req = req.json()['fact']
    return req

def jokePrep():
    req = requests.get(jokeURL)
    req = req.json()['setup'] + ' ' + req.json()['punchline']
    return req

def hedbanzPrep():
    req = requests.get(hedbanzURL + 'animal')
    req = req.json()[0].capitalize()
    return req

def updateWYR(reaction, user, value, pos_ques, neg_ques):
    message = reaction.message
    emoji = reaction.emoji
    color = message.embeds[0].colour.value

    # If message not embedded do nothing
    if len(message.embeds) == 0:
        return None

    # If message not wyr or if reaction is bot do nothing
    if user.bot or message.embeds[0].title != "Would You Rather..." or color == COLOR + 0x1:
        return None

    col = pos_ques if color == COLOR else neg_ques

    opts = message.embeds[0].fields[0].value.splitlines()
    opt1 = opts[0][6:]
    opt2 = opts[1][6:]

    if emoji == "1️⃣":
        doc = col.find_one_and_update({'opt1': opt1, 'opt2': opt2}, {'$inc': {'votes1': value}}, return_document=ReturnDocument.AFTER)
        if doc == None:
           doc = col.find_one_and_update({'opt1': opt2, 'opt2': opt1}, {'$inc': {'votes2': value}}, return_document=ReturnDocument.AFTER) 
    if emoji == "2️⃣":
        doc = col.find_one_and_update({'opt1': opt1, 'opt2': opt2}, {'$inc': {'votes2': value}}, return_document=ReturnDocument.AFTER)
        if doc == None:
            doc = col.find_one_and_update({'opt1': opt2, 'opt2': opt1}, {'$inc': {'votes1': value}}, return_document=ReturnDocument.AFTER) 
    
    return plotVotes(doc["votes1"], doc["votes2"], doc["opt1"], doc["opt2"])

def setStyles():
    sns.set(rc={'axes.facecolor':'#2f3136', 'figure.facecolor':'#2f3136'})
    mpl.rcParams['text.color'] = '#fffff8'
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = 'DejaVu Sans'

def plotVotes(votes1, votes2, opt1, opt2):
    
    setStyles()

    percent1 = votes1 / (votes2 + votes1)
    percent2 = votes2 / (votes1 + votes2)

    # Instead of saving image to server
    data_stream = io.BytesIO()

    # Plot creation
    df = pd.DataFrame({opt1 : [percent1], opt2 : [percent2]})
    ax = df.plot.barh(stacked=True, color=("blue", "red"))
    ax.figure.set_size_inches(6, 1.5) #0.85
    ax.set_title("Would You Rather...")
    legend = plt.legend(loc="upper center", bbox_to_anchor=(0.5, 0.0), fontsize="small")
    legend.get_frame().set_linewidth(0.0)
    ax.spines["top"].set_color("#2f3136")
    ax.spines["bottom"].set_color("#2f3136")
    ax.spines["left"].set_color("#2f3136")
    ax.spines["right"].set_color("#2f3136")
    plt.subplots_adjust(left = 0.05, right = 0.945, bottom = 0.39, top = 0.75)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])
    plt.text(percent1/2, 0.4, str(round(percent1 * 100)) + '%', va = 'center', ha = 'center')
    plt.text(1 - percent2/2, 0.4, str(round(percent2 * 100)) + '%', va = 'center', ha = 'center')
    plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 100)
    plt.close()

    # Prep for embedding, https://stackoverflow.com/questions/65526991/how-to-embed-images-from-matplotlib-to-discord-py-using-embed-set-image-without
    data_stream.seek(0)
    chart = discord.File(data_stream,filename="wyr.png")

    return chart