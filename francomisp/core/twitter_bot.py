import tweepy
from tweepy import OAuthHandler

from francomisp.keys import twitter_consumer_key, twitter_consumer_secret, twitter_access_secret, twitter_access_token
from francomisp.utils.tweet_content import TweetContent

class TwitterBot:

    @staticmethod
    def search():

        auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_access_secret)
        api = tweepy.API(auth)
        max_id = 0
        tweets = []
        list_ids = api.saved_searches()
        for ListId in list_ids:
            Query = ListId.name
            for page in range(1, 3):
                if page == 1:
                    tweets = api.search(q=Query, rpp=100,tweet_mode='extended')
                else:
                    tweets = api.search(q=Query, rpp=100, max_id=max_id,tweet_mode = 'extended')
                for tweet in tweets:
                    yield tweet

    @staticmethod
    def extract_url(tweet, twitter_content):
        urls_pasties = [ twitter_content.url_rewrite(url['expanded_url']) for url in tweet.entities['urls']]
        if hasattr(tweet, 'retweeted_status'):
            urls_pasties.extend([ url['expanded_url']for url in  tweet.retweeted_status.entities['urls']])
        return urls_pasties

