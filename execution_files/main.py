from datetime import datetime
from configurations.global_config import GlobalConfig
from execution_files.execution_parameters import ExecutionParameters

from data_pulling.reddit_pulling import RedditPuller
from data_pulling.twitter_pulling import TwitterPuller
from data_evaluation.reddit_evaluation import RedditEvaluator
from data_evaluation.twitter_evaluation import TwitterEvaluator
from data_evaluation.reddit_stock_picking import RedditStockPicker
from data_evaluation.twitter_stock_picking import TwitterStockPicker



def main():

    # pull reddit data
    reddit_puller = RedditPuller(subreddit_list=ExecutionParameters.subreddit_list,
                                 time_from=ExecutionParameters.time_from,
                                 time_to=ExecutionParameters.time_to,
                                 reddit_limit=ExecutionParameters.reddit_limit)
    reddit_puller.pull_reddit_data()

    # evaluate reddit data
    reddit_evaluator = RedditEvaluator()
    reddit_evaluator.count_company_ticker_occurrences()

    # pick top stocks from reddit data
    reddit_stock_picker = RedditStockPicker(num_top_stocks=ExecutionParameters.num_top_stocks)
    reddit_stock_picker.pick_top_stocks()

    # pull twitter data
    twitter_puller = TwitterPuller(time_from=ExecutionParameters.time_from,
                                   time_to=ExecutionParameters.time_to)
    twitter_puller.pull_twitter_data()

    # evaluate twitter data
    twitter_evaluator = TwitterEvaluator()
    twitter_evaluator.count_company_ticker_occurrences()

    # pick top stocks from twitter data
    twitter_stock_picker = TwitterStockPicker(num_top_stocks=ExecutionParameters.num_top_stocks)
    twitter_stock_picker.pick_top_stocks()




if __name__ == '__main__':

    # starting time
    starting_time = datetime.now()
    print(starting_time, ': Program started.')
    print(GlobalConfig.SEPARATION_STR)

    # execute program
    main()

    # ending time
    ending_time = datetime.now()
    print(GlobalConfig.SEPARATION_STR)
    print(ending_time, ': Program finished.')

    # execution length
    print('Program took', ending_time-starting_time, 'to run.')


