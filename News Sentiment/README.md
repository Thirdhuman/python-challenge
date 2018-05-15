

```python
#Insights
# 1. New York Times has had the most positive tweets as of late
# 2. The BBC Global Twtter has had the most positive tweets as of late
# 3. Fox CBS and CNN have compound polarity scores that are close to 0
# 4. The sentiment of tweets as a whole do not seem highly correlated with one another during the time range
```


```python
# Dependencies
import tweepy
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
import time
import pytz
# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# Twitter API Keys
from config import (consumer_key,
                    consumer_secret,
                    access_token,
                    access_token_secret)
#Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, 
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify= True,
                 parser=tweepy.parsers.JSONParser())
#Format times
utc=pytz.UTC
startDate = datetime(2018, 1, 1, 0, 0, 0)
endDate = datetime(2018, 4, 10, 0, 0, 0)
startDate = utc.localize(startDate) 
endDate = utc.localize(endDate) 
```


```python
# Target User Accounts
target_user = ("@nytimes", "@CBSNews",'@FoxNews', '@BBCWorld', "@CNN")
# List for dictionaries of results
counter = 0
# Loop through each user
for user in target_user:  
    counter = 0
    # Variables for holding sentiments
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []
    converted_timestamps = []
    tweet_times = []
    counter_list = [] 
    # Loop through pages.
    for x in range(0, 1):
        # Get all tweets from home feed
        public_tweets = api.user_timeline(user, page=x, count=100)
        # Loop through all tweets
        for tweet in public_tweets:
            created_at= (tweet['created_at'])
            created_at =datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
            try:
                # Run Vader Analysis on each tweet
                counter += 1
                results = analyzer.polarity_scores(tweet["text"])
                compound = results["compound"]
                pos = results["pos"]
                neu = results["neu"]
                neg = results["neg"]
                tweet_times.append(tweet["created_at"])
                compound_list.append(compound)
                positive_list.append(pos)
                negative_list.append(neg)
                neutral_list.append(neu)
                counter_list.append(counter)
            except Exception as e:
                print(e)
                continue
        #Create a dictionaty of results    
        user_results = pd.DataFrame({
            "Compound Score": (compound_list),
            "Postive Score": (positive_list),
            "Neutral Score": (neutral_list),
            "Negative Score": (negative_list),
            "Tweet Time": (tweet_times),
            "Tweets Ago": (counter_list)
        })
        user_results['Username'] = user
        if user == "@nytimes":
            final_results = user_results.copy()
        else:
            frames = [final_results, user_results]
            final_results = pd.concat(frames)

#Uncheck below if worried about large # of Tweets as a save.
#copy = final_results.copy()
```


```python
#Double Check # of Tweets
final_results2 = final_results[~(final_results['Tweets Ago'] >= 101)]  
print(final_results.count())
print(final_results2.count())
```

    Compound Score    500
    Negative Score    500
    Neutral Score     500
    Postive Score     500
    Tweet Time        500
    Tweets Ago        500
    Username          500
    dtype: int64
    Compound Score    500
    Negative Score    500
    Neutral Score     500
    Postive Score     500
    Tweet Time        500
    Tweets Ago        500
    Username          500
    dtype: int64



