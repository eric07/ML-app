from twitter import *
import json
from Parse import Parse
from datetime import datetime
import time
import requests
from Model import Model
import sys


class Fetch():
    t = None
    def __init__(self):
        self.parse = Parse()
        # Authorise my request using OAuth
        self.t = Twitter(auth=OAuth("2999654973-YS9XG2UdzWDNJhapOjAUDHjrv5wgG3az3MZ5JfF", "NlP0PWQPJv1Z0lPsH6xv3bb7jw3Aos5xD18ni3ODuDZME", "p6yoZBcF9NnteTV67YbVRwcis", "nY0Q4ugFlef0AtlRTaXptshXxJNGymxFgn4KzaeF77UXlMkRuq"))
        self.tweets = []
        # Define target account and fetch tweet
        self.t.statuses.user_timeline(screen_name="premierleague", count=1, exclude_replies=True, include_rts=False) 
        tweets = self.t.statuses.user_timeline(screen_name="premierleague", count=1, exclude_replies=True, include_rts=False) 
        for i in xrange(len(tweets)):
            self.tweets.append(self.parse.parseOne(tweets[i]))
            # print tweets[i]
        # print tweets[0]


if __name__ == '__main__':
    fetch = Fetch ()
    # print fetch.tweets [0]