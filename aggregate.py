import os
import csv

if __name__ == "__main__":
    with open('all_tweets.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['tweet_longitude', 'tweet_latitude', 'timestamp', 'status', 'phrase'])

        directory = './data/'
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                with open(os.path.join('./data/', filename), 'r') as file:
                    temp = file.read().splitlines()
                    for line in temp[1:]:
                        f.write(line + ',' + filename[:-4] + '\n')
