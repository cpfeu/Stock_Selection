import os
import json
from configurations.global_config import GlobalConfig


class TwitterEvaluator:

    def __init__(self):
        self.twitter_dict_name = os.listdir('../data/twitter_dicts')[0]
        with open('../data/company_names_dict.json', 'r') as file:
            self.company_names_dict = json.load(file)


    def count_company_ticker_occurences(self):

        # load twitter_dict
        with open('../data/twitter_dicts/' + self.twitter_dict_name, 'r') as file:
            twitter_dict = json.load(file)

        # load list of company tickers
        company_ticker_list = ['$'+symbol for symbol in list(self.company_names_dict.keys())]

        # create count dictionary
        count_dict = dict()

        for idx, ticker in enumerate(company_ticker_list):
            if idx % 1000 == 0:
                print('Searching for ticker with index ' + str(idx) + ' out of around 7000...')

            # add ticker to count dictionary
            count_dict.update({ticker: 0})

            # iterate over each tweet in twitter_dict
            for _, tweet_value in twitter_dict.items():
                tweet_text = tweet_value.get(GlobalConfig.TWITTER_TWEET_TEXT_STR)
                if ' ' + ticker + ' ' in tweet_text:
                    count_dict[ticker] = count_dict.get(ticker) + 1

        # store created dictionaries in twitter_evaluation_dicts
        with open('../data/twitter_evaluation_dicts/twitter_dict_evaluation.json', 'w') as file:
            json.dump(count_dict, file)







