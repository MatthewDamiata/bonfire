import requests
import random
import selenium
from selenium import webdriver

dogURL = 'https://dog-api.kinduff.com/api/facts'
catURL = 'https://catfact.ninja/fact'
jokeURL = 'https://official-joke-api.appspot.com/random_joke'
triviaURL = 'https://opentdb.com/api.php?amount=1'
hedbanzURL = 'https://random-word-form.herokuapp.com/random/'
gameGalURL = 'https://www.thegamegal.com/word-generator/'

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

def gameGalPrep():
    driver = webdriver.Chrome()
    driver.get(gameGalURL)
    newWordButton = find_element_by_id('newword-button')
    newWordButton.click()
    gennedWord = find_element_by_id('gennedword')
    print(gennedWord)

gameGalPrep()