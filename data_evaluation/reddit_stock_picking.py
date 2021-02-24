import os
import json
import multiprocessing
from operator import itemgetter
from configurations.global_config import GlobalConfig


class RedditStockPicker:

    def __init__(self, num_top_stocks):
        self.num_top_stocks = num_top_stocks
        self.reddit_evaluation_dicts_name_list = os.listdir('../data/reddit_evaluation_dicts')


    def pick_top_stocks(self):

        # create argument list for multiprocessing worker
        arg_list = [(reddit_evaluation_dict_name, self.num_top_stocks)
                    for reddit_evaluation_dict_name in self.reddit_evaluation_dicts_name_list]

        # start multiprocessing
        with multiprocessing.Pool(GlobalConfig.NUM_CPUS) as mp:
            mp.starmap(self.pick_top_stocks_worker, arg_list)


    @classmethod
    def pick_top_stocks_worker(cls, reddit_evaluation_dict_name, num_top_stocks):

        # extract subreddit name
        subreddit_name = reddit_evaluation_dict_name[:-29]

        # load reddit evaluation dict
        with open('../data/reddit_evaluation_dicts/'+reddit_evaluation_dict_name, 'r') as file:
            reddit_evaluation_dict = json.load(file)

        # pick stocks that were mentioned the most
        top_stock_dict = dict(sorted(reddit_evaluation_dict.items(), key=itemgetter(1), reverse=True)[:num_top_stocks])

        # show top stocks
        print(GlobalConfig.SEPARATION_STR)
        print('Top stocks from <'+subreddit_name+'> subreddit:')
        print(top_stock_dict)