```python
# Create DataFrame from Results List
results_df = final_results2.reset_index()
results_df = pd.DataFrame(results_df).round(5)
results_df['converted_time'] = ''
results_df['Username'] = results_df['Username'].astype(str)
results_df.set_index('index')
results_df['index'] = results_df['index'].astype(int)
results_df = results_df.drop_duplicates()
results_df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>Compound Score</th>
      <th>Negative Score</th>
      <th>Neutral Score</th>
      <th>Postive Score</th>
      <th>Tweet Time</th>
      <th>Tweets Ago</th>
      <th>Username</th>
      <th>converted_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>-0.7003</td>
      <td>0.290</td>
      <td>0.621</td>
      <td>0.090</td>
      <td>Tue Apr 10 20:40:04 +0000 2018</td>
      <td>1</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>-0.0772</td>
      <td>0.071</td>
      <td>0.929</td>
      <td>0.000</td>
      <td>Tue Apr 10 20:19:44 +0000 2018</td>
      <td>2</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>0.4404</td>
      <td>0.000</td>
      <td>0.868</td>
      <td>0.132</td>
      <td>Tue Apr 10 20:17:07 +0000 2018</td>
      <td>3</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>-0.3182</td>
      <td>0.148</td>
      <td>0.759</td>
      <td>0.093</td>
      <td>Tue Apr 10 20:10:07 +0000 2018</td>
      <td>4</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>Tue Apr 10 20:03:41 +0000 2018</td>
      <td>5</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>-0.1779</td>
      <td>0.166</td>
      <td>0.655</td>
      <td>0.179</td>
      <td>Tue Apr 10 19:55:03 +0000 2018</td>
      <td>6</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>-0.6705</td>
      <td>0.244</td>
      <td>0.756</td>
      <td>0.000</td>
      <td>Tue Apr 10 19:45:50 +0000 2018</td>
      <td>7</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>Tue Apr 10 19:40:09 +0000 2018</td>
      <td>8</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>Tue Apr 10 19:30:10 +0000 2018</td>
      <td>9</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>0.4404</td>
      <td>0.000</td>
      <td>0.822</td>
      <td>0.178</td>
      <td>Tue Apr 10 19:25:48 +0000 2018</td>
      <td>10</td>
      <td>@nytimes</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
# Ready Data for graphing.
for (idx,row) in results_df.iterrows():
    raw_time = (row.loc['Tweet Time'])
    converted_time = datetime.strptime(raw_time, "%a %b %d %H:%M:%S %z %Y")
    results_df.at[idx, 'converted_time'] = converted_time
results_df['date'] = pd.to_datetime(results_df['converted_time']).dt.date
results_df['days_ago'] =(max(results_df['date']) - results_df['date'])
results_df['days_ago'] = ((results_df['days_ago']).dt.days* -1)
endDateDay = datetime(int(2018), int(4), int(9))
results_df.set_index('Username')
results_df.to_csv('News_tweets(Ungrouped).csv')
results_df_tweet = results_df.groupby(['Username','Tweets Ago']).mean()
results_df_tweet = results_df_tweet.reset_index()
results_df_tweet.to_csv('News_tweets(grouped).csv')
```


```python
# Create plot 1
fig = plt.figure()
plt.rc('figure', figsize=(12, 8))
colors = {"@nytimes":'lightskyblue',
          "@CBSNews":'orange', 
          "@FoxNews":'red',
          '@BBCWorld': 'blue', 
          '@CNN': 'green'}
x_vals = results_df_tweet["Tweets Ago"]
y_vals = results_df_tweet["Compound Score"]
with plt.style.context('ggplot'):
    plt.scatter(x_vals,
             y_vals, marker="o", linewidth=0.5,
             alpha=0.8, c=results_df_tweet['Username'].apply(lambda x: colors[x]))
plt.title(f"Sentiment of Tweets ({results_df['date'][0]}) for News Organization Tweets")
plt.xlim([x_vals.max(),x_vals.min()])
plt.ylabel("Tweet Polarity")
plt.xlabel("Tweets ago")
plt.grid(alpha=.75)
plt.show()
fig.savefig("Plot_News.png")
```


    <matplotlib.figure.Figure at 0x1a17924240>



![png](output_6_1.png)



```python
# Create plot 2
results_df_mean = results_df.groupby(['Username']).mean()
results_df_mean = results_df_mean.reset_index()
x_vals = np.arange(len(results_df_mean['Username']))
x_names = results_df_mean['Username']
y_vals = results_df_mean["Compound Score"]
width = 0.4
fig = plt.figure()
fig, ax = plt.subplots()
with plt.style.context(('ggplot')):
    barp = ax.bar(x_vals, y_vals, width = 0.7,
    color=[colors[r] for r in results_df_mean['Username']] )
ax.set_title(f"Bar Chart - Sentiment of Tweets ({results_df['date'][0]}) for News Organization Tweets")
ax.set_xticks(np.arange(5) + width / 2)
ax.set_xticklabels(["@nytimes", "@CBSNews",'@FoxNews', '@BBCWorld', "@CNN"])
ax.set_ylabel('Tweet Polarity')
ax.set_facecolor('xkcd:light grey')
ax.axhline(y=0, color='black', linestyle='-')
vals = ax.get_yticks()
ax.set_yticklabels(['{:.0f}%'.format(x*100) for x in vals])
def autolabel(rects, ax):
    (y_bottom, y_top) = ax.get_ylim()
    y_height = y_top - y_bottom
    for rect in rects:
        height = rect.get_height()
        p_height = (height / y_height)
        if p_height > 0.95: 
            label_position = height - (y_height * 0.50)
        else:
            label_position = height + (y_height * 0.01)
        ax.text(rect.get_x() + rect.get_width()/2., label_position,
                "{:.1%}".format(height),
                ha='center', va='bottom')
autolabel(barp, ax)
plt.show()
fig.savefig("Bar_News.png")
```


    <matplotlib.figure.Figure at 0x1a178bfe10>



    <matplotlib.figure.Figure at 0x1a175dfc50>



![png](output_7_2.png)

