import praw
import config
import requests
import time
import os
import re

def authenticate():
    print 'Logging in...'
    reddit = praw.Reddit(username=config.username, 
                        password=config.password,
                        client_id=config.client_id,
                        client_secret=config.client_secret,
                        user_agent='Xkcd comic linker v0.1')
    print 'Logged in'
    return reddit

def findNumbers(st):
    global current
    current = requests.get('https://xkcd.com/info.0.json').json()['num']
    return [int(x) for x in re.findall('\\b\\d+\\b', st) if int(x) <= current and int(x) != 404 and str(x)[0] != '0']

def runBot(r):
    for comment in r.subreddit('xkcd').comments(limit=25):
        if len(findNumbers(comment.body)) > 0 and comment.id not in getSavedComments() and comment.author != r.user.me():
            print 'string found'
            getSavedComments().append(comment.id)
            print 'replying to comment ' + comment.id
            getSavedComments().append(comment.id)
            print comment.body
            print findNumbers(comment.body)
            reply = ['[XKCD #{a}](https://xkcd.com/{a})'.format(a=x) for x in findNumbers(comment.body)]
            print reply
            print '\n\n'.join(reply)
            comment.reply('\n\n'.join(reply))


            with open('repliedComments.txt', 'a') as f:
                f.write(comment.id + '\n')
            time.sleep(2)
    print 'sleeping...'
    time.sleep(5)


def getSavedComments():
    if not os.path.isfile('repliedComments.txt'):
        repliedComments = []
    else:
        with open('repliedComments.txt', 'r') as f:
            repliedComments = filter(None, f.read().split('\n'))
    return repliedComments


reddit = authenticate()

def run():
    while True:
        runBot(reddit)

def main():
    try:
        run()
    except KeyboardInterrupt:
        print '\nExiting...'
        exit()
    except:
        print '\nError, retrying...'
        time.sleep(10)
        main()          
main()
