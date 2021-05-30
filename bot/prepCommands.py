import requests
import random
import discord
import asyncio
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
    
    print(doc["opt1"]+ ": " + str(doc["votes1"]))
    print(doc["opt2"]+ ": " + str(doc["votes2"]))