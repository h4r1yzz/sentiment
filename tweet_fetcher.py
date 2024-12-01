import asyncio
import re
from twikit import Client, TooManyRequests
from datetime import datetime
from configparser import ConfigParser
from random import randint
from sentimental_analysis import get_sentiment  # Import sentiment analysis function

# Function to fetch tweets asynchronously
async def fetch_tweets_async(query, minimum_tweets=10):
    async def get_tweets(client, tweets):
        if tweets is None:
            print(f'{datetime.now()} - Getting tweets for query: {query}...')
            tweets = await client.search_tweet(query, product='Top')
        else:
            wait_time = randint(5, 8)
            print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
            await asyncio.sleep(wait_time)
            tweets = await tweets.next()
        return tweets

    # Read configuration
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    # Initialize and login to the client
    client = Client(language='en-US')
    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.load_cookies('cookies.json')

    tweets_list = []
    tweet_count = 0
    tweets = None

    while tweet_count < minimum_tweets:
        try:
            tweets = await get_tweets(client, tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1

            # Extract URLs from the tweet text using regex
            urls = re.findall(r'http[s]?://\S+', tweet.text)

            # Get sentiment analysis
            sentiment = get_sentiment(tweet.text)

            # Create tweet data with URLs in a separate column
            tweet_data = {
                "count": tweet_count,
                "username": tweet.user.name,
                "text": tweet.text,
                "created_at": tweet.created_at,
                "retweets": tweet.retweet_count,
                "likes": tweet.favorite_count,
                "sentiment": sentiment,
                "urls": ', '.join(urls)  # Store the URLs (if any) in a separate column
            }
            tweets_list.append(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print("Login and tweet retrieval successful!")
    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')
    return tweets_list
