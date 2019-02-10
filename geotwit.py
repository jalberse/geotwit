import json
import os
import csv
import string

import tweepy

DEBUG = 1

class MyStreamListenener(tweepy.StreamListener):
    """
    Listen for data
    """
    def __init__(self, tracking, api=None):
        super().__init__(api)
        self.tracking = tracking

    def on_status(self, status):
        # skip if no geolocation
        if status.coordinates == None:
            return

        # TODO: This is a HORRIBLE way to determine which phrase was a hit
        # But for the hackathon this should match at least match words...

        # Determine which phrase this status hits
        # crunch on status text
        text = ''.join(x for x in status.text if x in string.ascii_letters + '\'- ')
        text = text.split()
        tokenized_status = []
        # now ignore casing
        for token in text:
            tokenized_status.append(token.casefold())
        ##if (DEBUG): print("tokenized status: " + str(tokenized_status))
        if DEBUG:
            print(tokenized_status)

        # crunch on phrases
        tokenized_phrases_pairs = []
        for p in tracking:
            x = p.casefold()
            tokenized_phrases_pairs.append([x, x.split()])
        ##if (DEBUG): print("tokenized phrases: " + str(tokenized_phrases_pairs))

        # check which filter it passed
        passed_filter = ""
        for p in tokenized_phrases_pairs:
            if set(p[1]).issubset(set(tokenized_status)):
                passed_filter = p[0]
                if (DEBUG):
                    print(status.text)
                    print("passed filter: " + p[0])
                break

        if (passed_filter == ""):
            # discrepency between our match and twitters, ignore
            if (DEBUG):
                print(status.text)
                print("ignoring the problem (incorrect match)")
            return

        with open(os.path.join('./data/', passed_filter + '.csv'), 'a') as file:
            if (DEBUG): print('saving to ./data/' + passed_filter + '.csv')
            w = csv.writer(file)
            lon = status.coordinates["coordinates"][0]
            lat = status.coordinates["coordinates"][0]
            if (DEBUG):
                print(str(lon) + ',' + str(lat) + ',' + str(status.created_at))
            w.writerow([str(lon), str(lat), str(status.created_at), status.text])

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

    # Prepare files
    with open('track.txt') as f:
        tracking = f.read()
        tracking = tracking.casefold()
        tracking = tracking.splitlines()
    for phrase in tracking:
        filename = os.path.join('./data/',phrase + '.csv')
        if not os.path.exists(filename):
            if not os.path.exists('./data/'):
                os.mkdir('./data/')
            with open(filename, 'a+') as f:
                writer = csv.writer(f)
                writer.writerow(['Longitude', 'Latitude', 'Timestamp', 'Status'])

    # Set up stream and start listening
    stream_listener = MyStreamListenener(tracking)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener,
                           tweet_mode='extended')
    stream.filter(track=tracking)
