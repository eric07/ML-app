import os, fnmatch, subprocess
import getpass, re, csv, json
from pprint import pprint as pprint
import time

# Class to convert tweet in wanted format
class Parse():
    def __init__(self):
        pass
    def isNew(self, twStrings, newString):
        if newString in twStrings:
            return False
        return True
        
    # Function to return tweet in wanted format. For now focusing on text
    def parseOne(self, tweet):
        hashtags = []
        user_mentions = []
        urls = []
        for hashtag in tweet['entities']['hashtags']:
            hashtags.append(hashtag['text'])
        for url in tweet['entities']['urls']:
            urls.append(url['expanded_url'])
        for user in tweet['entities']['user_mentions']:
            user_mentions.append({
                "screen_name": user['screen_name'],
                "name": user['name']
            })
        link = None
        if "media" in tweet['entities']:
            link = tweet['entities']['media'][0]['media_url']
        return tweet['text'] 
        # Scraping the rest of the tweet attributes
            # "id" : str(tweet['id']),
            # "created_at" : tweet['created_at'],
            # "py_time": time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
            # "classId" : -1,
            # "user_mentions": user_mentions,
            # "hashtags": hashtags,
            # "urls": urls,
            # "retweet_count": int(tweet['retweet_count']),
            # "favourites_count": int(tweet['user']['favourites_count']),
            # "avatar": link

    # parse many tweets
    def parseJson(self, tweets):
        ids = [] # ensure unique ids
        twStrings = [] # body of tweets (to check for uniqueness)
        parsedTweets = []
        for line in tweets:
            if line['id'] not in ids and self.isNew(twStrings, line['text']):
                twStrings.append(line['text'])
                ids.append(line['id'])
                link = None
                if "media" in line['entities']:
                    link = line['entities']['media'][0]['media_url']

                parsedTweets.append({
                    "id" : str(line['id']),
                    "text" : line['text'],
                    "created_at" : line['created_at'],
                    "py_time": time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(line['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
                    "classId" : 0,
                    "avatar" : link
                    })
        parsedTweets = self.sortTweets(parsedTweets)
        return parsedTweets

    # Get tweet ID
    def getKey(self, item):
        return int(item['id'])

    # Sort Tweets
    def sortTweets(self, tweets):
        tweets = sorted(tweets, key=self.getKey)
        return tweets

if __name__ == '__main__':
    print("Run from Main class")