from datetime import datetime
from configurations.global_config import GlobalConfig
from execution_files.execution_parameters_stock_picking import ExecutionParameters

from data_pulling import *
from data_evaluation import *


def main():

    # starting time
    starting_time = datetime.now()
    print(starting_time, ': Program started.')
    print(GlobalConfig.SEPARATION_STR)

    # pull reddit data
    if ExecutionParameters.USE_MULTITHREADING:
        reddit_puller = RedditPullerSetup(subreddit_list=ExecutionParameters.SUBREDDIT_LIST,
                                          time_from=ExecutionParameters.TIME_FROM,
                                          time_to=ExecutionParameters.TIME_TO,
                                          reddit_limit=ExecutionParameters.REDDIT_LIMIT)
    else:
        reddit_puller = RedditPuller(subreddit_list=ExecutionParameters.SUBREDDIT_LIST,
                                     time_from=ExecutionParameters.TIME_FROM,
                                     time_to=ExecutionParameters.TIME_TO,
                                     reddit_limit=ExecutionParameters.REDDIT_LIMIT)
    total_seconds = reddit_puller.pull_reddit_data()
    print('Scraping took ' + str(total_seconds) + ' to finish.')

    # evaluate reddit data
    reddit_evaluator = RedditEvaluator()
    reddit_evaluator.count_company_ticker_occurrences()

    # pick top stocks from reddit data
    reddit_stock_picker = RedditStockPicker(num_top_stocks=ExecutionParameters.NUM_TOP_STOCKS)
    reddit_stock_picker.pick_top_stocks()

    # pull twitter data
    twitter_puller = TwitterPuller(time_from=ExecutionParameters.TIME_FROM,
                                   time_to=ExecutionParameters.TIME_TO)
    twitter_puller.pull_twitter_data()

    # evaluate twitter data
    twitter_evaluator = TwitterEvaluator()
    twitter_evaluator.count_company_ticker_occurrences()

    # pick top stocks from twitter data
    twitter_stock_picker = TwitterStockPicker(num_top_stocks=ExecutionParameters.NUM_TOP_STOCKS)
    twitter_stock_picker.pick_top_stocks()

    # ending time
    ending_time = datetime.now()
    print(GlobalConfig.SEPARATION_STR)
    print(ending_time, ': Program finished.')

    # execution length
    print('Program took', ending_time - starting_time, 'to run.')


if __name__ == '__main__':
    main()
