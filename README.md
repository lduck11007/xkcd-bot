# xkcd-reddit-bot
Scans through the r/xkcd subreddit, replying to comments with links to certain comics when mentioned. Currently in use by u/XkcdImageBot.

## Requirements
* [Praw](https://github.com/praw-dev/praw), Python Reddit API Wrapper
* [Requests](https://github.com/requests/requests), Python HTTP Requests

## Usage
To use the bot normally:

    python main.py
    
To use the bot in debugging mode: (displays normal outputs but does not comment)

    python main.py -debug
