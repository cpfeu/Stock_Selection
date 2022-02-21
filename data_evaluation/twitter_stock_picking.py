import os
import json
from operator import itemgetter
from configurations.global_config import GlobalConfig


class TwitterStockPicker:

    def __init__(self, num_top_stocks):
        self.num_top_stocks = num_top_stocks
        self.twitter_evaluation_dict_name = os.listdir('../data/twitter_evaluation_dicts')[0]

    def pick_top_stocks(self):

        # load twitter evaluation dict
        with open('../data/twitter_evaluation_dicts/'+self.twitter_evaluation_dict_name, 'r') as file:
            twitter_evaluation_dict = json.load(file)

        # pick stocks that were mentioned the most
        top_stock_dict = dict(sorted(twitter_evaluation_dict.items(), key=itemgetter(1), reverse=True)[:self.num_top_stocks])

        # show top stocks
        print(GlobalConfig.SEPARATION_STR)
        print('Top stocks from Twitter based on reddit evaluation dicts:')
        print(top_stock_dict)


