import praw
import requests
import config
import time
import sys
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

def isDebug():
    return 'debug' in sys.argv or '-debug' in sys.argv

def findNumbers(st):
    global current
    current = requests.get('https://xkcd.com/info.0.json').json()['num']
    return [int(x) for x in re.findall('\\b\\d+\\b', st) if int(x) <= current and int(x) != 404 and str(x)[0] != '0']

def runBot(r):
    for comment in r.subreddit('test').comments(limit=25):
        if len(findNumbers(comment.body)) > 0 and comment.id not in getSavedComments() and comment.author != r.user.me():
            print 'string found'
            getSavedComments().append(comment.id)
            print 'replying to comment ' + comment.id
            try:
                print comment.body
                getSavedComments().append(comment.id)
                print findNumbers(comment.body)
                reply = ['[XKCD #{a}](https://xkcd.com/{a})'.format(a=x) for x in findNumbers(comment.body)]
                print reply
                if len(reply) > 3:
                    print "num length > 3, skipping"
                    raise Exception
                commentreply = "{} \n_____\n^^I'm&#32;a&#32;Bot.&#32;|&nbsp;[GitHub](https://github.com/lduck11007/xkcd-reddit-bot)&#32;|&#32;[Contact](https://www.reddit.com/message/compose?to=superduck00711)".format("\n\n".join(reply))
                print commentreply
                if not isDebug():
                    comment.reply(commentreply)
            except:
                print 'Error'
                pass


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
    if isDebug():
        print 'Debug Mode'
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
