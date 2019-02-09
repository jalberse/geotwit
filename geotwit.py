import json
import os
import csv

import tweepy

class MyStreamListenener(tweepy.StreamListener):
    """
    Listen for data
    """
    def on_status(self, status):
        print(status.coordinates) # TODO save to s

if __name__ == '__main__':
    # Auth setup
    try:
        if os.path.isfile(".my_keys"):
            KEYS_FILE = open(".my_keys", 'r')
        else:
            KEYS_FILE = open("keys.json", 'r')
    except OSError:
        print("Error opening keys file")

    KEYS = json.load(KEYS_FILE)
    CONSUMER_KEY = KEYS['websites']['Twitter']['consumer_key']
    CONSUMER_SECRET = KEYS['websites']['Twitter']['consumer_secret']
    ACCESS_TOKEN = KEYS['websites']['Twitter']['access_token']
    ACCESS_TOKEN_SECRET = KEYS['websites']['Twitter']['access_secret']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth_handler=auth)

    stream_listener = MyStreamListenener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    f = open('track.txt')
    line = f.readline()
    tracking = []
    while line:
        tracking.append(line)
        line = f.readline()
    stream.filter(track=tracking)
