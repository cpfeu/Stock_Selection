from configurations.local_config import LocalConfig


class GlobalConfig:

    # CPU count
    NUM_CPUS = LocalConfig.NUM_CPUS

    # Separation string
    SEPARATION_STR = '----------------------------------------------------------------------------------------------'

    # Reddit credentials
    REDDIT_CLIENT_ID = LocalConfig.REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET = LocalConfig.REDDIT_CLIENT_SECRET
    REDDIT_USERNAME = LocalConfig.REDDIT_USERNAME
    REDDIT_PASSWORD = LocalConfig.REDDIT_PASSWORD
    REDDIT_USER_AGENT = LocalConfig.REDDIT_USER_AGENT

    # Subreddit name
    SUBREDDIT_WALLSTREETBETS_STR = 'wallstreetbets'
    SUBREDDIT_INVESTING_STR = 'investing'
    SUBREDDIT_STOCKS_STR = 'stocks'
    SUBREDDIT_PENNYSTOCKS_STR = 'pennystocks'
    SUBREDDIT_ALGOTRADING_STR = 'algotrading'
    SUBREDDIT_SECURITYANALYSIS_STR = 'securityanalysis'
    SUBREDDIT_ROBINHOODPENNYSTOCKS_STR = 'RobinHoodPennyStocks'
    SUBREDDIT_DAYTRADING_STR = 'Daytrading'
    SUBREDDIT_DAYTRADE_STR = 'daytrade'
    SUBREDDIT_STOCKMARKET_STR = 'StockMarket'

    # Reddit parameter strings
    REDDIT_POST_ID_STR = 'Reddit_post_id'
    REDDIT_POST_TITLE_STR = 'Reddit_post_title'
    REDDIT_POST_TEXT_STR = 'Reddit_post_text'
    REDDIT_POST_TIMESTAMP_STR = 'Reddit_post_timestamp'
    REDDIT_POST_NUM_UPS_STR = 'Reddit_post_number_ups'
    REDDIT_POST_NUM_DOWNS_STR = 'Reddit_post_number_downs'
    REDDIT_POST_NUM_COMMENTS_STR = 'Reddit_post_number_comments'
    REDDIT_POST_COMMENTS_STR = 'Reddit_post_comments'

    REDDIT_COMMENT_ID_STR = 'Reddit_comment_id'
    REDDIT_COMMENT_TEXT_STR = 'Reddit_comment_text'
    REDDIT_COMMENT_TIMESTAMP_STR = 'Reddit_comment_timestamp'


    # Twitter credentials
    TWITTER_CONSUMER_KEY = LocalConfig.TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET = LocalConfig.TWITTER_CONSUMER_SECRET
    TWITTER_ACCESS_TOKEN = LocalConfig.TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET = LocalConfig.TWITTER_ACCESS_TOKEN_SECRET

    #Twitter parameter strings
    TWITTER_TWEET_ID_STR = 'Twitter_tweet_id'
    TWITTER_TWEET_TEXT_STR = 'Twitter_tweet_text'
    TWITTER_TWEET_TIMESTAMP_STR = 'Twitter_tweet_timestamp'



