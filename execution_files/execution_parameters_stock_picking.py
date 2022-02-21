from configurations.global_config import GlobalConfig


class ExecutionParameters:

    # List of subreddits to consider for searching for stock tickers
    SUBREDDIT_LIST = [GlobalConfig.SUBREDDIT_WALLSTREETBETS_STR,
                      GlobalConfig.SUBREDDIT_INVESTING_STR,
                      GlobalConfig.SUBREDDIT_PENNYSTOCKS_STR,
                      GlobalConfig.SUBREDDIT_STOCKS_STR,
                      GlobalConfig.SUBREDDIT_ALGOTRADING_STR,
                      GlobalConfig.SUBREDDIT_SECURITYANALYSIS_STR,
                      GlobalConfig.SUBREDDIT_ROBINHOODPENNYSTOCKS_STR,
                      GlobalConfig.SUBREDDIT_DAYTRADING_STR,
                      GlobalConfig.SUBREDDIT_DAYTRADE_STR,
                      GlobalConfig.SUBREDDIT_STOCKMARKET_STR]

    # time frame for reddit data to scrape
    TIME_FROM = '2022-02-18 05:00:01'
    TIME_TO = '2022-02-20 13:00:00'

    # limit the number of hot and new reddit posts to
    REDDIT_LIMIT = 2

    # pick the number of top stocks to get
    NUM_TOP_STOCKS = 7

    # speed up the reddit scraping process
    USE_MULTITHREADING = True
