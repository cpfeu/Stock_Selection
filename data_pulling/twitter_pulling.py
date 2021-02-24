import os
import json
import tweepy
from datetime import datetime
from operator import itemgetter
from configurations.global_config import GlobalConfig


class TwitterPuller:

    def __init__(self, time_from, time_to):
        self.query_list = get_query_list()
        self.time_from = datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')
        self.time_to = datetime.strptime(time_to, '%Y-%m-%d %H:%M:%S')
        self.consumer_key = GlobalConfig.TWITTER_CONSUMER_KEY
        self.consumer_secret = GlobalConfig.TWITTER_CONSUMER_SECRET
        self.access_token = GlobalConfig.TWITTER_ACCESS_TOKEN
        self.access_token_secret = GlobalConfig.TWITTER_ACCESS_TOKEN_SECRET


    def pull_twitter_data(self):

        # create OAuthHandler object
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

        # set access token and secret
        auth.set_access_token(self.access_token, self.access_token_secret)

        # create tweepy API object to fetch tweets
        api = tweepy.API(auth)

        # twitter dict with scraped information
        twitter_dict = dict()

        # loop over each search query
        for query in self.query_list:
            fetched_tweets = api.search(query, count=100000000, result_type='recent')

            # add relevant information to twitter dictionary
            for status in fetched_tweets:
                if (status.created_at >= self.time_from) and (status.created_at <= self.time_to):
                    twitter_dict.update({status.text: {GlobalConfig.TWITTER_TWEET_ID_STR: status.id_str,
                                                       GlobalConfig.TWITTER_TWEET_TEXT_STR: status.text,
                                                       GlobalConfig.TWITTER_TWEET_TIMESTAMP_STR:
                                                           status.created_at.strftime('%Y-%m-%d %H:%M:%S')}})

        # save twitter dict
        current_utc_timestamp_str = str(datetime.now().timestamp())
        with open('../data/twitter_dicts/twitter_dict_'+current_utc_timestamp_str+'.json', 'w') as file:
            json.dump(twitter_dict, file)


def get_query_list():
    # initialize empty list
    query_set = set()

    # list all reddit evaluation dicts
    reddit_evaluation_dict_names = os.listdir('../data/reddit_evaluation_dicts')

    # loop over each dict
    for name in reddit_evaluation_dict_names:

        # extract top entries
        with open('../data/reddit_evaluation_dicts/'+name, 'r') as file:
            reddit_evaluation_dict = json.load(file)
        top_stock_dict = dict(sorted(reddit_evaluation_dict.items(), key=itemgetter(1), reverse=True)[:10])

        for key in top_stock_dict.keys():
            query_set.add(key)

    # convert set to list
    query_list = list(query_set)
    return query_list