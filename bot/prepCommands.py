import requests
import random
import discord
import asyncio
import io
import seaborn as sns
import matplotlib.pyplot as plt
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

def triviaPrep():
    req = requests.get(triviaURL)
    q = req.json()['results'][0]['question'].replace('&quot;', '\"').replace('&#039;', '\'')
    ans = req.json()['results'][0]['correct_answer'].replace('&quot;', '\"').replace('&#039;', '\'')
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

    # If message not embedded do nothing
    if len(message.embeds) == 0:
        return

    # If message not wyr or if reaction is bot do nothing
    if user.bot or message.embeds[0].title != "Would You Rather...":
        return

    color = message.embeds[0].colour.value

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
    
    plotVotes(doc["votes1"], doc["votes2"], doc["opt1"], doc["opt2"])

def plotVotes(votes1, votes2, opt1, opt2):
    sns.set_style("dark")
    percent1 = votes1 / (votes2 + votes1)
    percent2 = votes2 / (votes1 + votes2)

    data_stream = io.BytesIO()
    df = pd.DataFrame({opt1 : [percent1], opt2 : [percent2]})
    ax = df.plot.barh(stacked=True)

    ax.figure.set_size_inches(6, 0.85)
    ax.set_title("Would You Rather...")
    ax.get_legend().remove()
    plt.subplots_adjust(left = 0.05, right = 0.945, bottom = 0.60, top = 0.75)
    plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 100)
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])
    plt.text(0.25, 0.5, str(round(percent1 * 100, 2)) + '%', va = 'center', ha = 'center')
    plt.text(0.75, 0.5, str(round(percent2 * 100, 2)) + '%', va = 'center', ha = 'center')
    plt.show()