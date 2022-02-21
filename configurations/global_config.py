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

    # Twitter parameter strings
    TWITTER_TWEET_ID_STR = 'Twitter_tweet_id'
    TWITTER_TWEET_TEXT_STR = 'Twitter_tweet_text'
    TWITTER_TWEET_TIMESTAMP_STR = 'Twitter_tweet_timestamp'

    # AlphaVantage credentials
    ALPHA_VANTAGE_API_KEY_EXTENDED_HISTORY = LocalConfig.ALPHA_VANTAGE_API_KEY_EXTENDED_HISTORY

    # Parameters for AlphaVantage API
    SLICE_LIST_SHORT = ['year1month1']
    SLICE_LIST_LONG = ['year1month1', 'year1month2', 'year1month3', 'year1month4', 'year1month5', 'year1month6',
                       'year1month7', 'year1month8', 'year1month9', 'year1month10', 'year1month11', 'year1month12',
                       'year2month1', 'year2month2', 'year2month3', 'year2month4', 'year2month5', 'year2month6',
                       'year2month7', 'year2month8', 'year2month9', 'year2month10', 'year2month11', 'year2month12']

    # Intervals
    ONE_MIN_INTERVAL_STR = '1min'
    ONE_MIN_INTERVAL_INT = 1
    FIVE_MIN_INTERVAL_STR = '5min'
    FIVE_MIN_INTERVAL_INT = 5
    FIFTEEN_MIN_INTERVAL_STR = '15min'
    FIFTEEN_MIN_INTERVAL_INT = 15
    THIRTY_MIN_INTERVAL_STR = '30min'
    THIRTY_MIN_INTERVAL_INT = 30
    SIXTY_MIN_INTERVAL_STR = '60min'
    SIXTY_MIN_INTERVAL_INT = 60

    # Stock parameters
    STOCK_PARAM_TIME = 'time'
    STOCK_PARAM_OPEN = 'open'
    STOCK_PARAM_CLOSE = 'close'
    STOCK_PARAM_LOW = 'low'
    STOCK_PARAM_HIGH = 'high'
    STOCK_PARAM_VOLUME = 'volume'

    # postgreSQL database credentials
    DB_NAME = LocalConfig.DB_NAME
    USER = LocalConfig.USER
    PW = LocalConfig.PW
    HOST = LocalConfig.HOST
    PORT = LocalConfig.PORT
