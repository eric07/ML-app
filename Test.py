from twitter import *
import json
from datetime import datetime
import time
import requests
import sys

t = Twitter(auth=OAuth("2999654973-YS9XG2UdzWDNJhapOjAUDHjrv5wgG3az3MZ5JfF", "NlP0PWQPJv1Z0lPsH6xv3bb7jw3Aos5xD18ni3ODuDZME", "p6yoZBcF9NnteTV67YbVRwcis", "nY0Q4ugFlef0AtlRTaXptshXxJNGymxFgn4KzaeF77UXlMkRuq"))
    
tweets = t.statuses.user_timeline(screen_name="premierleague", count=100, exclude_replies=True, include_rts=False) 

print tweets[1]
print ("hi!")