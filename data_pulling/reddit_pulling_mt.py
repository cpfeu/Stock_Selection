import os
import praw
import json
import threading
from datetime import datetime
from configurations.global_config import GlobalConfig


class RedditPullerThread(threading.Thread):

    def __init__(self, subreddit_name, reddit_pulling_setup):
        threading.Thread.__init__(self)
        self.subreddit_name = subreddit_name
        self.reddit_pulling_setup = reddit_pulling_setup

    def run(self):

        print('Thread to scrape data from subreddit <' + str(self.subreddit_name) + '> started...')

        # create list reddit generators
        subreddit = self.reddit_pulling_setup.reddit_object.subreddit(self.subreddit_name)
        hot_subreddit = subreddit.hot(limit=self.reddit_pulling_setup.reddit_limit)
        new_subreddit = subreddit.new(limit=self.reddit_pulling_setup.reddit_limit)
        reddit_generator_list = [hot_subreddit, new_subreddit]

        # reddit dict with all scraped information
        reddit_dict = dict()

        # get hot and new reddit posts
        for reddit_generator in reddit_generator_list:

            # iterate over each reddit post
            for reddit_post in reddit_generator:

                # check if reddit post is relevant for search query
                reddit_post_timestamp = datetime.utcfromtimestamp(reddit_post.created_utc)
                if (reddit_post.stickied is False) and \
                        (reddit_post_timestamp >= self.reddit_pulling_setup.time_from) and \
                        (reddit_post_timestamp <= self.reddit_pulling_setup.time_to):

                    # fill reddit dictionary with information
                    reddit_dict.update({reddit_post.id: {GlobalConfig.REDDIT_POST_TITLE_STR: reddit_post.title,
                                                         GlobalConfig.REDDIT_POST_TEXT_STR: reddit_post.selftext,
                                                         GlobalConfig.REDDIT_POST_TIMESTAMP_STR:
                                                             datetime.utcfromtimestamp(reddit_post.created_utc).
                                                             strftime('%Y-%m-%d %H:%M:%S'),
                                                         GlobalConfig.REDDIT_POST_NUM_UPS_STR: reddit_post.ups,
                                                         GlobalConfig.REDDIT_POST_NUM_DOWNS_STR: reddit_post.downs,
                                                         GlobalConfig.REDDIT_POST_NUM_COMMENTS_STR:
                                                             reddit_post.num_comments,
                                                         GlobalConfig.REDDIT_POST_COMMENTS_STR: {}}})

                    reddit_post.comments.replace_more(limit=30)
                    reddit_post_comments = reddit_post.comments.list()
                    for reddit_post_comment in reddit_post_comments:
                        reddit_dict.get(reddit_post.id). \
                            get(GlobalConfig.REDDIT_POST_COMMENTS_STR). \
                            update({reddit_post_comment.id: {
                                GlobalConfig.REDDIT_COMMENT_TIMESTAMP_STR: datetime.utcfromtimestamp(
                                    reddit_post_comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                                GlobalConfig.REDDIT_COMMENT_TEXT_STR: reddit_post_comment.body}})

        # save reddit dict of current subreddit
        current_utc_timestamp_str = str(datetime.now().timestamp())
        with open('../data/reddit_dicts/' + self.subreddit_name + '_reddit_dict_' + current_utc_timestamp_str + '.json',
                  'w') as file:
            json.dump(reddit_dict, file)

        print('Thread to scrape data from subreddit <' + str(self.subreddit_name) + '> finished.')


class RedditPullerSetup:

    def __init__(self, subreddit_list=[GlobalConfig.SUBREDDIT_WALLSTREETBETS_STR],
                 time_from='1111-11-11 11:11:11', time_to='2222-11-11 11:11:11', reddit_limit=10000):
        self.subreddit_list = subreddit_list
        self.reddit_object = praw.Reddit(client_id=GlobalConfig.REDDIT_CLIENT_ID,
                                         client_secret=GlobalConfig.REDDIT_CLIENT_SECRET,
                                         username=GlobalConfig.REDDIT_USERNAME,
                                         password=GlobalConfig.REDDIT_PASSWORD,
                                         user_agent=GlobalConfig.REDDIT_USER_AGENT)
        self.time_from = datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')
        self.time_to = datetime.strptime(time_to, '%Y-%m-%d %H:%M:%S')
        self.reddit_limit = reddit_limit

        # create directory and delete old files
        os.makedirs('../data/reddit_dicts', exist_ok=True)
        for file in os.listdir('../data/reddit_dicts'):
            os.remove(os.path.join('../data/reddit_dicts', file))

    def pull_reddit_data(self):

        starting_time = datetime.now()

        # loop over each subreddit that is queried and start a scraping thread to speed up time
        reddit_scraping_thread_list = []
        for subreddit_name in self.subreddit_list:
            t = RedditPullerThread(subreddit_name=subreddit_name,
                                   reddit_pulling_setup=self)
            t.start()
            reddit_scraping_thread_list.append(t)
        for t in reddit_scraping_thread_list:
            t.join()

        ending_time = datetime.now()

        return (ending_time - starting_time).total_seconds()
