import pandas as pd
import tweepy
import re


# function to display data of each tweet
def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Username:{ith_tweet[0]}")
    print(f"Description:{ith_tweet[1]}")
    print(f"Date/Time:{ith_tweet[2]}")
    print(f"Following Count:{ith_tweet[3]}")
    print(f"Follower Count:{ith_tweet[4]}")
    print(f"Total Tweets:{ith_tweet[5]}")
    print(f"Retweet Count:{ith_tweet[6]}")
    print(f"Tweet Text:{ith_tweet[7]}")
    print(f"Hashtags Used:{ith_tweet[8]}")


# function to perform data extraction
def scrape(coin, numtweet, filename):
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])
    query = coin+' AND lang:en AND -is:nullcast AND list:1465337361601114114'
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        datetime = tweet.created_at
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        # in case of invalid reference in retweet, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        text = re.sub("@[A-Za-z0-9_]+","", text)
        text = re.sub("#[A-Za-z0-9_]+", "", text)
        ith_tweet = [username, description, datetime, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet

        printtweetdata(i, ith_tweet)
        i = i + 1
    db.to_csv(filename)


if __name__ == '__main__':
    # credentials for Academic Research Twitter API
    consumer_key = "CONSUMER_KEY"
    consumer_secret = "CONSUMER_SECRET"
    access_key = "ACCESS_KEY"
    access_secret = "ACCESS_SECRET"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    print("Enter Cashtag of Cryptocurrency to search for (ex: $BTC)")
    coin = input()
    print("Enter Number of Tweets to Scrape")
    numtweet = input()
    print("Enter Output File Name (.csv)")
    filename = input()
    scrape(coin, int(numtweet), filename)
    print('Scraping has completed!')
