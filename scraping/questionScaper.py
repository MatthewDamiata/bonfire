import praw
from tokens import *

def openFile(name):
    f = open(name, "w")
    return f

def scrapeReddit(output):
    user_agent = 'WYR question scaper by /u/matt91rd'
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    for submission in reddit.subreddit("WouldYouRather").hot(limit=1000):
        submission = submission.title
        if('WYR' == submission[0:3] or 'Would you rather' in submission[0:16]):
            output.write(submission.replace('Would you rather', 'WYR') + '\n')

def main():
    f = openFile("output.txt")
    scrapeReddit(f)
    f.close()

if __name__ == '__main__':
    main()