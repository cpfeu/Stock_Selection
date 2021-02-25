from configurations.global_config import GlobalConfig


class ExecutionParameters:

    subreddit_list = [GlobalConfig.SUBREDDIT_WALLSTREETBETS_STR,
                      GlobalConfig.SUBREDDIT_INVESTING_STR,
                      GlobalConfig.SUBREDDIT_PENNYSTOCKS_STR,
                      GlobalConfig.SUBREDDIT_STOCKS_STR,
                      GlobalConfig.SUBREDDIT_ALGOTRADING_STR,
                      GlobalConfig.SUBREDDIT_SECURITYANALYSIS_STR,
                      GlobalConfig.SUBREDDIT_ROBINHOODPENNYSTOCKS_STR,
                      GlobalConfig.SUBREDDIT_DAYTRADING_STR,
                      GlobalConfig.  SUBREDDIT_DAYTRADE_STR,
                      GlobalConfig.SUBREDDIT_STOCKMARKET_STR]
    time_from = '2021-02-23 01:00:01'
    time_to = '2021-02-23 17:59:59'
    reddit_limit = 1000
    num_top_stocks = 7