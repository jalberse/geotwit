import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('all_tweets.csv')

plt.plot(data['tweet_latitude'],data['tweet_longitude'],'ro')
plt.show()
